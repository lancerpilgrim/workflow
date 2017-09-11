import uuid
import random

import faker

from bidong.core.database import session
from bidong.storage.models import Account, AccountProfile, Dyncol, PNField, Tag
from bidong.storage.models import AP, Online
from bidong.service import account
from tests.service import ServiceTestCase

fake = faker.Factory.create()


class TestAccount(ServiceTestCase):
    models = [Tag, Account]

    def setUp(self):
        super(TestAccount, self).setUp()

    def tearDown(self):
        super(TestAccount, self).tearDown()

    def test_create_account(self):
        kwargs = {
            "mobile": "13612444229", "password": "89012345", "name": "名字"}
        rv = account.create_account(**kwargs)
        self.assertTrue(rv > 0)

        record = session.query(Account).filter_by(id=rv).first()
        self.assertEqual(record.mobile, kwargs['mobile'])

    def test_upate_account(self):
        kwargs = {
            "mobile": "13612444229", "password": "89012345", "name": "名字"}
        account_id = account.create_account(**kwargs)

        kwargs = {
            "password": "1234567890", "name": "CC", "coin": 20, "ends": 5
        }
        account.update_account(account_id, **kwargs)
        record = session.query(Account).filter_by(id=account_id).first()
        self.assertEqual(record.name, kwargs['name'])
        self.assertEqual(record.coin, kwargs['coin'])

    def test_disable_account_global(self):
        kwargs = {
            "mobile": "13612444229", "password": "89012345", "name": "CC"
        }
        account_id = account.create_account(**kwargs)
        kwargs = {
            "mobile": "18825111139", "password": "89012345", "name": "小明"
        }
        account.create_account(**kwargs)

        account.disable_account(account_id=account_id)
        account.disable_account(mobile=kwargs['mobile'])

        rvs = session.query(Account).all()
        for rv in rvs:
            self.assertTrue((rv.mask & (1 << 30)) > 0)

    def test_many_thing(self):
        tags = [
            {"pn": 0, "tag_type": "account", "name": "员工"},
            {"pn": 0, "tag_type": "account", "name": "优惠"},
            {"pn": 0, "tag_type": "account", "name": "开发者"}
        ]
        tags = [Tag(**kw) for kw in tags]
        session.add_all(tags)
        session.commit()
        tags = session.query(Tag).all()
        self.assertTrue(len(tags) > 0)

        tag_id_list = [t.id for t in tags]
        kwargs = {
            "mobile": "13612444229", "password": "89012345", "name": "CC"
        }
        account_id = account.create_account(**kwargs)
        account.attach_tags(account_id, tag_id_list, 0)

        record = session.query(Account).filter_by(id=account_id).first()
        self.assertEqual(len(record.tags), len(tag_id_list))

        record = account.get_account(account_id)
        self.assertIsNotNone(record)
        record = account.get_account(mobile=kwargs["mobile"])
        self.assertIsNotNone(record)

        profile = account.base_profile(account_id)
        self.assertEqual(profile['name'], kwargs['name'])
        self.assertEqual(profile['mobile'], kwargs['mobile'])
        self.assertEqual(len(profile['tags']), len(tags))

        data = account.account_overview()
        print(data)
        self.assertEqual(data["total_user"], 1)
        self.assertEqual(data["online_user"], 0)
        self.assertEqual(data["today_register"], 1)


