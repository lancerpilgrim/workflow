'''
'''
from __future__ import absolute_import, division, print_function, with_statement

# Tornado framework
import tornado.web
HTTPError = tornado.web.HTTPError

import tornado.ioloop
import tornado.auth
import tornado.escape
import tornado.options
import tornado.locale
import tornado.httpclient
import tornado.gen
import tornado.httputil
from tornado.util import errno_from_exception
from tornado.platform.auto import set_close_exec
from tornado.log import access_log, gen_log, app_log
# from tornado.concurrent import Future

import errno
import os
import sys

import time

import socket
import collections
import functools
import copy

from urlparse import parse_qs

# import xml.etree.ElementTree as ET

# Mako template
import mako.lookup
import mako.template

import radius.utility as utility
# import settings
import radius.config as config
import user_agents

import radius.account as account
import radius.template as template

from radius.task import portal


portal_config = config['portal_config']

json_encoder = utility.json_encoder
json_decoder = utility.json_decoder

_PORTAL_VERSION = 0x01
RUN_PATH = '/var/run'

_REQUESTES_ = {}

AC_CONFIGURE = {}

BAS_PORT = 2000
_BUFSIZE=1024

PORTAL_PORT = 50100

LOGIN = 0
LOGOUT = 1

WWW_PATH = config['www_path']


PN_PROFILE = collections.defaultdict(dict)
AP_MAPS = {}

# MOBILE_PATTERN = re.compile(r'^(?:13[0-9]|14[57]|15[0-35-9]|17[678]|18[0-9])\d{8}$')

class Application(tornado.web.Application):
    '''
        Web application class.
        Redefine __init__ method.
    '''
    def __init__(self):
        handlers = [
            (r'/account$', PortalHandler),
            (r'/user/(.*)$', UserHandler),
            (r'/pn/(.*)$', PnHandler),
            (r'/wx_auth$', PortalHandler),
            (r'/(.*?\.html)$', PageHandler),
            # in product environment, use nginx to support static resources
            (r'/(.*\.(?:css|jpg|js|png))$', tornado.web.StaticFileHandler, 
             {'path':WWW_PATH}),
            (r'/test$', TestHandler),
            # (r'/weixin', WeiXinHandler),
        ]
        settings = {
            'cookie_secret':utility.sha1('portal_server').hexdigest(), 
            'static_path':WWW_PATH,
            # 'static_url_prefix':'resource/',
            'debug':False,
            'autoreload':True,
            'autoescape':'xhtml_escape',
            'i18n_path':os.path.join(WWW_PATH, 'resource/i18n'),
            # 'login_url':'',
            'xheaders':True,    # use headers like X-Real-IP to get the user's IP address instead of
                                # attributeing all traffic to the balancer's IP address.
        }
        super(Application, self).__init__(handlers, **settings)

class BaseHandler(tornado.web.RequestHandler):
    '''
        BaseHandler
        override class method to adapt special demands
    '''
    HTML_PATH = os.path.join(config['www_path'], 'html')
    LOOK_UP = mako.lookup.TemplateLookup(directories=[HTML_PATH, ], 
                                         module_directory='/tmp/mako/portal',
                                         output_encoding='utf-8',
                                         input_encoding='utf-8',
                                         encoding_errors='replace')

    RESPONSES = {}
    RESPONSES.update(tornado.httputil.responses)
    from bd_err import portal_responses
    RESPONSES.update(portal_responses)

    def initialize(self, lookup=LOOK_UP):
        '''
        '''
        pass

    def render_string(self, filename, **kwargs):
        '''
            Override render_string to use mako template.
            Like tornado render_string method, this method also
            pass request handler environment to template engine
        '''
        try:
            template = self.LOOK_UP.get_template(filename)
            env_kwargs = dict(
                handler = self,
                request = self.request,
                locale = self.locale,
                _ = self.locale.translate,
                static_url = self.static_url,
                xsrf_form_html = self.xsrf_form_html,
                reverse_url = self.application.reverse_url,
                agent = self.agent,
            )
            env_kwargs.update(kwargs)
            return template.render(**env_kwargs)
        except:
            from mako.exceptions import RichTraceback
            tb = RichTraceback()
            for (module_name, line_no, function_name, line) in tb.traceback:
                print('File:{}, Line:{} in {}'.format(module_name, line_no, function_name))
                print(line)
            access_log.error('Render {} failed, {}:{}'.format(filename, tb.error.__class__.__name__, tb.error), 
                         exc_info=True)
            raise HTTPError(500, 'Render page failed')

    def render(self, filename, **kwargs):
        '''
            Render the template with the given arguments
        '''
        # if not os.path.exists(os.path.join(directory, filename)):
        #     raise HTTPError(404, 'File Not Found')

        self.finish(self.render_string(filename, **kwargs))

    def _get_argument(self, name, default, source, strip=True):
        args = self._get_arguments(name, source, strip=strip)
        if not args:
            if default is self._ARG_DEFAULT:
                raise tornado.web.MissingArgumentError(name)
            return default
        return args[0]

    def set_status(self, status_code, reason=None):
        '''
            Set custom error resson
        '''
        self._status_code = status_code
        self._reason = 'Unknown Error'
        if reason is not None:
            self._reason = tornado.escape.native_str(reason)
        else:
            try:
                self._reason = self.RESPONSES[status_code]
            except KeyError:
                raise ValueError('Unknown status code {}'.format(status_code))

    def write_error(self, status_code, **kwargs):
        '''
            Customer error return format
        '''
        if self.settings.get('Debug') and 'exc_info' in kwargs:
            self.set_header('Content-Type', 'text/plain')
            import traceback
            for line in traceback.format_exception(*kwargs['exc_info']):
                self.write(line)
            self.finish()
        else:
            # self.render('error.html', Code=status_code, Msg=self._reason)
            if status_code in (427,):
                self.render_json_response(Code=status_code, Msg=self.RESPONSES[status_code], pn=self.profile['pn'])
            elif status_code in (428, ):
                downmacs = 0 
                if self.profile['pn'] in (15914, 59484):
                    downmacs = 1
                self.render_json_response(Code=status_code, Msg=self.RESPONSES[status_code], 
                                          downMacs=downmacs, macs=self.response_kwargs.get('macs', ''))
            else:
                self.render_json_response(Code=status_code, Msg=self._reason)

    def _handle_request_exception(self, e):
        if isinstance(e, tornado.web.Finish):
            # not an error; just finish the request without loggin.
            if not self._finished:
                self.finish(*e.args)
            return
        try:
            self.log_exception(*sys.exc_info())
        except Exception:
            access_log.error('Error in exception logger', exc_info=True)

        if self._finished:
            return 
        if isinstance(e, HTTPError):
            if e.status_code not in BaseHandler.RESPONSES and not e.reason:
                tornado.gen_log.error('Bad HTTP status code: %d', e.status_code)
                self.send_error(500, exc_info=sys.exc_info())
            else:
                self.send_error(e.status_code, exc_info=sys.exc_info())
        else:
            self.send_error(500, exc_info=sys.exc_info())

    def log_exception(self, typ, value, tb):
        if isinstance(value, HTTPError):
            if value.log_message:
                format = '%d %s: ' + value.log_message
                args = ([value.status_code, self._request_summary()] + list(value.args))
                access_log.warning(format, *args)

        access_log.error('Exception: %s\n%s\n%r', self._request_summary(), 
                         self.request, self.request.arguments, 
                         exc_info=(typ, value, tb))
    

    def render_exception(self, ex):
        self.set_status(ex.status_code)
        self.render('error.html', Code=ex.status_code, Msg=ex.reason)

    def render_json_response(self, **kwargs):
        '''
            Encode dict and return response to client
        '''
        callback = self.get_argument('callback', None)
        if callback:
            # return jsonp
            self.set_status(200, kwargs.get('Msg', None))
            self.finish('{}({})'.format(callback, json_encoder(kwargs)))
        else:
            self.set_status(kwargs['Code'], kwargs.get('Msg', None))
            self.set_header('Content-Type', 'application/json;charset=utf-8')
            self.finish(json_encoder(kwargs))

    def prepare(self):
        '''
            check client paltform
        '''
        self.agent_str = self.request.headers.get('User-Agent', '')
        self.agent = None
        self.is_mobile = False
        self.task_resp = None
        
        # check app & os info 
        self.check_app()
        
        if self.agent_str:
            try:
                self.agent = user_agents.parse(self.agent_str)
                self.is_mobile = self.agent.is_mobile
                self.brand = self.agent.device.brand if self.agent.device.brand else 'Other'
            except:
                # assume user platfrom is mobile
                self.is_mobile = True
                self.brand = 'Other'


    def check_app(self):
        '''
        '''
        name = '\xe8\x87\xaa\xe8\xb4\xb8\xe9\x80\x9a'
        if name in self.agent_str:
            self.is_mobile = True
            # if self.agent_str.find('Android'):
            #     self.agent['os'] = {'family':'Android'}
            # else:
            #     self.agent['os'] = {'family':'IOS'}

    def b64encode(self, **kwargs):
        '''
            use base64 to encode kwargs
            the end of b64 : '' | '=' | '==' 
        '''
        arguments = copy.copy(kwargs)
        arguments.pop('firsturl', '')
        arguments.pop('urlparam', '')
        data = utility.b64encode(json_encoder(arguments))
        if data[-2] == '=':
            data = data[:-2] + '_2'
        elif data[-1] == '=':
            data = data[:-1] + '_1'
        else:
            data = data + '_0'
        return data

    def b64decode(self, data):
        '''
            decode data to dict
            data : bdata_number
        '''
        bdata, nums = data.split('_')
        nums = int(nums, 10)
        if nums == 2:
            bdata = bdata + '=='
        elif nums == 1:
            bdata = bdata + '='

        return json_decoder(utility.b64decode(bdata))

