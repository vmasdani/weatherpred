# import requests
# import base64

# def main():
#   image_string = base64.urlsafe_b64encode(open("backend/model/1/testimages/UMN-Kampus-Hijau.jpg", "rb").read())

#   endpoint = "http://127.0.0.1:8500"
#   json_data = {"model_name": "cnnmodel", "data": {"images": [image_string]} }
#   result = requests.post(endpoint, json=json_data)
#   print(result)

# if __name__ == "__main__":
#   main()

from __future__ import print_function

import base64
import requests
import numpy as np
import matplotlib.pyplot as plt

# The server URL specifies the endpoint of your server running the ResNet
# model with the name "resnet" and using the predict interface.
SERVER_URL = 'http://localhost:8501/v1/models/cnnmodel:predict'

# The image URL is the location of the image we should send to the server
IMAGE_URL = 'https://tensorflow.org/images/blogs/serving/cat.jpg'


def main():
  # Download the image
  dl_request = requests.get(IMAGE_URL, stream=True)
  dl_request.raise_for_status()

  # Compose a JSON Predict request (send JPEG image in base64).
  img_array = np.asarray(img).flatten() / 255
  jpeg_bytes = base64.b64encode(dl_request.content).decode('utf-8')
  predict_request = '{"instances" : [{"b64": "%s"}]}' % jpeg_bytes

  # Send few requests to warm-up the model.
  for _ in range(3):
    response = requests.post(SERVER_URL, data=predict_request)
    response.raise_for_status()

  # Send few actual requests and report average latency.
  total_time = 0
  num_requests = 10
  for _ in range(num_requests):
    response = requests.post(SERVER_URL, data=predict_request)
    response.raise_for_status()
    total_time += response.elapsed.total_seconds()
    prediction = response.json()['predictions'][0]

  print('Prediction class: {}, avg latency: {} ms'.format(
      prediction['classes'], (total_time*1000)/num_requests))


if __name__ == '__main__':
  main()