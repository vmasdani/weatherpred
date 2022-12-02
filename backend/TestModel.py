import keras
from keras.models import Sequential
from keras.utils import to_categorical
import numpy as np
from tensorflow.keras.utils import load_img, img_to_array
import pandas as pd
from pathlib import Path
from typing import Tuple, List

from PIL import Image
import numpy as np
import matplotlib.pyplot as plt


imgWidth= 256
imgHeight=256

classes = ["sunny", "cloudy", "foggy", "rainy", "snowy"]

# model = load_model("/home/idnosian/weather-classification/dataset/bestWeatherModel.h5")
loaded_model = keras.models.load_model("./CNN")
print(model.summary() )

def predict_image_3c(
    model, file: str, pixels: int = 50, show: bool = False
) -> str:
    """Return the prediction of the `file` image
    with 3 channels, for CNN."""

    img = Image.open(file)

    # convert into gray and resize
    img = img.convert("RGB").resize((pixels, pixels))
    # scale pixel values out of 256 values
    img_array = np.asarray(img) / 255

    if show:
        plt.gca().imshow(img_array)

    # reashape to feed it in the CNN
    img_array = img_array.reshape((1, pixels, pixels, 3))


    return model.predict(img_array, verbose=False)

def prepareImage(ImagePath):
    image = load_img(ImagePath, target_size=(imgHeight,imgWidth))
    imgResult = img_to_array(image)
    imgResult = np.expand_dims(imgResult, axis = 0)
    imgResult - imgResult / 255.
    return imgResult

file_path = input('Enter a file path to image: ') 


resultArray = model.predict(prepareImage(file_path), batch_size=16, verbose=1)
answers = np.argmax(resultArray, axis = 1)
print("RESULT : " + classes[answers[0]])






# testImagesFolder = "/home/idnosian/weather-classification/dataset/test"
# testImagesNamesDF = pd.read_csv("/home/idnosian/weather-classification/original-dataset/test.csv")
# testImagesList = []

# # create list of images with its full names

# # testDFList = testImagesNamesDF['Image_id'].tolist()

# #print(testDFList)

# # for item in testDFList:
# #     tempName = testImagesFolder + "/" + str(item)
# #     testImagesList.append(tempName)


# print("The list of the images : ")
# print(testImagesList)

# #The first element 
# ImagesArray = prepareImage(testImagesList[0])

# # from the second till the end 
# for imgName in testImagesList[1: ]:
#     print("preparing image : " + imgName)
#     processedImage = prepareImage(imgName)
#     ImagesArray = np.append(ImagesArray,processedImage,axis=0)

# print("Images shape: ")
# print(ImagesArray.shape)

# #save the np array
# np.save("/home/idnosian/weather-classification/dataset", ImagesArray)

# # predict all the images in the array

