#!/usr/bin/python3
"""
This module contains the database engine implementation
"""
import os
from models.base_model import Base
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, scoped_session
from models.place import Place
from models.city import City
from models.review import Review
from models.state import State
from models.amenity import Amenity
from models.user import User


class DBStorage:
    """Definition for database storage instances"""
    __engine = None
    __session = None

    def __init__(self):
        """Called on object instantiation"""
        self.__engine = create_engine(
                'mysql+mysqldb://{}:{}@{}/{}'
                .format(
                    os.getenv('HBNB_MYSQL_USER'),
                    os.getenv('HBNB_MYSQL_PWD'),
                    os.getenv('HBNB_MYSQL_HOST', 'localhost'),
                    os.getenv('HBNB_MYSQL_DB')
                    ),
                pool_pre_ping=True
                )

        if os.getenv('HBNB_ENV') == 'test':
            # Drop tables only in the test environment
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Returns specified objects from database"""
        # Dictionary to hold objects
        _objects = {}

        if cls:
            # Query the specified class
            if issubclass(cls, Base):
                objs = self.__session.query(cls).order_by(cls.name).all()

        else:
            # Query all specified classes
            classes = [User, State, City, Amenity, Place, Review]
            objs = []

            for cls in classes:
                if issubclass(cls, Base):
                    objs.extend(self.__session.query(cls).order_by(cls.name).all())

        # Create unique keys for each object and add them to the dictionary
        for obj in objs:
            key = f'{obj.__class__.__name__}.{obj.id}'
            _objects[key] = obj

        return _objects

    def new(self, obj):
        """Add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete obj from the current database session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database"""
        Base.metadata.create_all(self.__engine)

        # Create the current database session
        self.__session = scoped_session(
                sessionmaker(bind=self.__engine, expire_on_commit=False)
                )

    def close(self):
        """Close the current session"""
        self.__session.remove()