def _parse_body(method):
    '''
        Framework only parse body content as arguments 
        like request POST, PUT method.
        Through this method parameters can be send in uri or
        in body not matter request methods(contain 'GET', 'DELETE')
    '''
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        content_type = self.request.headers.get('Content-Type', '')

        # parse json format arguments in request body content
        if content_type.startswith('application/json') and self.request.body:
            arguments = json_decoder(tornado.escape.native_str(self.request.body))
            # logger.info('arguments: {}'.format(arguments))
            for name, values in arguments.iteritems():
                if isinstance(values, basestring):
                    values = [values, ]
                elif isinstance(values, int):
                    values = [str(values), ]
                elif isinstance(values, float):
                    values = [str(values), ]
                elif values:
                    values = [v for v in values if v]

                if values:
                    self.request.arguments.setdefault(name, []).extend(values)
        
        # parse body if request's method not in (PUT, POST, PATCH)
        if self.request.method not in ('PUT', 'PATCH', 'POST'):
            if content_type.startswith('application/x-www-form-urlencode'):
                arguments = tornado.escape.parse_qs_bytes(
                    tornado.escape.native_str(self.request.body))
                for name, values in arguments.iteritems():
                    values = [v for v in values if v]
                    if values:
                        self.request.arguments.setdefault(name, []).extend(values)
            elif content_type.startswith('multipart/form-data'):
                fields = content_type.split(';')
                for field in fields:
                    k, sep, v = field.strip().partition('=')
                    if k == 'boundary' and v:
                        tornado.httputil.parse_multipart_form_data(
                            tornado.escape.utf8(v), self.request.body, 
                            self.request.arguments, self.request.files)
                        break
                    else:
                        access_log.warning('Invalid multipart/form-data')
        return method(self, *args, **kwargs)
    return wrapper

def _trace_wrapper(method):
    '''
        Decorate method to trace logging and exception.
        Remarks : to make sure except catch and progress record
        _trace_wrapper should be the first decorator if a method
        is decorated by multiple decorators.
    '''
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        try:
            access_log.info('<-- In %s: <%s> -->', self.__class__.__name__, self.request.method)
            return method(self, *args, **kwargs)
        except HTTPError as ex:
            access_log.error('HTTPError catch', exc_info=True)
            raise
        except KeyError as ex:
            if self.application.settings.get('debug', False):
                print(self.request)
            access_log.error('Arguments error', exc_info=True)
            raise HTTPError(400)
        except ValueError as ex:
            if self.application.settings.get('debug', False):
                print(self.request)
            access_log.error('Arguments value abnormal', exc_info=True)
            raise HTTPError(400)
        except Exception:
            # Only catch normal exceptions
            # exclude SystemExit, KeyboardInterrupt, GeneratorExit
            access_log.error('Unknow error', exc_info=True)
            raise HTTPError(500)
        finally:
            access_log.info('<-- Out %s: <%s> -->\n\n', self.__class__.__name__, self.request.method)
    return wrapper

def _check_token(method):
    '''
        check user & token
    '''
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        user = self.get_argument('user') 
        if not user:
            raise HTTPError(400, reason='account can\'t be null')
        token = self.get_argument('token')

        token, expired = token.split('|')
        token2 = utility.token2(user, expired)
        if token != token2:
            raise HTTPError(400, reason='Abnormal token')

        return method(self, *args, **kwargs)
    return wrapper

