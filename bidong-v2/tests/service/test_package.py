from bidong.core.database import session
from bidong.storage.models import Package, Tag
from bidong.service.package import PackageService

from tests.service import ServiceTestCase


class TestPackage(ServiceTestCase):
    models = [Package, Tag]

    def setUp(self):
        super().setUp()
        self.pn = 12

    def tearDown(self):
        super().tearDown()

    def _loat_tags(self, pn=0):
        tags = [
            {"pn": pn, "tag_type": "account", "name": "老师"},
            {"pn": pn, "tag_type": "account", "name": "学生"},
            {"pn": pn, "tag_type": "account", "name": "房东"},
            {"pn": pn, "tag_type": "account", "name": "租客"}
        ]
        for kw in tags:
            tag = Tag(**kw)
            session.add(tag)
        session.commit()
        rvs = session.query(Tag).all()
        self.assertEqual(len(rvs), len(tags))
        return [rv.id for rv in rvs]

    def test_create_package(self):
        # testing project create package
        pro = PackageService(self.pn)
        kwargs = {
            "name": "套餐1", "price": 30.00, "ends": 1,
            "time": 30, "tags": []
        }
        pro.create(**kwargs)
        p = session.query(Package).filter_by(name=kwargs['name']).first()
        self.assert
