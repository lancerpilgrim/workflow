import sys
import logging

import tornado.options
from tornado import web
from tornado import httpserver
from tornado.options import options, define

import settings as config
from bidong.core.views import Api404Handler
from bidong.router.platform import routers as mprouters
from bidong.router.project import routers as pnrouters

define('host', default='0.0.0.0', type=str)
define('port', default=8787, type=int, help='run server on given port')
define('serve', type=str, help='which server to serve, platform or project')
define('log_file_num_backups', type=int, default=3,
       help='number of log files to keep')


def make_app(serve):
    if serve == 'platform':
        return web.Application(
            mprouters,
            debug=config.DEBUG,
            xheader=True,
            default_handler_class=Api404Handler,
            cookie_secret=config.COOKIE_SECRET
        )
    elif serve == 'project':
        return web.Application(
            pnrouters,
            debug=config.DEBUG,
            xheader=True,
            default_handler_class=Api404Handler,
            cookie_secret=config.COOKIE_SECRET
        )
    else:
        logging.fatal(
            "Invalid options, only project or platform allow."
            "try python server.py --serve=project(or platform) "
        )
        sys.exit(-1)


def main():
    tornado.options.parse_command_line()
    logging.info('Run bidong-{} server on {}:{}'.format(
        options.serve, options.host, options.port))

    app = make_app(options.serve)
    http_server = httpserver.HTTPServer(app)
    http_server.listen(options.port, options.host)
    loop = tornado.ioloop.IOLoop.instance()
    loop.start()


if __name__ == "__main__":
    main()
