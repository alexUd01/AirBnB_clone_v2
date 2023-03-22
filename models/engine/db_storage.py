#!/usr/bin/python3
""" A module that contains only a single class `DBStorage` """


class DBStorage:
    """ Database Storage Engine """
    __engine = None
    __session = None

    def __init__(self):
        """ Initialize instances """
        from sqlalchemy import create_engine
        from os import getenv
        from models.base import Base

        _user = getenv('HBNB_MYSQL_USER')
        _pass = getenv('HBNB_MYSQL_PWD')
        _host = getenv('HBNB_MYSQL_HOST', default='localhost')
        _db_name = getenv('HBNB_MYSQL_DB')

        self.__engine = create_engine(
            "mysql+msqldb://{}:{}@{}/{}".format(_user, _pass, _host, _db_name),
            pool_pre_ping=True
        )
        # Determine whether to use `test` or `development` envirionment
        _env = getenv('HBNB_ENV')
        if _env == 'test':
            