class TestDyncol(ServiceTestCase):
    models = [PNField, Dyncol]

    def setUp(self):
        super().setUp()

        self.dyncols = [
            {"col": "company", "label": "公司"},
            {"col": "department", "label": "部门"},
            {"col": "title", "label": "职位"},
            {"col": "email", "label": "邮箱"},
            {"col": "id_number", "label": "身份证号"},
            {"col": "id_front_image", "label": "身份证照片（正面）"},
            {"col": "id_back_image", "label": "身份证照片（反面）"},
            {"col": "note", "label": "备注"}
        ]
        for kw in self.dyncols:
            rv = Dyncol(**kw)
            session.add(rv)
        session.commit()
        self.service = account.ProjectAccountService(12)

    def tearDown(self):
        super().tearDown()

    def test_get_default_dyncol(self):
        dyncols = account.get_default_dyncol()
        self.assertEqual(len(dyncols), len(self.dyncols))

    def get_col_id_list(self, dyncols):
        choiced = [rv['col'] for rv in dyncols]
        rvs = session.query(Dyncol.id).filter(Dyncol.col.in_(choiced)).all()
        col_id_list = [rv.id for rv in rvs]
        return col_id_list

    def test_set_project_dyncol(self):
        col_id_list = self.get_col_id_list(self.dyncols[:5])
        self.service.set_dyncol(col_id_list)
        count = session.query(PNField).count()
        self.assertEqual(len(col_id_list), count)

        col_id_list = self.get_col_id_list(self.dyncols[5:])
        self.service.set_dyncol(col_id_list)
        count = session.query(PNField).count()
        self.assertEqual(len(col_id_list), count)

    def test_get_project_dyncol(self):
        col_id_list = self.get_col_id_list(self.dyncols[:5])
        self.service.set_dyncol(col_id_list)
        count = session.query(PNField).count()
        self.assertEqual(len(col_id_list), count)

        dyncols = self.service.get_dyncol()
        insert_ids = [c.id for c in dyncols]
        self.assertListEqual(sorted(col_id_list), sorted(insert_ids))


class TestAccountProfile(ServiceTestCase):
    models = [PNField, Dyncol, AccountProfile, Account]

    def setUp(self):
        super().setUp()

        self.dyncols = [
            {"col": "company", "label": "公司"},
            {"col": "department", "label": "部门"},
            {"col": "title", "label": "职位"},
            {"col": "email", "label": "邮箱"},
            {"col": "id_number", "label": "身份证号"},
            {"col": "id_images", "label": "身份证照片"},
            {"col": "note", "label": "备注"},
        ]
        for kw in self.dyncols:
            rv = Dyncol(**kw)
            session.add(rv)
        session.commit()
        self.pn = 12
        self.service = account.ProjectAccountService(self.pn)

    def tearDown(self):
        super().tearDown()

    def test_create_account_profile(self):
        attr_dict = {"company": "CNICG", "department": "Develop"}
        kwargs = {
            "account_id": 12, "name": "Wong", "mobile": 13612444229,
            "attr_dict": attr_dict
        }
        profile_id = self.service.create_profile(**kwargs)
        self.assertTrue(profile_id > 0)

        profile = session.query(
            AccountProfile).filter_by(id=profile_id).first()
        self.assertEqual(profile.name, kwargs['name'])
        self.assertEqual(profile.dynattr('company'), attr_dict['company'])

    def test_update_account_profile(self):
        attr_dict = {"company": "CNICG", "department": "Develop"}
        kwargs = {
            "account_id": 12, "name": "Chou", "mobile": 13612444229,
            "attr_dict": attr_dict
        }
        profile_id = self.service.create_profile(**kwargs)
        self.assertTrue(profile_id > 0)

        attr_dict['company'] = 'SIOV'
        attr_dict['title'] = "Python Engineer"
        kwargs.pop("account_id")
        kwargs["profile_id"] = profile_id
        kwargs["name"] = "Wong"
        self.service.update_profile(**kwargs)

        profile = session.query(AccountProfile).first()
        self.assertEqual(profile.name, kwargs["name"])
        self.assertEqual(profile.dynattr("company"), attr_dict["company"])
        self.assertEqual(profile.dynattr("title"), attr_dict["title"])

    def test_get_account_profile(self):
        cols = ("company", "department", "title")
        dyncol_id_list = [
            rv.id for rv in
            session.query(Dyncol).filter(Dyncol.col.in_(cols)).all()
        ]
        for col_id in dyncol_id_list:
            field = PNField(pn=self.pn, dyncol_id=col_id)
            session.add(field)
        session.commit()

        kwargs = {
            "mobile": "13612444229", "password": "89012345", "name": "名字"}
        account_id = account.create_account(**kwargs)
        attr_dict = {"company": "CNICG", "department": "Develop"}
        kwargs = {
            "account_id": account_id, "name": "Chou",
            "mobile": 13612444229, "attr_dict": attr_dict
        }
        profile_id = self.service.create_profile(**kwargs)
        self.assertTrue(profile_id > 0)

        rv = self.service.get_profile(profile_id)
        self.assertEqual(rv["name"], kwargs["name"])
        self.assertEqual(len(rv["attrs"]), len(cols))
        self.assertEqual(len(rv["tags"]), 0)

    def test_delete_profile(self):
        kwargs = [
            {"account_id": 1, "pn": self.pn, "mobile": 13612444229},
            {"account_id": 2, "pn": self.pn, "mobile": 13612444230},
            {"account_id": 3, "pn": self.pn, "mobile": 13612444231},
        ]

        ids = []
        for kw in kwargs:
            p = AccountProfile(**kw)
            session.add(p)
            session.commit()
            ids.append(p.id)
        count = session.query(AccountProfile).count()
        self.assertEqual(count, 3)

        self.service.delete_profile(profile_id=ids[0])
        count = session.query(AccountProfile).count()
        self.assertEqual(count, 2)

        self.service.delete_profile(batch_delete=ids[1:])
        count = session.query(AccountProfile).count()
        self.assertEqual(count, 0)