class TestHandler(BaseHandler):
    '''
    '''
    # def get(self):
    #     self.render_json_response(Code=200, Msg='OK')
    # @tornado.gen.coroutine
    # def get(self):
    #     print('in : {}'.format(self.request))

    #     return 'Success'

    #     try:
    #         response = yield template.get_portal('10001', 'h5') 
    #     except template.PortalConfig as portal_config:
    #         access_log.info('portal_config: {}'.format(portal_config.value), exc_info=True)
    #         print(portal_config.value)
    #     except:
    #         access_log.info('exception', exc_info=True)

    #     
    #     self.render_json_response(Code=200, Msg='OK')

    @tornado.gen.coroutine
    def get(self):
        access_log.info('hello world')
        response = yield tornado.gen.Task(portal.add.apply_async, args=[3,5], expires=20)
        access_log.info('response: %s', response)
        self.finish('Success')

class PageHandler(BaseHandler):
    '''
    '''
    _WX_IP = 'api.weixin.qq.com'


    @_parse_body
    @tornado.gen.coroutine
    def get(self, page):
        '''
            Render html page
        '''
        # logger.info(self.request)
        page = page.lower()

        if page in ('nagivation.html', 'niot.html', 'help.html'):
            self.render(page)
            return

        if page not in ('login.html'):
            self.redirect_to_bidong()
            return

        kwargs = {}
        accept = self.request.headers.get('Accept', 'text/html')

        kwargs['ac_ip'] = self.get_argument('nasip', '') or self.get_argument('wlanacip', '') or self.get_argument('wip', '')
        if not kwargs['ac_ip']:
            access_log.error('can\'t found ac parameter, please check ac url configuration')
            self.redirect_to_bidong()
            return

        self.parse_ac_parameters(kwargs)

        url = kwargs['firsturl']
        
        self.profile, self.ap_groups = account.get_billing_policy(kwargs['ac_ip'], kwargs['ap_mac'], kwargs['ssid'])

        if (not kwargs['ap_mac']) and kwargs['ssid'] != self.profile['ssid']:
            kwargs['ssid'] = self.profile['ssid']

        # process weixin argument
        self.prepare_wx_wifi(**kwargs)
        
        # get portal profile
        # if kwargs['ac_ip'] not in ('172.201.2.252', '172.201.2.251'):
        #     try:
        #         platform = 'h5' if self.is_mobile else 'pc'
        #         response = yield template.get_portal(str(self.profile['pn']), platform) 
        #     except template.PortalConfig as portal_config:
        #         portal_config = portal_config.value
        #         if portal_config['mask'] not in (1, 2):
        #             self.profile['portal'] = portal_config['config']
        #     except:
        #         pass

        if self.profile['pn'] in (55532, ) or (not AC_CONFIGURE[kwargs['ac_ip']]['mask'] & 2): 
            # ac doesn't support mac auth, need portal do it 
            result = yield self.login_auto_by_mac(**kwargs)

            if self.task_resp is None:
                pass
            else:
                _user, self.task_resp = self.task_resp.result, None
                if _user:
                    self._add_online_by_bas(kwargs['ac_ip'], kwargs['ap_mac'], 
                                            kwargs['user_mac'], kwargs['user_ip'])
                    yield tornado.gen.sleep(0.2)
                    if accept.startswith('application/json'):
                        token = utility.token(self.user['user'])
                        self.render_json_response(User=self.user['user'], Token=token, Mask=self.user['mask'], 
                                                  Code=200, Msg='OK')
                    elif url:
                        # self.set_header('Access-Control-Allow-Origin', '*')
                        if self.profile['pn'] in (55532, ):
                            self.redirect(self.profile['portal'])
                            return
                        if kwargs['urlparam']:
                            url = ''.join([url, '?', kwargs['urlparam']])
                        self.redirect(url)
                    return 

        if 'wx/m_bidong/onetonet' in url:
            # user from weixin, parse code & and get openid
            if 'MicroMessenger' not in self.agent_str:
                self.render_exception(HTTPError(400, 'Abnormal agent'))
                return

            try:
                response = yield self.wx_login(**kwargs)
            except:
                access_log.error('weixin login failed', exc_info=True)

            if self.task_resp:
                response, self.task_resp = self.task_resp, None
                if response.status in ('SUCCESS', ):
                    _user = response.result
                elif isinstance(response.result, HTTPError) and response.result.status_code in (440,):
                    _user = self.user
                else:
                    access_log.info('weixin auth failed, {}'.format(response.result))
                    _user = None

                if _user:
                    # login successfully
                    # redirect to account page
                    _user = response.result
                    token = utility.token(_user['user'])
                    self.redirect(config['bidong'] + 'account/{}?token={}'.format(self.user['user'], token))
                    
                    if self.profile:
                        account.update_mac_record(self.user['user'], kwargs['user_mac'],
                                                  self.profile['duration'], self.agent_str, self.brand, self.profile)

                    return

        # get policy
        kwargs['user'] = ''
        kwargs['password'] = ''
        if self.profile['_location'].startswith('318922'): 
            kwargs['user'] = '55532'
            kwargs['password'] = '987012'

        # render portal page
        self.render_portal(self.is_mobile, accept, self.profile, self.ap_groups, self.wx_wifi, **kwargs)


    def render_portal(self, platform, accept, profile, ap_groups, wx_config, **kwargs):
        # render json response to app
        if accept.startswith('application/json'):
            self.render_json_response(Code=200, Msg='OK', openid='', pn_ssid=profile['ssid'], 
                                      pn_note=profile['note'], pn_logo=profile['logo'],  
                                      ispri=profile['policy'] & 2, pn=profile['pn'], 
                                      note=profile['note'], image=profile['logo'], 
                                      logo=profile['logo'], **kwargs)
            return

        if isinstance(profile['portal'], basestring) and not profile['portal'].endswith('.html'):
            # query portal template profile
            results = account.get_portal_tmp(profile['portal'])
            if results:
                portal_tmp = results[0]
                profile['portal'] = portal_tmp
                # pic = portal_tmp['h5_pic'] if platform else portal_tmp['pc_pic']
                # profile['portal'] = {'title':portal_tmp['title'], 'pic':pic}
            else:
                profile['portal'] = 'login.html'

        # now all page user login, later after update back to use self.profile['portal']  
        if isinstance(profile['portal'], dict):
            page = 'tplh5.html' if platform else 'tplpc.html'
            portal_tmp = profile['portal']
            pic = portal_tmp['h5_pic'] if platform else portal_tmp['pc_pic']
            kwargs['config'] = {'title':portal_tmp['title'], 'pic':pic}
        else:
            page = profile['portal'] or 'login.html'

        self.set_header('CacheControl', 'no-cache')
        self.set_header('Pragma', 'no-cache')
        self.set_header('Expires', '-1')

        groups = profile['_location']
        if '77201' in groups:
            groups = 10003

        access_log.info('pn profile: %s', profile)

        self.render(page, ismobile=platform, openid='', policy=profile['policy'], groups=groups, ap_groups=ap_groups,  
                    pn=profile['pn'], note=profile['note'], image=profile['logo'],  
                    appid=profile['appid'], shopid=profile['shopid'], secret=profile['secret'], 
                    logo=profile['logo'],
                    extend=wx_config['extend'], timestamp=wx_config['timestamp'], 
                    sign=wx_config['sign'], authUrl=wx_config['auth_url'], 
                    **kwargs)


    def parse_ac_parameters(self, kwargs):
        '''
        '''
        if kwargs['ac_ip'] not in AC_CONFIGURE:
            raise HTTPError(400, reason='Unknown AC: {}'.format(kwargs['ac_ip']))

        if not AC_CONFIGURE[kwargs['ac_ip']]['mask'] & 1: 
            # sangfor device
            kwargs['vlan'] = self.get_argument('vlan', 1)
            ssids = self.get_arguments('ssid')
            if not ssids:
                raise HTTPError(400)
            ssid = ssids[-1] if kwargs['ac_ip'] == '172.29.1.246' else ssids[0]
            # ssid = self.get_argument('ssid')
            kwargs['ssid'] = ssid.strip('"')
            
            kwargs['user_ip'] = self.get_argument('wlanuserip', '') or self.get_argument('userip', '')

            # user mac address 
            mac = self.get_argument('mac', '') or self.get_argument('wlanstamac', '') 
            if not mac:
                raise HTTPError(400, reason='mac address can\'t be None')
            kwargs['user_mac'] = utility.format_mac(mac)

            # ap mac address
            # 00:00:00:00:00:00 - can't get ap mac address
            ap_mac = self.get_argument('apmac', '') or self.get_argument('ap_mac', '') or self.get_argument('wlanapmac', '00:00:00:00:00:01')
            kwargs['ap_mac'] = utility.format_mac(ap_mac)

            try:
                kwargs['firsturl'] = self.get_argument('wlanuserfirsturl', '') or self.get_argument('url', '') or self.get_argument('userurl', '')
                kwargs['urlparam'] = self.get_argument('urlparam', '')
            except:
                kwargs['firsturl'] = config['bidong']
                # kwargs['firsturl'] = 'http://wwww.bidongwifi.com/'
                kwargs['urlparam'] = ''
        else:
            # bas mask == 1
            kwargs['vlan'] = ''
            # kwargs['ssid'] = 'BD_TEST'
            kwargs['ssid'] = self.get_argument('ssid', 'BD_TEST')
            kwargs['user_ip'] = self.get_argument('wlanuserip', '') or self.get_argument('userip', '')
            mac = self.get_argument('usermac', '') or self.get_argument('wlanusermac', '')
            kwargs['user_mac'] = utility.format_mac(mac)
            kwargs['ap_mac'] = ''

            kwargs['firsturl'] = self.get_argument('url', '') or self.get_argument('rehost', '') or 'http://www.gzdjy.org/'
            kwargs['urlparam'] = ''

    @tornado.gen.coroutine
    def login_auto_by_mac(self, **kwargs):
        if self.profile['pn'] == 10000:
            # 10000 (test) owner, skip auto login check
            return

        if self.profile['pn'] in (55532, ):
            # all user use holder's account
            _user = {'user':'55532', 'password':'987012', 'mask':10, 'coin':60, 'ends':100}
            self.user = _user
        else:
            _user = account.get_bd_user(kwargs['user_mac'], ismac=True)
            if not _user:
                return

            if account.check_auto_login_expired(_user):
                return

            self.user = _user
            try:
                results = account.check_account_privilege(_user, self.profile)
                if results:
                    name = results['name'] if results['name'] else results['mobile']
                    self.user['name'] = name if name else u''
            except:
                return

            onlines = account.get_onlines(_user['user'])
            if kwargs['user_mac'] not in onlines and len(onlines) >= _user['ends']:
                # allow user logout ends 
                return

        task_id = _user['user'] + '-' + kwargs['user_mac']

        response = yield tornado.gen.Task(portal.login.apply_async, 
                                          args=[_user, kwargs['ac_ip'], kwargs['user_ip'], kwargs['user_mac']], 
                                          expires=20) 
                                          # task_id=task_id)

        if response.status in ('SUCCESS', ):
            access_log.info('{} auto login successfully, mac:{}'.format(_user['user'], kwargs['user_mac']))
            self._add_online_by_bas(kwargs['ac_ip'], kwargs['ap_mac'], kwargs['user_mac'], kwargs['user_ip'])
        elif isinstance(response.result, HTTPError) and response.result.status_code in (440,):
            access_log.info('{} has been authed, mac:{}'.format(_user['user'], kwargs['user_mac']))
        else:
            access_log.info('{} auto login failed, {}'.format(_user['user'], response.result))
            return

        self.task_resp = response
        
    @tornado.gen.coroutine
    def wx_login(self, **kwargs):
        if kwargs['urlparam']:
            urlparam = parse_qs('urlparam='+kwargs['urlparam'])
            params = parse_qs(urlparam['urlparam'][0])
            code = params['code'][0]
        else:
            code = self.parse_url_arguments(kwargs['firsturl'])['code'] 

        URL = 'https://{}/sns/oauth2/access_token?appid={}&secret={}&code={}&grant_type=authorization_code'
        url = URL.format(self._WX_IP, config['weixin']['appid'], config['weixin']['secret'], code)
        client = tornado.httpclient.AsyncHTTPClient()
        response = yield client.fetch(url)

        if response.error:
            raise response

        result = json_decoder(response.body)
        if 'openid' not in result:
            access_log.error('Get weixin account\'s openid failed, msg: {}'.format(result))
            raise HTTPError(400)

        openid =  result['openid']

        access_log.info('openid: {} login by weixin'.format(openid))
        user, password = '', ''
        # _user = account.check_weixin_user(openid, appid=self.profile['appid'], mac=kwargs['user_mac'])
        _user = account.get_weixin_user(openid, self.profile['appid'], '', kwargs['user_mac'])
        if not _user:
            raise HTTPError(432)

        self.user = _user
        # user unsubscribe, the account will be forbid
        if _user['mask']>>31 & 1:
            raise HTTPError(431)
            
        # check ac ip
        if kwargs['ac_ip'] not in AC_CONFIGURE:
            access_log.error('not avaiable ac & ap')
            raise HTTPError(400, reason='Unknown AC,ip : {}'.format(kwargs['ac_ip']))

        results = account.check_account_privilege(self.user, self.profile)
        if results:
            name = results['name'] if results['name'] else results['mobile']
            self.user['name'] = name if name else u''

        task_id = self.user['user'] + '-' + kwargs['user_mac']
        response = yield tornado.gen.Task(portal.login.apply_async, 
                                          args=[self.user, kwargs['ac_ip'], 
                                                kwargs['user_ip'], kwargs['user_mac']], 
                                          expires=20) 
                                          # task_id=task_id)

        if response.status in ('SUCCESS', ):
            access_log.info('{} weixin login successfully, mac:{}'.format(self.user['user'], kwargs['user_mac']))
        elif isinstance(response.result, HTTPError) and response.result.status_code in (440,):
            access_log.info('{} has been authed, mac:{}'.format(self.user['user'], kwargs['user_mac']))
        else:
            access_log.info('{}auto login failed, {}'.format(self.user['user'], response.result))
            return

        self.task_resp = response


    def timeout(self, sock, ac_ip, header, user_mac):
        '''
        '''
        access_log.info('ip: %s timeout', self.request.remote_ip)
        portal.timeout(sock, ac_ip, header, user_mac)

    def calc_sign(self, *args):
        '''
            sign = md5(appid, extend,timestamp, shop_id, authUrl, 
                       mac, ssid, bssid, secretkey) 
        '''
        data = ''.join(args)
        return utility.md5(data).hexdigest()

    def redirect_to_bidong(self):
        '''
        '''
        access_log.info('redirect : {}'.format(self.request.arguments))
        self.redirect(config['bidong'])
        # self.finish()

    def prepare_wx_wifi(self, **kwargs):
        wx_wifi = {}
        wx_wifi['extend'] = self.b64encode(appid=self.profile['appid'], shopid=self.profile['shopid'], **kwargs)
        wx_wifi['timestamp'] = str(int(time.time()*1000))

        portal_server = 'http://{}/wx_auth'.format(self.request.headers.get('Host'))
        
        # wx_wifi['auth_url'] = tornado.escape.url_escape(portal_server)
        wx_wifi['auth_url'] = portal_server
        wx_wifi['sign'] = self.calc_sign(self.profile['appid'], wx_wifi['extend'], wx_wifi['timestamp'], 
                                         self.profile['shopid'], wx_wifi['auth_url'], 
                                         kwargs['user_mac'], self.profile['ssid'], kwargs['ap_mac'], 
                                         self.profile['secret'])

        self.wx_wifi = wx_wifi


    def parse_url_arguments(self, url):
        '''
        '''
        arguments = {}
        if url.find('?') != -1:
            url, params = url.split('?')
            items = params.split('&')

            for item in items:
                key, value = item.split('=')
                arguments[key] = value

        return arguments

    def get_openid(self, code):
        URL = 'https://{}/sns/oauth2/access_token?appid={}&secret={}&code={}&grant_type=authorization_code'
        url = URL.format(self._WX_IP, config['weixin']['appid'], config['weixin']['secret'], code)
        client = tornado.httpclient.HTTPClient()
        response = client.fetch(url)
        result = json_decoder(response.body)
        if 'openid' not in result:
            access_log.error('Get weixin account\'s openid failed, msg: {}'.format(result))
            raise HTTPError(500)

        return result['openid']

    def _add_online_by_bas(self, nas_addr, ap_mac, mac_addr, user_ip):
        '''
            if bas's mask & 1, add online record
            sangfor doesn't support accounting package (Radius, AccountRequest)
        '''
        if AC_CONFIGURE[nas_addr]['mask'] & 4:
            # bas is sangfor 
            try:
                account.add_online2(self.user['user'], nas_addr, ap_mac, mac_addr, user_ip,
                                    self.profile['_location'], self.profile['ssid'])
            except:
                access_log.error('add {} online failed, mac: {}'.format(self.user['user'], mac_addr), exc_info=True)

