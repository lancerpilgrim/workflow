import random
import uuid

from bidong.core.database import session
from bidong.storage.models import Account, AccountProfile, Dyncol, PNField, Tag
from bidong.storage.models import AP, Online

from tests.view import ApiTestCase, fake


def load_dyncol():
    dyncols = [
        {"col": "company", "label": "公司"},
        {"col": "department", "label": "部门"},
        {"col": "title", "label": "职位"},
        {"col": "email", "label": "邮箱"},
        {"col": "id_number", "label": "身份证号"},
        {"col": "id_images", "label": "身份证照片"},
        {"col": "note", "label": "备注"},
    ]
    for kw in dyncols:
        rv = Dyncol(**kw)
        session.add(rv)
    session.commit()
    return len(dyncols)


def load_pnfile(pn, col_id_list=None, count=None):
    if col_id_list is None:
        cols = session.query(Dyncol).all()
        if count is not None:
            cols = cols[:count]

        col_id_list = [rv.id for rv in cols]

    for col in col_id_list:
        rv = PNField(pn=pn, dyncol_id=col)
        session.add(rv)
    session.commit()
    return col_id_list


def load_tags(pn):
    tags = [
        {"pn": pn, "tag_type": "account", "name": "标签1"},
        {"pn": pn, "tag_type": "account", "name": "标签2"},
        {"pn": pn, "tag_type": "account", "name": "标签3"}
    ]
    for kw in tags:
        t = Tag(**kw)
        session.add(t)
        session.flush()
        kw['id'] = t.id
    session.commit()
    return tags


class CustomAttrApiTestCase(ApiTestCase):
    api = "project"
    url_pattern = '/v1.0/projects/{}/users/custom-attr'

    related_models = [Dyncol, PNField]

    def setUp(self):
        super(CustomAttrApiTestCase, self).setUp()
        self.default_count = load_dyncol()
        self.pn = 12
        self.url = self.url_pattern.format(self.pn)

    def tearDown(self):
        # super(CustomAttrApiTestCase, self).tearDown()
        pass

    def test_get(self):
        resp = self.get(self.url)
        self.assertEqual(resp.code, 200)
        self.assertEqual(len(resp.json['setted']), 0)
        self.assertEqual(len(resp.json['default']), self.default_count)

        col_id_list = [rv.id for rv in session.query(Dyncol).all()[:4]]
        load_pnfile(self.pn, col_id_list)
        resp = self.get(self.url)
        self.assertEqual(resp.code, 200)
        self.assertEqual(len(resp.json['setted']), 4)
        self.assertEqual(len(resp.json['default']), self.default_count)

    def test_post(self):
        resp = self.json_post(self.url, payload={})
        self.assertEqual(resp.code, 400)

        col_id_list = [rv.id for rv in session.query(Dyncol).all()[:4]]
        payload = {"cols": col_id_list}
        resp = self.json_post(self.url, payload=payload)
        self.assertEqual(resp.code, 200)

        count = session.query(PNField).count()
        self.assertEqual(count, 4)

        resp = self.get(self.url)
        self.assertEqual(resp.code, 200)
        self.assertEqual(len(resp.json['setted']), 4)
        self.assertEqual(len(resp.json['default']), self.default_count)