class TestProjectAccount(ServiceTestCase):
    models = [Dyncol, PNField, Account, AccountProfile, Tag, AP, Online]

    def setUp(self):
        super().setUp()

        self.pn = 12
        self.service = account.ProjectAccountService(self.pn)

        dyncols = [
            {"col": "company", "label": "公司"},
            {"col": "department", "label": "部门"},
            {"col": "title", "label": "职位"},
            {"col": "email", "label": "邮箱"},
            {"col": "id_number", "label": "身份证号"},
            {"col": "id_images", "label": "身份证照片"},
            {"col": "note", "label": "备注"},
        ]
        self.cols_id = []
        for kw in dyncols:
            col = Dyncol(**kw)
            session.add(col)
            session.commit()
            self.cols_id.append(col.id)
        self.service.set_dyncol(self.cols_id[:4])

        tags = [
            {"pn": self.pn, "tag_type": "account", "name": "员工"},
            {"pn": self.pn, "tag_type": "account", "name": "优惠"},
            {"pn": self.pn, "tag_type": "account", "name": "开发者"}
        ]
        self.tags_id = []
        for t in tags:
            tag = Tag(**t)
            session.add(tag)
            session.commit()
            self.tags_id.append(tag.id)

    def tearDown(self):
        super().tearDown()

    def test_create_project_account(self):
        attrs = [
            {"col": self.cols_id[0], "value": "SIOV"},
            {"col": self.cols_id[1], "value": "研发部"},
            {"col": self.cols_id[2], "value": "Python工程师"}
        ]
        tags = self.tags_id[:2]

        kwargs = {
            "name": "Wong", "mobile": "13612444229",
            "attrs": attrs, "tags": tags
        }
        rv = self.service.create(**kwargs)
        self.assertTrue(rv)
        rv = self.service.create(**kwargs)
        self.assertFalse(rv)

        self.service.pn = self.pn + 100
        rv = self.service.create(**kwargs)
        self.assertTrue(rv)
        self.service.pn = self.pn

        count = session.query(Account).count()
        self.assertEqual(count, 1)

        count = session.query(AccountProfile).count()
        self.assertEqual(count, 2)

        _account = session.query(Account).first()
        tag_count = len(_account.tags)
        self.assertEqual(tag_count, 2)

    def test_update_project_account(self):
        attrs = [
            {"col": self.cols_id[0], "value": "SIOV"},
            {"col": self.cols_id[1], "value": "研发部"},
            {"col": self.cols_id[2], "value": "Python工程师"}
        ]
        tags = self.tags_id[:2]

        kwargs = {
            "name": "ChouKinchong", "mobile": "13612444229",
            "attrs": attrs, "tags": tags
        }
        rv = self.service.create(**kwargs)
        self.assertTrue(rv)

        profile = session.query(AccountProfile).first()
        kwargs = {
            "profile_id":  profile.id, "name": "Wong",
            "attrs": attrs, "tags": self.tags_id[2:]
        }
        self.service.update(**kwargs)
        profile = session.query(AccountProfile).first()
        self.assertEqual(profile.name, kwargs["name"])
        self.assertEqual(profile.dynattr("company"), "SIOV")

        _account = session.query(Account).first()
        tag_count = len(_account.tags)
        self.assertEqual(tag_count, 1)

    def test_get_project_account_list(self):
        user_count = 20
        attrs = [
            {"col": self.cols_id[0], "value": "SIOV"},
            {"col": self.cols_id[1], "value": "研发部"},
            {"col": self.cols_id[2], "value": "Python工程师"}
        ]
        tags = self.tags_id

        kwargs = {
            "name": "", "mobile": "",
            "attrs": attrs, "tags": tags
        }
        for n in range(user_count):
            kwargs["name"] = "Wong - {}".format(n)
            kwargs["mobile"] = "136124442{}".format(n+10)
            self.service.create(**kwargs)

        count = session.query(AccountProfile).count()
        self.assertEqual(count, user_count)

        users = self.service.fetch()
        self.assertEqual(len(users), user_count)

        users = self.service.fetch(online=0)
        self.assertEqual(len(users), user_count)

        users = self.service.fetch(online=1)
        self.assertEqual(len(users), 0)

        users = self.service.fetch(tag_id=tags[0])
        self.assertEqual(len(users), user_count)

        users = self.service.fetch(keyword="13612444210")
        self.assertEqual(len(users), 1)

        paginator = self.service.fetch(page=1, page_size=5)
        self.assertEqual(paginator['total_items'], user_count)
        self.assertEqual(paginator['total_pages'], 4)
        self.assertEqual(len(paginator['objects']), 5)

        ap_mac = "58:69:6C:59:1D:4C"
        ap = AP(mac=ap_mac, pn=self.pn, address="研究院三楼")
        session.add(ap)
        for n in range(user_count // 4):
            o = Online(user="136124442{}".format(n+10), ap_mac=ap_mac,
                       mac_addr="58:69:6C:59:10:{}".format(n+10),
                       nas_addr=str(n), acct_session_id=str(n))
            session.add(o)
        session.commit()

        users = self.service.fetch(online=0)
        self.assertEqual(len(users), user_count - user_count // 4)

        users = self.service.fetch(online=1)
        self.assertEqual(len(users), user_count // 4)


class TestProjectVisitor(ServiceTestCase):
    models = [Account, AccountProfile, AP, Online]

    def setUp(self):
        super().setUp()
        self.a, self.b = 10, 12
        self.service = account.ProjectAccountService(self.a)

    def tearDown(self):
        super().tearDown()

    def test_list_visitors(self):
        # testing prepare
        user_count = 20
        kwargs = {
            "name": "", "mobile": "",
            "attrs": [], "tags": []
        }
        for n in range(user_count):
            kwargs["name"] = "Wong - {}".format(n)
            kwargs["mobile"] = "136124442{}".format(n+10)
            if n % 2:
                self.service.pn = self.a
                self.service.create(**kwargs)
            else:
                self.service.pn = self.b
                self.service.create(**kwargs)

        project_a_accounts = session.query(
            Account.user, AccountProfile.id
        ).filter(
            Account.id == AccountProfile.account_id,
            AccountProfile.pn == self.a
        ).all()
        project_b_accounts = session.query(
            Account.user, AccountProfile.id
        ).filter(
            Account.id == AccountProfile.account_id,
            AccountProfile.pn == self.b
        ).all()

        self.assertEqual(len(project_a_accounts), user_count//2)
        self.assertEqual(len(project_b_accounts), user_count//2)

        online_people = [a.user for a in project_a_accounts]
        online_people.extend([b.user for b in project_b_accounts])

        ap_mac = "58:69:6C:59:1D:4C"
        ap = AP(mac=ap_mac, pn=self.a, address="研究院三楼")
        session.add(ap)

        for user in online_people:
            user_mac = fake.mac_address().upper()
            auth_type = random.choice([0, 1, 2, 4])
            o = Online(user=user, ap_mac=ap_mac, pn=self.a,
                       auth_type=auth_type, mac_addr=user_mac,
                       nas_addr=str(uuid.uuid4())[:8],
                       acct_session_id=str(uuid.uuid4())[:8])
            session.add(o)
        session.commit()

        experted_count = len(online_people) // 2
        self.service.pn = self.a
        rvs = self.service.list_visitors(page=1, page_size=20)
        self.assertEqual(experted_count, len(rvs["objects"]))

        userid = rvs['objects'][0]['userid']
        rv = self.service.kick_out_visitor(userid)
        self.assertTrue(bool(rv))
        rvs = self.service.list_visitors(page=1, page_size=20)
        self.assertEqual(experted_count - 1, len(rvs["objects"]))

        rvs = self.service.list_visitors(page=20, page_size=20)
        self.assertEqual(0, len(rvs["objects"]))
