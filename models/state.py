#!/usr/bin/python3
""" State Module for HBNB project """
import os
from sqlalchemy import Column, String
from models.base_model import BaseModel, Base


class State(BaseModel, Base):
    """ State class """

    __tablename__ = 'states'

    name = Column(String(128), nullable=False)

    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        from sqlalchemy.orm import relationship
        cities = relationship(
                'City',
                backref='state',
                order_by='City.name',
                cascade='all, delete-orphan'
                )

    else:
        @property
        def cities(self):
            from models.city import City
            from models import storage
            all_cities = storage.all(City)
            my_cities = []

            for ID, city in all_cities.items():
                if city.state_id == self.id:
                    my_cities.append(city)

            return my_cities