class UserProfileTestCase(ApiTestCase):
    api = "project"
    url_pattern = "/v1.0/projects/{}/users/profiles"
    related_models = [
        Account, AccountProfile, Dyncol, PNField, Tag, AP, Online]

    def setUp(self):
        super(UserProfileTestCase, self).setUp()
        self.pn = 12
        self.url = self.url_pattern.format(self.pn)
        load_dyncol()
        load_pnfile(self.pn)
        load_tags(self.pn)

    def tearDown(self):
        # super(UserProfileTestCase, self).tearDown()
        pass

    def test_create_list_get_and_delete(self):
        resp = self.get("/v1.0/projects/{}/users/custom-attr".format(self.pn))
        self.assertEqual(resp.code, 200)
        setted = resp.json['setted']

        resp = self.get("/v1.0/projects/{}/tags".format(self.pn),
                        query={"type": "account"})
        self.assertEqual(resp.code, 200)
        project_tags = resp.json["tags"]

        attrs = []
        for rv in setted:
            attrs.append({"col": rv["id"], "value": fake.pystr()})
        tags = [rv["id"] for rv in project_tags]

        attrs_count = len(attrs)
        tags_count = len(tags)

        url = self.url_pattern.format(self.pn)

        # this is for create
        payload = {
            "mobile": "15154058701", "name": fake.name(), "attrs": attrs,
            "tags": tags
        }
        resp = self.json_post(self.url, payload=payload)
        self.assertEqual(resp.code, 200)

        payload = {
            "mobile": "15154058702", "name": fake.name(), "attrs": attrs,
            "tags": [],
        }
        resp = self.json_post(self.url, payload=payload)
        self.assertEqual(resp.code, 200)

        payload = {
            "mobile": "15154058703", "name": fake.name(),
            "tags": tags, "attrs": attrs,
        }
        resp = self.json_post(self.url, payload=payload)
        self.assertEqual(resp.code, 200)

        for attr in attrs:
            attr['value'] = ""

        payload = {
            "mobile": "15154058704", "name": fake.name(),
            "tags": tags, "attrs": attrs
        }
        resp = self.json_post(self.url, payload=payload)
        self.assertEqual(resp.code, 200)

        payload = {
            "mobile": "15154058704", "name": fake.name(),
            "tags": tags, "attrs": attrs
        }
        resp = self.json_post(self.url, payload=payload)
        self.assertEqual(resp.code, 409)

        payload = {
            "mobile": "", "name": fake.name(),
            "tags": tags, "attrs": attrs
        }
        resp = self.json_post(self.url, payload=payload)
        self.assertEqual(resp.code, 400)

        # test for list
        resp = self.get(self.url)
        self.assertEqual(resp.code, 200)
        self.assertEqual(resp.json['page'], 1)
        self.assertEqual(resp.json['total_items'], 4)
        self.assertEqual(len(resp.json['objects']), 4)

        project_user_list = []
        for rv in resp.json["objects"]:
            project_user_list.append(rv["id"])

        query = {"page": 20}
        resp = self.get(self.url, query=query)
        self.assertEqual(resp.code, 200)
        self.assertEqual(resp.json['total_items'], 4)
        self.assertEqual(len(resp.json['objects']), 0)

        query["page"] = 1
        query["online"] = 0
        resp = self.get(self.url, query=query)
        self.assertEqual(resp.code, 200)
        self.assertEqual(len(resp.json['objects']), 4)

        query = {"tag": 0}
        resp = self.get(self.url, query=query)
        self.assertEqual(resp.code, 200)
        self.assertEqual(len(resp.json['objects']), 0)

        query = {"keyword": "15154058704"}
        resp = self.get(self.url, query=query)
        self.assertEqual(resp.code, 200)
        self.assertEqual(len(resp.json['objects']), 1)
        self.assertEqual(resp.json["objects"][0]["mobile"], query["keyword"])

        # test get profile
        profile_id = project_user_list[0]
        url_404 = (self.url_pattern + '/{}').format(999, profile_id)
        resp = self.get(url_404)
        self.assertEqual(resp.code, 404)

        url = "{}/{}".format(self.url, profile_id)
        resp = self.get(url)
        self.assertEqual(resp.code, 200)
        print('=' * 80)
        print(resp.json)
        self.assertEqual(len(resp.json['attrs']), attrs_count)
        self.assertEqual(len(resp.json["tags"]), tags_count)

        # test for update  profile
        tags = [rv["id"] for rv in resp.json["tags"]][:2]
        attrs = []
        for attr in resp.json["attrs"]:
            if attr["col"] == "company":
                attrs.append({"col": attr["id"], "value": "SIOV"})
            elif attr["col"] == "department":
                attrs.append({"col": attr["id"], "value": "研发部"})
            else:
                attrs.append({"col": attr["id"], "value": attr["value"]})

        name = "老王"
        payload = {"tags": tags, "attrs": attrs,
                   "name": name, "mobile": resp.json["mobile"]}
        url = "{}/{}".format(self.url, profile_id)
        resp = self.json_put(url, payload=payload)
        self.assertEqual(resp.code, 200)
        resp = self.get(url)
        self.assertEqual(resp.code, 200)
        self.assertEqual(len(resp.json["tags"]), len(tags))
        self.assertEqual(resp.json["name"], name)
        resp_attrs = resp.json["attrs"]
        for attr in resp_attrs:
            if attr["col"] == "company":
                self.assertEqual(attr["value"], "SIOV")
            elif attr["col"] == "department":
                self.assertEqual(attr["value"], "研发部")

        # test for delete only one profile
        resp = self.delete(url)
        self.assertEqual(resp.code, 200)
        remained_count = session.query(AccountProfile).count()
        self.assertEqual(remained_count, 3)
        tag = session.query(Tag).filter(
            Tag.tag_type == Tag.ACCOUNT_TAG).first()
        print(tag.accounts.all())
        self.assertEqual(len(tag.accounts.all()), 2)

        # test for batch delete
        choice = ",".join(map(str, project_user_list[1:3]))
        url = "{}?choice={}".format(self.url, choice)
        resp = self.delete(url)
        self.assertEqual(resp.code, 200)
        remained_count = session.query(AccountProfile).count()
        self.assertEqual(remained_count, 1)


