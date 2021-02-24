from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL

from . import settings

DeclarativeBase = declarative_base()


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(URL(**settings.DATABASE))


def create_table(engine):
    DeclarativeBase.metadata.create_all(engine)


class Threads(DeclarativeBase):
    """Sqlalchemy threads model"""
    __tablename__ = "threads"

    id = Column(Integer, primary_key=True)
    title = Column('title', String)
    author = Column('author', String, nullable=True)
    author_url = Column('author_url', String, nullable=True)
    date_created = Column('date_created', String, nullable=True)
    last_post_by = Column('last_post_by', String, nullable=True)
    last_post_date = Column('last_post_date', String, nullable=True)
    total_replies = Column('total_replies', String, nullable=True)
    total_views = Column('total_views', String, nullable=True)


class Authors(DeclarativeBase):
    """Sqlalchemy authors model for raidforums.com"""
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True)
    name = Column('name', String)
    # sex = Column('sex', String, nullable=True)
    date_joined = Column('date_joined', String, nullable=True)
    time_spent = Column('time_spent', String, nullable=True)
    members_referred = Column('members_referred', String, nullable=True)
    total_threads = Column('total_threads', String, nullable=True)
    total_posts = Column('total_posts', String, nullable=True)
    reputation = Column('reputation', String, nullable=True)
