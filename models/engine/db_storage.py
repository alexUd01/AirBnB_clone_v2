#!/usr/bin/python3
""" A module that contains only a single class `DBStorage` """
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


classes = {"User": User, "State": State, "City": City, "Amenity": Amenity,
           "Place": Place, "Review": Review}


class DBStorage:
    """ Database Storage Engine """
    __engine = None
    __session = None

    def __init__(self):
        """ Initialize instances """
        from sqlalchemy import create_engine
        from os import getenv
        from models.base_model import Base

        _user = getenv('HBNB_MYSQL_USER')
        _pass = getenv('HBNB_MYSQL_PWD')
        _host = getenv('HBNB_MYSQL_HOST', default='localhost')
        _db_name = getenv('HBNB_MYSQL_DB')

        self.__engine = create_engine(
            "mysql+mysqldb://{}:{}@{}/{}".format(_user, _pass, _host, _db_name),
            pool_pre_ping=True
        )
        # Determine whether to use `test` or `development` envirionment
        _env = getenv('HBNB_ENV')
        if _env == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ A method that performs a query on the current database session
        depending on the class name `cls`
        """
        if cls is None:
            query = self.__session.query(User, State, City, Amenity, Place,
                                         Review).all()
        else:
            query = self.__session.query(classes[cls]).all()

        result = {}
        for obj in query:
            key = type(obj).__name__ + '.' + obj.id
            result[key] = obj
            del result[key]._sa_instance_state

        return result

    def new(self, obj):
        """ Adds the object `obj` to the current database session. """
        self.__session.add(obj)

    def save(self):
        """ Commit all changes of the current database session. """
        self.__session.commit()

    def delete(self, obj=None):
        """ Delete from the current database session `obj`. """
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """ Create all tables in the database """
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review
        from sqlalchemy.orm import sessionmaker
        from sqlalchemy.orm import scoped_session
        from models.base_model import Base

        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False
        )
        Session = scoped_session(session_factory)
        self.__session = Session()
