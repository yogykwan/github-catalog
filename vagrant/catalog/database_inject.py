from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Category, Item

engine = create_engine('sqlite:///githubcatalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

user = User(name='Jennica', email='jingg.cxy@foxmail.com')
session.add(user)
session.commit()

category1 = Category(name='Frontend', description='HTML/CSS/Javascript')
session.add(category1)
session.commit()

items11 = Item(name='movie-trailer-website', url='https://github.com/yogykwan/movie-trailer-website', user_id=1, category_id='1', highlight='Amazing!')
session.add(items11)
session.commit()

items12 = Item(name='portfolio', url='https://github.com/yogykwan/portfolio', user_id=1, category_id='1', highlight='Amazing!')
session.add(items12)
session.commit()

category2 = Category(name='Backend', description='Python/Flask/Database')
session.add(category2)
session.commit()

items21 = Item(name='multi-user-blog', url='https://github.com/yogykwan/multi-user-blog', user_id=1, category_id='2', highlight='Amazing!')
session.add(items21)
session.commit()

category3 = Category(name='Fullstack', description='Ionic/Nodejs/Mongodb')
session.add(category3)
session.commit()

