import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(32), index=True)
    email = Column(String(254))
    picture = Column(String(250))


class Categories(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)
    description = Column(String(250))

    @property
    def serialize(self):
        return {
               'id': self.id,
               'name': self.name,
               'description': self.description
        }


class subCategories(Base):
    __tablename__ = "subcategories"

    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship(Categories)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        return {
               'id': self.id,
               'name': self.name
        }


class CategoryItem(Base):
    __tablename__ = 'category_item'

    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)
    description = Column(String(250), nullable=False)
    category_id = Column(Integer, ForeignKey('subcategories.id'))
    category = relationship(subCategories)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        return {
               'id': self.id,
               'name': self.name,
               'description': self.description,
               'user_id': self.user_id
        }


engine = create_engine('sqlite:///categorymenu.db')

Base.metadata.create_all(engine)
