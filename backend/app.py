from argparse import ArgumentParser
from dataclasses import dataclass
import datetime
import dacite
import flask
from flask import jsonify, request
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import SingletonThreadPool


# parser = ArgumentParser()
# parser.add_argument('--type')

# args = parser.parse_args()

engine = create_engine("sqlite:///./db.sqlite3", echo=True, poolclass=SingletonThreadPool)
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

# if args.type == 'exec':
app = flask.Flask(__name__)


@app.route('/')
def hello():
    return 'hello world!'


@app.get('/cameras')
def cameras():
    d =  session.query(Camera).all()
    session.close()
    return jsonify(d)

@app.post('/cameras')
def cameras_post():
    cam = request.get_json(force=True)
    cam['created'] = datetime.datetime.now().isoformat()

    session.add(Camera(cam))
    session.commit()
    
    return session.query(Camera).all()


app.run('0.0.0.0', 7002)