class PortalHandler(BaseHandler):
    '''
        Handler portal auth request
    '''
    def prepare(self):
        '''
            is_weixin : weixin ends
            is_third : third app 
                third app: see ad page
        '''
        super(PortalHandler, self).prepare()
        self.is_weixin = False
        self.is_third = False
        self.response_kwargs = {}
        self.token = None

    def write_error(self, status_code, **kwargs):
        '''
            Customer error return format
        '''
        if self.settings.get('Debug') and 'exc_info' in kwargs:
            self.set_header('Content-Type', 'text/plain')
            import traceback
            for line in traceback.format_exception(*kwargs['exc_info']):
                self.write(line)
            self.finish()
        else:
            responses = {'Code':status_code, 'Msg':self.RESPONSES.get(status_code, 'Unknown Error').decode('utf-8')} 
            if status_code in (428, ):
                downmacs = 0 
                if self.profile['pn'] in (15914, 59484):
                    downmacs = 1
                responses['downMacs'] = downmacs
                responses['macs'] = self.response_kwargs.get('macs', '')
            
            if self.token:
                responses['Token'] = self.token

            profile = getattr(self, 'profile', None)
            if profile:
                responses['pn'] = profile['pn']
                responses['ssid'] = profile['ssid']

            self.render_json_response(**responses)

    def _check_app_sign(self):
        '''
            check appid's sign if request arguments contains {appid:'', sign:''}
        '''
        appid = self.get_argument('appid', '')
        kwargs = {key:value[0] for key,value in self.request.arguments.iteritems()}
        sign = kwargs.pop('sign', '')
        if appid and sign:
            record = account.get_appid(appid)
            # kwargs['appkey'] = record['appkey']
            data = u'&'.join([u'{}={}'.format(key, kwargs[key]) for key in sorted(kwargs.keys())])
            data = data + u'&appkey={}'.format(record['appkey'])
            access_log.info('data: {}'.format(data))

            md5 = utility.md5(data.encode('utf-8')).hexdigest()
            if sign != md5:
                raise HTTPError(400, reason='app sign check failed')


    # @_trace_wrapper
    @_parse_body
    @tornado.gen.coroutine
    def get(self):
        try:
            tid = self.get_argument('tid')
            openid = self.get_argument('openId')
        except tornado.web.MissingArgumentError as e: 
            user = (u'default',u'')
            token = utility.token(str(time.time()))
            return self.render_json_response(Code=200,Msg='OK',user=user,token=token)
        extend = self.get_argument('extend')

        access_log.info('openid:{}, tid: {}'.format(openid, tid))

        kwargs = self.b64decode(extend)
        ac_ip = kwargs['ac_ip']
        # check ac ip
        if ac_ip not in AC_CONFIGURE:
            access_log.error('not avaiable ac & ap')
            raise HTTPError(400, reason='AC ip error')

        ap_mac = kwargs['ap_mac']
        user_mac = kwargs['user_mac']
        user_ip = kwargs['user_ip']

        user, password = '',''

        record = account.get_online2(ac_ip, user_mac)
        if not record:
            access_log.warning('cant\'t found online record: %s, %s', ac_ip, user_mac)
            _user = (openid, kwargs['appid'])
            # _user = account.check_weixin_user(openid, appid=kwargs['appid'], tid=tid, mac=user_mac)
            # if not _user:
            #     raise HTTPError(432)
        else:
            _user = account.check_weixin_user(record['user'], user_mac, openid, appid=kwargs['appid'], tid=tid)

            # update online records
        
        self.user = _user

        # # vlanId = self.get_argument('vlan')
        # ssid = kwargs['ssid']
        # self.profile, self.ap_groups = account.get_billing_policy(ac_ip, ap_mac, ssid)

        # # check account privilege
        # results = account.check_account_privilege(self.user, self.profile)
        # if results:
        #     name = results['name'] if results['name'] else results['mobile']
        #     self.user['name'] = name if name else u''

        # task_id = self.user['user'] + '-' + user_mac
        # 
        # response = yield tornado.gen.Task(portal.login.apply_async, 
        #                                   args=[self.user,  ac_ip, user_ip, user_mac], 
        #                                   expires=30) 
        #                                   # task_id=task_id)

        # if response.successful() and self.profile:
        #     # login successfully 
        #     self._add_online_by_bas(ac_ip, ap_mac, user_mac, user_ip)
        #     account.update_mac_record(self.user['user'], user_mac, 
        #                               self.profile['duration'], self.agent_str, self.profile)
        #     yield tornado.gen.sleep(0.2)
        # else:
        #     if isinstance(response.result, HTTPError) and response.result.status_code in (440, ):
        #         # has been authed
        #         pass
        #     else:
        #         access_log.error('Auth failed, {}'.format(response.traceback))
        #         raise response.result
        # 
        # token = utility.token(self.user['user'])
        # 
        # if 'WeChat' not in self.agent_str:
        #     # auth by other pc 
        #     self.redirect(config['bidong'] + 'account/{}?token={}'.format(self.user['user'], token))
        # else:
        #     self.render_json_response(Code=200, Msg='OK', user=self.user['user'], token=token)
        access_log.info('%s login successfully, ip: %s', self.user, self.request.remote_ip)

    # @_trace_wrapper
    @_parse_body
    @tornado.gen.coroutine
    def post(self):
        # first check app sign
        self._check_app_sign()

        user = self.get_argument('user', '')
        password = self.get_argument('password', '')
        _user = None

        ac_ip = self.get_argument('ac_ip')
        # check ac ip
        if ac_ip not in AC_CONFIGURE:
            access_log.error('not avaiable ac: {}'.format(ac_ip))
            raise HTTPError(400, reason='AC ip error')

        ap_mac = self.get_argument('ap_mac')
        user_mac = self.get_argument('user_mac')
        user_ip = self.get_argument('user_ip')

        if user_ip != self.request.remote_ip:
            access_log.warning('user ip conflict: user_ip: {}, remote_ip: {}'.format(user_ip, self.request.remote_ip))
                # user_ip = self.request.remote_ip

        # vlanId = self.get_argument('vlan')
        ssid = self.get_argument('ssid')
        self.profile, self.ap_groups = account.get_billing_policy(ac_ip, ap_mac, ssid)

        wx = self.get_argument('wx', 0)
        if wx:
            # check account ,if not existed,create new accout by mac
            _user = account.check_account_by_mac(user_mac)
            user, password = _user['user'], _user['password']
        else:
            _user = account.get_bd_user(user, ismac=False)

        if not _user:
            access_log.warning('can\'t found user, user: {}, pwd_{}'.format(user, 
                                                                            ''.join([utility.generate_password(3), password])))
            raise HTTPError(430)

        self.user = _user

        if password not in (_user['password'], utility.md5(_user['password']).hexdigest()):
            # password or user account error
            access_log.error('{} password error, pwd_{}'.format(_user['user'], 
                                                                ''.join([utility.generate_password(3), password])))
            raise HTTPError(430)

        self.token = utility.token(self.user['user'])

        # check account privilege, results: {mask, mobile, name}
        results = account.check_account_privilege(self.user, self.profile)

        if results:
            name = results['name'] if results['name'] else results['mobile']
            self.user['name'] = name if name else u''

        onlines = account.get_onlines(self.user['user'])
        if user_mac not in onlines and len(onlines) >= self.user['ends']:
        # if self.user['user'] == '10001':
            # allow user login ends 
            access_log.warning('{} exceed ends: {}'.format(self.user['user'], self.user['ends']))
            macs = ','.join(onlines)
            self.response_kwargs['macs'] = macs.encode('utf-8')
            raise HTTPError(428)

        task_id = self.user['user'] + '-' + user_mac

        response = yield tornado.gen.Task(portal.login.apply_async, 
                                          args=[self.user,  ac_ip, user_ip, user_mac], 
                                          expires=20) 

        access_log.info('response: %s', response)
                                          # task_id=task_id)

        if response.status in ('SUCCESS', ) and self.profile:
            # login successfully 
            self._add_online_by_bas(ac_ip, ap_mac, user_mac, user_ip)
            account.update_mac_record(self.user['user'], user_mac,
                                      self.profile['duration'], self.agent_str, self.brand, self.profile)
            yield tornado.gen.sleep(0.5)
        else:
            if isinstance(response.result, HTTPError) and response.result.status_code in (440, ):
                access_log.info('user:{} has been authed'.format(self.user['user']))
                # has been authed
                pass
            else:
                access_log.info('user:{}, pwd_{}'.format(self.user['user'], 
                                                      ''.join([utility.generate_password(3), self.user['password']])))
                access_log.error('Auth failed, {}'.format(response.traceback))
                
                raise response.result 

        self.render_json_response(User=self.user['user'], Token=self.token, 
                                  pn=self.profile['pn'], ssid=self.profile['ssid'], 
                                  location=self.profile['_location'],
                                  Code=200, Msg='OK')

        access_log.info('%s login successfully, ip: %s', self.user['user'], self.request.remote_ip)

    @_parse_body
    def delete(self):
        '''
            user logout, portal server send REQ_LOGOUT request to AC, AC return ACK_LOGOUT
            admin revoke user privilege: {manager:'',token:'',user:''}
            user send logout request: {'user':'', token:''}

        '''
        user = self.get_argument('user')
        mac = self.get_argument('mac', '')
        macs = self.get_argument('macs', '')

        macs = macs if macs else mac
        if not macs:
            self.render_json_response(Code=200, Msg='OK')

        macs = macs.split(',')

        onlines = account.get_onlines(user, macs, onlymac=False)
        access_log.info('user:{} online devices: {}, onlines:{}'.format(user, macs, onlines))
        for online in onlines:
            if online['nas_addr'] and online['framed_ipaddr']:
                # portal.logout.delay(online['nas_addr'], online['framed_ipaddr'], mac)
                portal.logout.apply_async((online['nas_addr'], online['framed_ipaddr'], mac), expires=5)
                # account.del_online2(online['nas_addr'], online['mac_addr'])
        if onlines:
            account.clear_user_records(user, macs)

        self.render_json_response(Code=200, Msg='OK')


    def _add_online_by_bas(self, nas_addr, ap_mac, mac_addr, user_ip):
        '''
            if bas's mask & 1, add online record
            if bas's mask & 4, close accounting package
            sangfor doesn't support accounting package (Radius, AccountRequest)
        '''
        if AC_CONFIGURE[nas_addr]['mask'] & 4:
            # bas is gateway or close accounting package
            # portal manage client online & offline
            try:
                account.add_online2(self.user['user'], nas_addr, ap_mac, mac_addr, user_ip,
                                    self.profile['_location'], self.profile['ssid'])
            except:
                access_log.error('add {} online failed, mac: {}'.format(self.user['user'], mac_addr), exc_info=True)

