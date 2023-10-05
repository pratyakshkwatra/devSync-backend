from sqlalchemy import create_engine, Column, String, Integer, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy_json import NestedMutableJson
from sqlalchemy import inspect

Base = declarative_base()
db_url = 'sqlite:///devSync.db'
engine = create_engine(db_url)


class Project(Base):
    __tablename__ = "project"
    id = Column("project-id", Integer, primary_key=True)
    title = Column("project-title", String)
    description = Column("project-description", String)
    timeStamp = Column("project-timestamp", String)
    path = Column("project-path", String)
    last_used = Column("project-last_used", String)

    def __init__(self, title, description, timeStamp, details, path, last_used):
        self.title = title
        self.description = description
        self.timeStamp = timeStamp
        self.details = details
        self.path = path
        self.last_used = last_used


Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine, expire_on_commit=True)
session = Session()


class File():
    id: int
    name: str
    path: str

    def __init__(self, id: int, name: str, path: str) -> None:
        self.id = id
        self.name = name
        self.path = path
