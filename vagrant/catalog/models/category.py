from sqlalchemy import Column, ForeignKey, Integer, String, Sequence, DateTime, Text
from sqlalchemy.orm import relationship

from utils import Base


class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, Sequence('category_id'), primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(Text, default="")
    user_id = Column(Integer, ForeignKey('user.id'))
    items = relationship('Item', backref='item')
