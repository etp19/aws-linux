"""
Database set-up script for item catalogue
"""

# [START Imports]
from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import backref
# [END Imports]


base = declarative_base()

# Ubuntu, Apache, PostgreSQL config
# TODO change password
engine = create_engine(
    'postgresql+psycopg2://restaurant:db-password@localhost/restaurant')


db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
# [END Db engine and session]


class User(base):
    """
    Table to store User information
    """
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))


class Restaurant(base):
    __tablename__ = 'restaurant'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable = False)
    phone = Column(String(80), nullable=False)
    email = Column(String(250))
    website = Column(String(300))
    created_at = Column(DateTime, default=datetime.now())
    food_type = Column(String(80), nullable=False)
    description = Column(String(300), nullable=False)

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
            'phone': self.phone,
            'email': self.email,
            'website': self.website,
            'description': self.description,
        }


class RestaurantAddress(base):
    __tablename__ = 'restaurant_address'

    street = Column(String(250), nullable=False)
    city = Column(String(80), nullable=False)
    state = Column(String(80), nullable=False)
    zip_code = Column(String(300), nullable=False)
    id = Column(Integer, primary_key=True)
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'street': self.street,
            'city': self.city,
            'state': self.state,
            'zip code': self.zip_code,
        }


class MenuItem(base):
    __tablename__ = 'menu_item'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    course = Column(String(250))
    description = Column(String(250))
    price = Column(String(8))
    created_at = Column(DateTime, default=datetime.now())
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant, backref=backref("children", cascade="all,delete"))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'price': self.price,
            'course': self.course,
        }


base.metadata.create_all(engine)