import random
from datetime import datetime, timedelta

from bidong.core.database import session
from bidong.storage.models import Package, PackageOrder
from bidong.storage.models import Account, Projects, AccountProfile


def insert_record(datas, model):
    rvs = []
    for kwargs in datas:
        m = model(**kwargs)
        session.add(m)
        session.flush()
        kwargs['id'] = m.id
        rvs.append(kwargs)
    session.commit()
    return rvs


def today_offset(offset=0):
    day = datetime.now() + timedelta(days=offset)
    return day.strftime("%Y-%m-%d %H:%M:%S")


def fetch_projects():
    rvs = session.query(Projects.id, Projects.name).filter(
        Projects.status == Projects.ENABLED
    ).all()
    return {rv.id: rv.name for rv in rvs}


def fetch_account_id_list(project_id=None):
    if project_id is None:
        rvs = session.query(Account.id).all()
        return [rv.id for rv in rvs]
    else:
        rvs = session.query(AccountProfile.account_id).filter(
            AccountProfile.pn == project_id).all()
        return [rv.account_id for rv in rvs]


def bulk_new_package(project_id=None, project_name=None):
    if project_id is None:
        pn, name = 0, "平台"
    else:
        pn, name = project_id, project_name

    count = 2
    packages = []
    for n in range(count):
        pack = {
            "pn": pn, "name": "{}的套餐-{}".format(name, n),
            "price": random.randint(30, 80),
            "time": random.choice([30, 45, 60])
        }
        packages.append(pack)

    return insert_record(packages, Package)


def gen_fack_orders(project_id=None, project_name=None):
    accounts = fetch_account_id_list(project_id)
    if not accounts:
        print("{} has not user, quit".format(project_name))

    if len(accounts) > 20:
        accounts = accounts[:20]
    packages = bulk_new_package(project_id, project_name)

    orders = []
    for offset in range(7):
        created_at = today_offset(-offset)
        idx = 20 - offset
        if len(accounts) < idx:
            idx = len(accounts)
        if not idx:
            break

        for aid in accounts[:idx]:
            for p in packages:
                kwargs = {}
                kwargs['pay_with'] = random.choice(['微信支付', '支付宝'])
                kwargs['pay_from'] = random.choice(['APP', '微信'])
                kwargs['package_id'] = p['id']
                kwargs['account_id'] = aid
                kwargs['amount'] = p['price']
                kwargs['created_at'] = created_at
                print("Package => ", kwargs)
                orders.append(kwargs)

    return insert_record(orders, PackageOrder)


def load():
    orders = gen_fack_orders()
    print("Gen platform orders => {}".format(len(orders)))

    project_dict = fetch_projects()
    for _id, name in project_dict.items():
        print("{} => {}".format(_id, name))
        orders = gen_fack_orders(_id, name)
        print("Gen {} orders => {}".format(name, len(orders)))
