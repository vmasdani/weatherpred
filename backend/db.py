
from dataclasses import dataclass
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import SingletonThreadPool

engine = create_engine("sqlite:///./db/db.sqlite3",
                       echo=True, poolclass=SingletonThreadPool)
Base = declarative_base()

@dataclass
class Camera(Base):
    __tablename__ = 'cameras'

    id: int = Column(Integer, primary_key=True,)
    name: str = Column(String)
    ip_address: str = Column(String)
    created: str = Column(String)
    deleted: str = Column(String)

    def __init__(self, obj):
        self.id = obj.get('id')

        self.name = obj.get('name')
        self.ip_address = obj.get('ip_address')

        self.created = obj.get('created')
        self.deleted = obj.get('deleted')


@dataclass
class Snapshot(Base):
    __tablename__ = 'snapshots'

    id: int = Column(Integer, primary_key=True)
    camera_id: int = Column(Integer)
    prediction: str = Column(String)
    created: str = Column(String)
    deleted: str = Column(String)

    def __init__(self, obj):
        self.id = obj.get('id')

        self.camera_id = obj.get('camera_id')
        self.prediction = obj.get('prediction')

        self.created = obj.get('created')
        self.deleted = obj.get('deleted')


Session = sessionmaker(bind=engine)
session = Session()