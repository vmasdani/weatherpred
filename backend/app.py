from argparse import ArgumentParser
import asyncio
import base64
from dataclasses import dataclass
import dataclasses
import datetime
import os
import random
import dacite
import flask
from flask import jsonify, make_response, request, send_file
from flask_cors import CORS
from db import Snapshot, session, Camera
from dto import SnapshotEndpoint
import tempfile
import numpy as np
from utils import (
    predict_image_3c,
)

# if args.type == 'exec':
app = flask.Flask(__name__)
CORS(app)


@app.route('/')
def hello():
    return 'hello world!'


@app.get('/snapshots/<id>')
def get_snapshot(id):
    return send_file(f'{os.getcwd()}/files/snapshot-{id}', mimetype='image/png')


@app.get('/cameras')
def cameras():
    d = session.query(Camera).all()
    session.close()
    return jsonify(d)


@app.get('/snapshots')
def snapshots():
    d = session.query(Snapshot).all()
    session.close()
    return jsonify(d)


@app.post('/cameras')
def cameras_post():
    cam = request.get_json(force=True)
    cam['created'] = datetime.datetime.now().isoformat()

    session.merge(Camera(cam))
    session.commit()

    d = session.query(Camera).all()
    session.close()

    return d


@app.post('/cameras-save-bulk')
def cameras_post_bulk():
    cam = request.get_json(force=True)
    cams = []

    for c in cam:
        if 'created' not in c:
            c['created'] = datetime.datetime.now().isoformat()

        session.merge(Camera(c))

    session.commit()

    d = session.query(Camera).all()
    session.close()

    return d


@app.post('/predict')
def predict_endpoint():
    snapshot_endpoint_body = request.get_json(force=True)
    # print(snapshot_endpoint_body)

    snapshot_param = SnapshotEndpoint(snapshot_endpoint_body)

    # print(snapshot_param.image_base_64)
    s = snapshot_weather(
        camera_id=snapshot_param.camera_id,
        dummy=snapshot_param.dummy,
        image_base_64=snapshot_param.image_base_64
    )
    return jsonify(dataclasses.asdict(s))


@app.get('/predict-scheduler')
def predict_scheduler_endpoint():
    predict_scheduler()
    return 'OK'


@app.get('/predict-dummy')
def predict_dummy_endpoint():
    predict_scheduler(dummy=True)
    return 'OK'

# Move model here


def actual_predict(img_bytes: str):
    temp = tempfile.NamedTemporaryFile(suffix='.jpg', prefix=os.path.basename(__file__))
    temp.write(img_bytes)
    temp.seek(0)

    PIXELS = 200
    categories = ["sunny", "cloudy", "foggy", "rainy", "snowy"]
    testImagePath = os.path.dirname(temp.name)
    resultArray = predict_image_3c(
        testImagePath, pixels=PIXELS, show=True
    )
    temp.close()
    flattenResultArray = np.round(resultArray * 100, 1).flatten()
    answer = np.argmax(flattenResultArray, axis=0)
    
    return categories[answer]
    # # Placeholder prediction
    # rn = random.randint(0, 2)

    # if rn == 0:
    #     return 'sunny'
    # elif rn == 1:
    #     return 'cloudy'
    # elif rn == 2:
    #     return 'rainy'
    # else:
    #     return None


def dummy_predict():
    rn = random.randint(0, 2)

    if rn == 0:
        return 'sunny'
    elif rn == 1:
        return 'cloudy'
    elif rn == 2:
        return 'rainy'
    else:
        return None


def snapshot_weather(camera_id: int, image_base_64: str, dummy=False):
    s = Snapshot({})
    s.camera_id = camera_id

    img_bytes = ''

    if dummy == True:
        dummy_prediction_file = open('./dummy-pred.png', 'rb')
        dummy_prediction_file_contents = dummy_prediction_file.read()
        dummy_prediction_file.close()

        img_bytes = dummy_prediction_file_contents

        s.prediction = dummy_predict()
    else:
        # print(image_base_64)
        img_bytes = base64.b64decode(image_base_64)
        s.prediction = actual_predict(img_bytes=img_bytes)

    # Save snapshot
    s.created = datetime.datetime.now().isoformat()

    saved_snapshot = session.merge(s)
    session.commit()

    # Save image snapshot
    pred_img = open(f'./files/snapshot-{saved_snapshot.id}', 'wb')
    pred_img.write(img_bytes)
    pred_img.close()

    return saved_snapshot


def predict_scheduler(dummy=False):
    print(
        f'[Periodic cam] {datetime.datetime.now().isoformat()} fetching camera snapshot...')

    cameras = session.query(Camera).all()

    for c in cameras:
        print(f'Fetching camera: {dataclasses.asdict(c)}')

        # Image base64
        image_base_64 = ''

        if dummy == False and image_base_64 == '':
            print(f'No camera result detected for camera {c.id}. Skipping.')
            return

        snapshot_weather(
            camera_id=c.id,
            dummy=dummy,
            image_base_64=image_base_64
        )


app.run('0.0.0.0', 7002)
