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
from PIL import Image
import requests
import json
import numpy as np
# if args.type == 'exec':
app = flask.Flask(__name__)
CORS(app)
PIXELS = 200


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


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
    temp = tempfile.NamedTemporaryFile(
        suffix='.jpg', prefix=os.path.basename(__file__))
    temp.write(img_bytes)
    temp.seek(0)

    image_file = temp
    # Convert arbitrary sized jpeg image to 200x200 b/w image.
    img = Image.open(image_file)

    categories = ["sunny", "cloudy", "foggy", "rainy", "snowy"]

    # Convert arbitrary sized jpeg image to 200x200 b/w image.
    img = Image.open(image_file)
    # convert into gray and resize
    img = img.convert("RGB").resize((PIXELS, PIXELS))
    # scale pixel values out of 256 values
    img_array = np.asarray(img) / 255
    # reashape to feed it in the CNN
    img_array = img_array.reshape((1, PIXELS, PIXELS, 3))
    # dumping the result to json to send
    json_request = json.dumps({'instances': img_array}, cls=NpEncoder)
    # sending request to TensorFlow Serving, and the response
    resp = requests.post(
        'http://localhost:8501/v1/models/cnnmodel:predict', data=json_request)
    print('response.status_code: {}'.format(resp.status_code))
    print('response.content: {}'.format(resp.content))
    # loads the result
    jsonResult = json.loads(resp.content)
    # Convert LIST to nparray so that it multiplies correctly, this took me like 4 hours to figure out, god damn it.
    convertedResultArray = np.asarray(jsonResult['predictions'])
    flattenResultArray = np.round(convertedResultArray * 100, 1).flatten()
    answer = np.argmax(flattenResultArray, axis=0)
    temp.close()
    return (categories[answer])


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
