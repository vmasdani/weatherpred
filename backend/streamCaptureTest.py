import cv2 as cv
import base64
import numpy as np
from PIL import Image
import requests
import json
import tempfile
from io import BytesIO
import os
PIXELS = 200

# def frame_to_base64(frame):
#     return base64.b64encode(frame)
def capture():
    image_base_64 = ''
    cap = cv.VideoCapture("192.168.1.266")
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret==True:
        # Capture frame
            print(frame)
            is_success, im_buf_arr = cv.imencode(".jpg", frame)
            encodedFrame = im_buf_arr.tobytes()
            print(encodedFrame)
            image_base_64 = base64.b64encode(encodedFrame)
            # print(image_base_64)
            cap.release()
            predict(image_base_64)
    else:
        print(f'Camera URL not valid.')

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


def predict(b64capture: str):

    categories = ["sunny", "cloudy", "foggy", "rainy", "snowy"]

    # Convert arbitrary sized jpeg image to 200x200 b/w image.
    # print(b64capture)
    img_bytes = base64.b64decode(b64capture) 
    print(img_bytes)
    temp = tempfile.NamedTemporaryFile(suffix='.jpg', prefix=os.path.basename(__file__))
    temp.write(img_bytes)
    temp.seek(0)
    image_file = temp
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
    # Convert LIST to nparray so that it multiplies correctly, this took me like 4 hours to figure out, god damn it. -Fahre
    convertedResultArray = np.asarray(jsonResult['predictions'])
    flattenResultArray = np.round(convertedResultArray * 100, 1).flatten()
    answer = np.argmax(flattenResultArray, axis=0)
    print(categories[answer])


capture()
