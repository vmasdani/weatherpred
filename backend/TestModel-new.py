import tensorflow as tf
import keras
from keras.models import Sequential
from keras.models import Model
from keras.preprocessing import image
from tensorflow.keras.utils import load_img, img_to_array
from utils import (
    predict_image_3c,
)
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
PIXELS = 200
categories = ["sunny", "cloudy", "foggy", "rainy", "snowy"]

model = keras.models.load_model("./backend/model")

# def prepareImage(pathForImage):
#     image = load_img(pathForImage , target_size=(150,150))
#     imgResult = img_to_array(image)
#     imgResult = np.expand_dims(imgResult , axis = 0)
#     imgResult = imgResult / 255. 
#     return imgResult

testImagePath = input('Enter a file path to image: ') 

# prepare the image using our function
# imgForModel = prepareImage(testImagePath)

resultArray = predict_image_3c(
    model, testImagePath, pixels=PIXELS, show=True
)
print (resultArray)

flattenResultArray = np.round(resultArray * 100, 1).flatten()
print (flattenResultArray)
# the highest value is the predicted value and wee need the index in the resultArray
answer = np.argmax(flattenResultArray, axis=0)
print (answer)

# index = answer[0]

print ("this image is : "+ categories[ answer ])
