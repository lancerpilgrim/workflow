import uuid

import faker

from bidong.core.database import session
from bidong.storage.models import Account, AccountProfile
from bidong.storage.models import AP, Online, Projects

fake = faker.Factory.create()

host_project = '20170905'
vistor_project = '20170904测试'


def get_project_by_name(name):
    rv = session.query(Projects.id).filter_by(name=name).first()
    return rv.id if rv else 0


def load():
    host_id = get_project_by_name(host_project)
    vistor_id = get_project_by_name(vistor_project)
    if not host_id or not vistor_id:
        print("error! project not exists")
        return
    print("Get Host=> %s, Guest=> %s" % (host_id, vistor_id))

    rv = session.query(AP.mac).filter_by(pn=host_id).first()
    if not rv:
        print("AP NOT FOUND")
        return
    ap_mac = rv.mac

    rvs = session.query(Account.user, AccountProfile.account_id).filter(
        Account.id == AccountProfile.account_id,
        AccountProfile.pn == vistor_id
    ).all()
    rvs = [rv for rv in rvs]
    if not rvs:
        print("Vistor project hos not user!")
    if len(rvs) > 2:
        rvs = rvs[:2]

    account_users = [rv.user for rv in rvs]

    for user in account_users:
        o = Online(
            user=user, ap_mac=ap_mac, pn=host_id,
            mac_addr=fake.mac_address().upper(),
            nas_addr=str(uuid.uuid4())[:8],
            acct_session_id=str(uuid.uuid4())[:8]
        )
        session.add(o)
    session.commit()
    print('Add online success!')