class UserHandler(BaseHandler):
    def check_token(self, user, token):
        token,expired = token.split('|')
        token2 = utility.token2(user, expired)
        if token != token2:
            raise HTTPError(400, reason='Abnormal token')

    def get(self, user):
        '''
        '''
        token = self.get_argument('token')
        self.check_token(user, token)
        # check token
        pn = self.get_argument('pn')
        ssid = self.get_argument('ssid', 'Bidong')
        # mac = self.get_argument('mac')
        code = int(self.get_argument('code'))
        _user = account.get_bd_user(user, ismac=False)
        if not _user:
            raise HTTPError(404)
        # days,hours = utility.format_left_time(_user['expired'], _user['coin'])
        # exchange time
        ex_hours = int(_user['coin']/60)
        msg = self.RESPONSES[code]

        self.render('pay.html', ex_hours=ex_hours, 
                    photo='', code=code, ssid=ssid, 
                    msg=msg.decode('utf-8'), **_user)

class PnHandler(BaseHandler):
    def get(self, pn):
        name = self.get_argument('name')
        mobile = self.get_argument('mobile')
        # pn = self.get_argument('pn')
        # query user
        record = account.get_pn_user(pn, name, mobile)
        if not record:
            raise HTTPError(404, reason=u'can\'t found pn:{} user: {},{}'.format(pn, name, mobile))

        # check account, if not create
        # user = account.check_pn_account_by_mobile(mobile, pn)
        # access_log.info('user: {}'.format(user))

        self.render_json_response(department=record['department'], 
                                  # user=user['user'], password=user['password'], 
                                  Code=200, Msg='OK')

