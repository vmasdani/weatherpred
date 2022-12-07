import numpy as np
from PIL import Image
import requests
import json
    
def main():
  pixels = 200
  image_file = 'backend/model/1/testimages/test7.jpg'
  categories = ["sunny", "cloudy", "foggy", "rainy", "snowy"]
  # Convert arbitrary sized jpeg image to 200x200 b/w image.
  img = Image.open(image_file)
    
  # convert into gray and resize
  img = img.convert("RGB").resize((pixels, pixels))
  # scale pixel values out of 256 values
  img_array = np.asarray(img) / 255

  # reashape to feed it in the CNN
  img_array = img_array.reshape((1, pixels, pixels, 3))
  img_array = img_array.astype(float)
  # print(img_array)
  # Dump jpeg image bytes as 200x200 tensor
  np.set_printoptions(threshold=np.inf)       
  json_request = '{{ "instances" : {} }}'.format(np.array2string(img_array, separator=',', formatter={'float':lambda x: "%.1f" % x}))
  resp = requests.post('http://localhost:8501/v1/models/cnnmodel:predict', data=json_request)
  # print('response.status_code: {}'.format(resp.status_code))     
  # print('response.content: {}'.format(resp.content))
  jsonResult = json.loads(resp.content)
  answer = np.argmax(jsonResult, axis=0)
  # print(answer)
  print(categories[answer])
main()