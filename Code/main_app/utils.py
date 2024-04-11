from bs4 import BeautifulSoup
import requests
import numpy as np
import os,cv2
import pandas as pd

from PIL import Image

import numpy as np

import pandas as pd
import os
import requests, json

import keras
from keras.models import load_model
from tensorflow.keras.utils import load_img, img_to_array 
import tensorflow_addons as tfa

idx_to_classes = {0: 'Apple___Apple_scab',
                  1: 'Apple___Black_rot',
                  2: 'Apple___Cedar_apple_rust',
                  3: 'Apple___healthy',
                  4: 'Background_without_leaves',
                  5: 'Blueberry___healthy',
                  6: 'Cherry___Powdery_mildew',
                  7: 'Cherry___healthy',
                  8: 'Corn___Cercospora_leaf_spot Gray_leaf_spot',
                  9: 'Corn___Common_rust',
                  10: 'Corn___Northern_Leaf_Blight',
                  11: 'Corn___healthy',
                  12: 'Grape___Black_rot',
                  13: 'Grape___Esca_(Black_Measles)',
                  14: 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)',
                  15: 'Grape___healthy',
                  16: 'Orange___Haunglongbing_(Citrus_greening)',
                  17: 'Peach___Bacterial_spot',
                  18: 'Peach___healthy',
                  19: 'Pepper,_bell___Bacterial_spot',
                  20: 'Pepper,_bell___healthy',
                  21: 'Potato___Early_blight',
                  22: 'Potato___Late_blight',
                  23: 'Potato___healthy',
                  24: 'Raspberry___healthy',
                  25: 'Soybean___healthy',
                  26: 'Squash___Powdery_mildew',
                  27: 'Strawberry___Leaf_scorch',
                  28: 'Strawberry___healthy',
                  29: 'Tomato___Bacterial_spot',
                  30: 'Tomato___Early_blight',
                  31: 'Tomato___Late_blight',
                  32: 'Tomato___Leaf_Mold',
                  33: 'Tomato___Septoria_leaf_spot',
                  34: 'Tomato___Spider_mites Two-spotted_spider_mite',
                  35: 'Tomato___Target_Spot',
                  36: 'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
                  37: 'Tomato___Tomato_mosaic_virus',
                  38: 'Tomato___healthy'}

disease_info = pd.read_csv(r'disease_info.csv' , encoding='cp1252')
supplement_info = pd.read_csv(r'supplement_info.csv',encoding='cp1252')
model = load_model("./model/",custom_objects={'KerasLayer':tfa.activations.gelu})



def load_image(img_path, show=False):
    img = cv2.imread(img_path)
    img = cv2.resize(img,(224,224))
    img = img.reshape(1,224,224,3) 
    return img


def predict(image_path): 
    i = load_img(image_path, target_size=(224,224))
    i = img_to_array(i)
    i = i.reshape(1, 224,224,3)

    out = model.predict(i)[0]
    pred = out.argmax()
    pr = out[pred]*100
    title = disease_info['disease_name'][pred]
    if pred>=75:
        title+=" (Stage III)"
    elif pred<75 and pred>50:
        title+=" (Stage II)"
    elif pred<=50:
        title+=" (Stage I)"
    description =disease_info['description'][pred]
    symptoms = disease_info['sypmtoms'][pred]
    prevent = disease_info['precautions'][pred]
    image_url = disease_info['image_url'][pred]
    supplement_name = supplement_info['supplement name'][pred]
    supplement_image_url = supplement_info['supplement image'][pred]
    supplement_buy_link = supplement_info['buy link'][pred]
    return title,description,symptoms,prevent,supplement_name

print(predict("leaf.jpg"))
