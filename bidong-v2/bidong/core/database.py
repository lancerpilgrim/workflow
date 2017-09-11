from functools import wraps

from werkzeug.local import LocalProxy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import settings

dburi = ("mysql+pymysql://{user}:{password}@{host}:{port}/{db}"
         "?charset={charset}")
dbconf = settings.database

engines = {
    "master": create_engine(
        dburi.format(**dbconf['master']),
        echo=dbconf['echo'] == 1,
        pool_recycle=dbconf['pool_recycle']
    ),
    "slave": create_engine(
        dburi.format(**dbconf['slave']),
        echo=dbconf['echo'] == 1,
        pool_recycle=dbconf['pool_recycle']
    )
}

session_factory = sessionmaker(bind=engines['master'])
Session = scoped_session(session_factory)
session = LocalProxy(Session)


def with_db(name):
    def with_session(func):
        @wraps(func)
        def func_wrapper(*args, **kwargs):
            session = Session()
            old_bind = session.bind
            session.bind = engines[name]

            try:
                return func(*args, **kwargs)
            finally:
                session.bind = old_bind

        return func_wrapper
    return with_session