EXPIRE = 7200

_DEFAULT_BACKLOG = 128
# These errnos indicate that a non-blocking operation must be retried
# at a later time. On most paltforms they're the same value, but on 
# some they differ
_ERRNO_WOULDBLOCK = (errno.EWOULDBLOCK, errno.EAGAIN)
if hasattr(errno, 'WSAEWOULDBLOCK'):
    _ERRNO_WOULDBLOCK += (errno.WSAEWOULDBLOCK, )

def bind_udp_socket(port, address=None, family=socket.AF_UNSPEC, backlog=_DEFAULT_BACKLOG, flags=None):
    '''
    '''
    udp_sockets = []
    if address == '':
        address = None
    if not socket.has_ipv6 and family == socket.AF_UNSPEC:
        family = socket.AF_INET
    if flags is None:
        flags = socket.AI_PASSIVE
    bound_port = None
    for res in socket.getaddrinfo(address, port, family, socket.SOCK_DGRAM, 0, flags):
        af, socktype, proto, canonname, sockaddr = res
        try:
            sock = socket.socket(af, socktype, proto)
        except socket.error as e:
            if errno_from_exception(e) == errno.EAFNOSUPPORT:
                continue
            raise
        set_close_exec(sock.fileno())
        if os.name != 'nt':
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        if af == socket.AF_INET6:
            if hasattr(socket, 'IPPROTO_IPV6'):
                sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 1)

        # automatic port allocation with port=None
        # should bind on the same port on IPv4 & IPv6 
        host, requested_port = sockaddr[:2]
        if requested_port == 0 and bound_port is not None:
            sockaddr = tuple([host, bound_port] + list(sockaddr[2:]))
        sock.setblocking(0)
        sock.bind(sockaddr)
        bound_port = sock.getsockname()[1]
        udp_sockets.append(sock)
    return udp_sockets

