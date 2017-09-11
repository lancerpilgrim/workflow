import os

import pymysql
import pymysql.cursors
from sqlalchemy import create_engine

import settings
from bidong.core.database import dburi, session

dbconf = settings.database["master"]
test_database = dbconf["db"] + "_test"


def patch_session():
    dbconf["db"] = test_database
    test_engine = create_engine(
        dburi.format(**dbconf),
        echo=settings.database["echo"],
        pool_recycle=settings.database["pool_recycle"]
    )
    session.bind = test_engine


def create_tables(sqlpath=None):
    if sqlpath is None:
        sqlpath = os.path.join(settings.BASE_DIR, 'docs/database/bidongv2.sql')

    with open(sqlpath, 'r') as reader:
        sql = " ".join(reader.readlines())

    dbconf["cursorclass"] = pymysql.cursors.DictCursor
    dbconf["db"] = test_database
    connection = pymysql.connect(**dbconf)

    try:
        with connection.cursor() as cursor:
            cursor = connection.cursor()
            cursor.execute(sql)
        connection.commit()
    except Exception as err:
        raise err
    finally:
        connection.close()


def init_database():
    dbconf["cursorclass"] = pymysql.cursors.DictCursor
    connection = pymysql.connect(**dbconf)
    try:
        with connection.cursor() as cursor:
            sql = "CREATE DATABASE `{}` DEFAULT CHARSET=utf8mb4;".format(
                test_database)
            cursor.execute(sql)
        connection.commit()
    except:
        pass
    finally:
        connection.close()

    try:
        create_tables()
    except Exception as err:
        raise err


def drop_database():
    dbconf["cursorclass"] = pymysql.cursors.DictCursor
    dbconf["db"] = test_database
    connection = pymysql.connect(**dbconf)
    try:
        with connection.cursor() as cursor:
            sql = "DROP DATABASE `{}`;".format(test_database)
            cursor.execute(sql)
        connection.commit()
    except Exception as err:
        print(err)
    finally:
        connection.close()
