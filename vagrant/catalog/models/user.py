from sqlalchemy import Column, ForeignKey, Integer, String, Sequence, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from base import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, Sequence('user_id'), primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    categories = relationship('Category', backref='user')
    items = relationship('Item', backref='user')