class VisitorsUsersTestCase(ApiTestCase):
    api = "project"
    url_pattern = "/v1.0/projects/{}/users/visitors"
    related_models = [Account, AccountProfile, AP, Online]

    def setUp(self):
        super().setUp()
        self.host_pn = 12
        self.url = self.url_pattern.format(self.host_pn)

    def insert_record(self, datas, model):
        for rv in datas:
            m = model(**rv)
            session.add(m)
            session.commit()

        count = session.query(model).count()
        self.assertEqual(count, len(datas))

    def test_users_visitors(self):
        account_kwargs = [
            {"mobile": "18825111140", "nickname": fake.name(),
             "user": "1143", "password": ""},
            {"mobile": "13612444229", "nickname": fake.name(),
             "user": "4229", "password": ""}
        ]
        self.insert_record(account_kwargs, Account)

        ap_mac = fake.mac_address().upper()
        ap_kwargs = [
            {"mac": ap_mac, "pn": self.host_pn, "address": "研究院三楼"}
        ]
        self.insert_record(ap_kwargs, AP)

        users = [rv['user'] for rv in account_kwargs]

        online_kwargs = []
        for user in users:
            user_mac = fake.mac_address().upper()
            auth_type = random.choice([0, 1, 2, 4])
            kwargs = {
                "user": user, "ap_mac": ap_mac, "pn": self.host_pn,
                "mac_addr": user_mac, "auth_type": auth_type,
                "nas_addr": str(uuid.uuid4())[:8],
                "acct_session_id": str(uuid.uuid4())[:8],
            }
            online_kwargs.append(kwargs)
        self.insert_record(online_kwargs, Online)

        resp = self.get(self.url)
        print('Resp => ', resp.json)
        self.assertEqual(resp.code, 200)
        self.assertEqual(resp.json['total_items'], 2)
        self.assertEqual(len(resp.json['objects']), 2)

        userid = resp.json['objects'][0]['userid']
        url = "{}?userid={}&action={}".format(self.url, userid, 'offline')
        resp = self.json_put(url, payload={})
        print('Resp => ', resp.json)
        self.assertEqual(resp.code, 200)

        resp = self.get(self.url)
        print('Resp => ', resp.json)
        self.assertEqual(resp.code, 200)
        self.assertEqual(resp.json['total_items'], 1)