def add_udp_handler(sock, servers, io_loop=None):
    '''
        Read data in 4096 buffer
    '''
    if io_loop is None:
        io_loop = tornado.ioloop.IOLoop.current()
    def udp_handler(fd, events):
        while True:
            try:
                data, addr = sock.recvfrom(4096)
                if data:
                    ac_data_handler(sock, data, addr)
                    # ac data arrived, deal with
                    pass
            except socket.error as e:
                if errno_from_exception(e) in _ERRNO_WOULDBLOCK:
                    # _ERRNO_WOULDBLOCK indicate we have accepted every
                    # connection that is avaiable
                    return
                import traceback
                traceback.print_exc(file=sys.stdout)
            except: 
                import traceback
                traceback.print_exc(file=sys.stdout)
    io_loop.add_handler(sock.fileno(), udp_handler, tornado.ioloop.IOLoop.READ)

def ac_data_handler(sock, data, addr):
    '''
        User logout
    '''
    # parse data, get ntf_logout packet
    # query online db by mac_addr

    # send 
    access_log.info('Receive data from {}: message type {:02X}'.format(addr, ord(data[1])))
    header = portal.Header.unpack(data)
    if header.type == 0x08:
        # ac notify portal, user logout
        # data = '\x01\x07' + data[2:]

        if True:
            start = 32 if header.ver == 0x02 else 16
            attrs = portal.Attributes.unpack(header.num, data[start:])
            if not attrs.mac:
                user_ip = socket.inet_ntoa(header.ip)
                access_log.info('User quit, nas_addr: {}, ip: {}'.format(addr[0], user_ip))
                # if addr[0] in ('172.201.2.252', '172.201.2.251'):
                account.del_online3(addr[0], user_ip)
                # portal.ack_logout.delay(addr[0], user_ip, '00:11:22:33:44:55:66', header.serial)
                portal.ack_logout.apply_async((addr[0], user_ip, '00:11:22:33:44:55:66', header.serial), expires=5)
                return
            #
            mac = []
            for b in attrs.mac:
                mac.append('{:02X}'.format(ord(b)))
            mac = ':'.join(mac)

            if addr[0] in AC_CONFIGURE and AC_CONFIGURE[addr[0]]['mask'] & 4:
                # receive logout request from 
                access_log.info('Portal delete user, nas_addr: {}, mac: {}'.format(addr[0], mac))
                account.del_online2(addr[0], mac)

    elif header.type == 0x30:
        #
        start = 32 if header.ver == 0x02 else 16
        attrs = portal.Attributes.unpack(header.num, data[start:])
        user_mac = attrs.extend.get('mac', '')
        # ac_ip = attrs.extend.get('ac_ip', '')
        ac_ip = addr[0]
        ssid = attrs.extend.get('ssid', 'GDFS')
        if user_mac and ac_ip:
            mac = []
            for b in user_mac:
                mac.append('{:02X}'.format(ord(b)))
            mac = ':'.join(mac)

            # ac_ip = socket.inet_ntoa(ac_ip)
            user_ip = socket.inet_ntoa(header.ip)

            # if ac_ip in ('172.16.0.252',):
            try:
                # if ac_ip in h3c_ac, deal with 0x30
                user = account.get_bd_user(mac, True)
                if user:
                    profile, ap_groups = account.get_billing_policy(ac_ip, '', ssid)
                    existed = True
                    results = {}

                    try:
                        results = account.check_account_privilege(user, profile)
                    except:
                        existed = False

                    onlines = account.get_onlines(user['user'])
                    if user_mac not in onlines and len(onlines) >= user['ends']:
                        existed = False

                    if results:
                        name = results['name'] if results['name'] else results['mobile']
                        user['name'] = name if name else u''

                    # check auto_login expired
                    # check account privilege
                    if existed and account.check_auto_login_expired(user):
                        access_log.info('{} auto login expired'.format(user['user']))
                        existed = False

                    access_log.info('h3c auto login: ac_ip:{}, mac:{}, existed:{}'.format(ac_ip, mac, existed))
                    # portal.mac_existed.delay(user, ac_ip, header.ip, mac, header.serial, existed)
                    portal.mac_existed.apply_async((user, ac_ip, header.ip, mac, header.serial, existed), expires=30)
            except:
                access_log.error('h3c auto login failed!', exc_info=True)
    elif header.type == 0x32:
        start = 32 if header.ver == 0x02 else 16
        attrs = portal.Attributes.unpack(header.num, data[start:])
        user_mac = attrs.extend.get('mac', '')
        ac_ip = attrs.extend.get('ac_ip', '')
        ssid = attrs.extend.get('ssid', 'GDFS')
        existed = False
        ac_ip = socket.inet_ntoa(ac_ip)
        # user auto login successfully
        name = attrs.user 
        name = name.split(' (')[0]
        mac = []
        for b in user_mac:
            mac.append('{:02X}'.format(ord(b)))
        mac = ':'.join(mac)
        user_ip = socket.inet_ntoa(header.ip)
        profile, ap_groups = account.get_billing_policy(ac_ip, '', ssid)

        access_log.info('h3c {} auto login notify, mac:{}, {}'.format(name, mac, user_ip))
        account.add_online2(name, ac_ip, '', mac, user_ip, profile['_location'], ssid)
    elif header.type == 0x34:
        start = 32 if header.ver == 0x02 else 16
        attrs = portal.Attributes.unpack(header.num, data[start:])
        user_mac = attrs.extend.get('mac', '')
        ac_ip = attrs.extend.get('ac_ip', '')
        ssid = attrs.extend.get('ssid', 'GDFS')
        if user_mac and ac_ip:
            mac = []
            for b in user_mac:
                mac.append('{:02X}'.format(ord(b)))
            mac = ':'.join(mac)

            name = attrs.user 
            name = name.split(' (')[0]

            ac_ip = socket.inet_ntoa(ac_ip)
            user_ip = socket.inet_ntoa(header.ip)

            access_log.info('Portal delete user: {}, nas_addr: {}, mac: {}, {}'.format(name, ac_ip, mac, user_ip))
            account.del_online2(ac_ip, mac)

