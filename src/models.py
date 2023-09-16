from sqlalchemy import create_engine, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from eralchemy2 import render_er

engine = create_engine('sqlite:///social_media.db', echo=True)
Base = declarative_base()

class User(Base):
    __tablename__ = 'User'
    ID = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    firstname = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True)

    # Relaciones
    followers = relationship('Follower', foreign_keys='Follower.user_to_id')
    following = relationship('Follower', foreign_keys='Follower.user_from_id')
    posts = relationship('Post', back_populates='user')
    comments = relationship('Comment', back_populates='user')

class Post(Base):
    __tablename__ = 'Post'
    ID = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('User.ID'), nullable=False)
    content = Column(String(255), nullable=False)

    # Relaciones
    user = relationship('User', back_populates='posts')
    comments = relationship('Comment', back_populates='post')
    media = relationship('Media', back_populates='post')

class Media(Base):
    __tablename__ = 'Media'
    ID = Column(Integer, primary_key=True)
    type = Column(String(50), nullable=False)
    url = Column(String(255), nullable=False)
    post_id = Column(Integer, ForeignKey('Post.ID'), nullable=False)

    # Relaciones
    post = relationship('Post', back_populates='media')

class Follower(Base):
    __tablename__ = 'Follower'
    ID = Column(Integer, primary_key=True)
    user_from_id = Column(Integer, ForeignKey('User.ID'), nullable=False)
    user_to_id = Column(Integer, ForeignKey('User.ID'), nullable=False)

    # Relaciones
    user_from = relationship('User', foreign_keys=[user_from_id])
    user_to = relationship('User', foreign_keys=[user_to_id])

class Comment(Base):
    __tablename__ = 'Comment'
    ID = Column(Integer, primary_key=True)
    comment_text = Column(String(255), nullable=False)
    author_id = Column(Integer, ForeignKey('User.ID'), nullable=False)
    post_id = Column(Integer, ForeignKey('Post.ID'), nullable=False)

    # Relaciones
    user = relationship('User', back_populates='comments')
    post = relationship('Post', back_populates='comments')

# Crear la base de datos y las tablas
Base.metadata.create_all(engine)

# Generar el diagrama de entidad-relación
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem generating the diagram")
    raise e
