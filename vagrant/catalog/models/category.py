from sqlalchemy import Column, ForeignKey, Integer, String, Sequence, DateTime, Text
from sqlalchemy.orm import relationship
from base import Base


class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, Sequence('category_id'), primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(String, default="")
    user_id = Column(Integer, ForeignKey('user.id'))
    items = relationship('Item', backref='item')

    @property
    def serialize(self):
        return {'id': self.id, 'name': self.name, 'description': self.description, 'user_id': self.user_id}