def get_bas():
    global AC_CONFIGURE
    results = account.list_bas()
    AC_CONFIGURE = {item['ip']:item for item in results}

def main():
    import tornado.options
    define, options = tornado.options.define, tornado.options.options

    define('port', default=8880, help='running on the given port', type=int)
    define('index', default=0, help='portal start index, used for serial number range', type=int)
    define('total', default=1, help='portal server total number , used for serial number range', type=int)
    define('udp_listen', default=0, help='portal server listen on 50100? 1 : 0', type=int)
    define('portal_listen', default=50100, help='portal server listening port', type=int)

    # log configuration
    tornado.options.parse_command_line(final=False)
    define('log_rotate_mode', type=str, default='time', help='time or size')
    define('log_file_num_backups', type=int, default=3, help='number of log files to keep')
    define('log_file_prefix', type=str, default=os.path.join(config['log_path'], 'portal/{}.log'.format(options.port)))
    options.run_parse_callbacks()

    # init_log(config['log_folder'], config['logging_config'], options.port)

    portal_pid = os.path.join(config['pid_path'], 'portal/p_{}.pid'.format(options.port))
    with open(portal_pid, 'w') as f:
        f.write('{}'.format(os.getpid()))

    # initialize portal module
    index, total = options.index, options.total

    step = int(2**16/total) 
    start = index*step


    portal.init(config['portal_config'], None, xrange(start, start+step))

    account.setup(config['database'])

    import tcelery
    
    tcelery.setup_nonblocking_producer()

    # get bas lists
    get_bas()

    app = Application()
    app.listen(options.port, xheaders=app.settings.get('xheaders', False), decompress_request=True)
    io_loop = tornado.ioloop.IOLoop.instance()

    if options.udp_listen:
        udp_sockets = bind_udp_socket(options.portal_listen)
        for udp_sock in udp_sockets:
            add_udp_handler(udp_sock, '', io_loop)

    app_log.info('Portal Server Listening:{} Started'.format(options.port))
    io_loop.start()

if __name__ == '__main__':
    main()
