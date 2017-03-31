from sqlalchemy import Column, ForeignKey, Integer, String, Sequence, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, Sequence('user_id'), primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))
    created_at = Column(DateTime, default=datetime.now)
    categories = relationship('Category', backref='user')
    items = relationship('Item', backref='user')


class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, Sequence('category_id'), primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(Text)
    user_id = Column(Integer, ForeignKey('user.id'))


class Item(Base):
    __tablename__ = 'item'
    id = Column(Integer, Sequence('item_id'), primary_key=True)
    name = Column(String(250), nullable=False)
    url = Column(String(250), nullable=False)
    hightlight = Column(Text)
    user_id = Column(Integer, ForeignKey('user.id'))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


engine = create_engine('sqlite:///githubcatalog.db')
Base.metadata.create_all(engine)
