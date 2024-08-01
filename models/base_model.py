#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models"""

    id = Column(
            String(60),
            primary_key=True,
            default=lambda: str(uuid.uuid4())
            )
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        self.id = kwargs.get('id', str(uuid.uuid4()))

        self.created_at = (
                datetime.strptime(kwargs['created_at'], '%Y-%m-%dT%H:%M:%S.%f')
                if 'created_at' in kwargs
                else datetime.utcnow()
        )

        self.updated_at = (
                datetime.strptime(kwargs['updated_at'], '%Y-%m-%dT%H:%M:%S.%f')
                if 'updated_at' in kwargs
                else datetime.utcnow()
        )
        if '__class__' in kwargs:
            del kwargs['__class__']

        self.__dict__.update(kwargs)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]

        str_fmt = {}

        # excludes '_sa_instance_state' from string output
        for key, value in self.__dict__.items():
            if key != '_sa_instance_state':
                str_fmt[key] = value

        return '[{}] ({}) {}'.format(cls, self.id, str_fmt)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        if isinstance(dictionary.get('created_at'), datetime):
            dictionary['created_at'] = self.created_at.isoformat()
        if isinstance(dictionary.get('updated_at'), datetime):
            dictionary['updated_at'] = self.updated_at.isoformat()

        if '_sa_instance_state' in dictionary:
            del dictionary['_sa_instance_state']

        return dictionary

    def delete(self):
        """delete the current instance from storage"""
        from models import storage
        storage.delete(self)
