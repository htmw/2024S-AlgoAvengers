from bs4 import BeautifulSoup
import requests
import numpy as np
import os,cv2
import pandas as pd
import torch.nn as nn
from PIL import Image
import torchvision.transforms.functional as TF
import numpy as np
import torch
import pandas as pd
import os
import requests, json
class CNN(nn.Module):
    def __init__(self, K):
        super(CNN, self).__init__()
        self.conv_layers = nn.Sequential(
            # conv1
            nn.Conv2d(in_channels=3, out_channels=32,
                      kernel_size=3, padding=1),
            nn.ReLU(),
            nn.BatchNorm2d(32),
            nn.Conv2d(in_channels=32, out_channels=32,
                      kernel_size=3, padding=1),
            nn.ReLU(),
            nn.BatchNorm2d(32),
            nn.MaxPool2d(2),
            # conv2
            nn.Conv2d(in_channels=32, out_channels=64,
                      kernel_size=3, padding=1),
            nn.ReLU(),
            nn.BatchNorm2d(64),
            nn.Conv2d(in_channels=64, out_channels=64,
                      kernel_size=3, padding=1),
            nn.ReLU(),
            nn.BatchNorm2d(64),
            nn.MaxPool2d(2),
            # conv3
            nn.Conv2d(in_channels=64, out_channels=128,
                      kernel_size=3, padding=1),
            nn.ReLU(),
            nn.BatchNorm2d(128),
            nn.Conv2d(in_channels=128, out_channels=128,
                      kernel_size=3, padding=1),
            nn.ReLU(),
            nn.BatchNorm2d(128),
            nn.MaxPool2d(2),
            # conv4
            nn.Conv2d(in_channels=128, out_channels=256,
                      kernel_size=3, padding=1),
            nn.ReLU(),
            nn.BatchNorm2d(256),
            nn.Conv2d(in_channels=256, out_channels=256,
                      kernel_size=3, padding=1),
            nn.ReLU(),
            nn.BatchNorm2d(256),
            nn.MaxPool2d(2),
        )

        self.dense_layers = nn.Sequential(
            nn.Dropout(0.4),
            nn.Linear(50176, 1024),
            nn.ReLU(),
            nn.Dropout(0.4),
            nn.Linear(1024, K),
        )

    def forward(self, X):
        out = self.conv_layers(X)

        # Flatten
        out = out.view(-1, 50176)

        # Fully connected
        out = self.dense_layers(out)

        return out


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
model = CNN(39)    
model.load_state_dict(torch.load(r"plant_disease_model_1.pt"))
model.eval()


def weather(city):
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
    CITY = city #"Ahmedabad"

    URL = BASE_URL + "q=" + CITY + "&appid=" + "2e46c08796ce01d9788055302c9ad485"

    response = requests.get(URL)

    if response.status_code == 200:

        data = response.json()

        main = data['main']
        main['temp'] = round(main['temp']-273.15)
        main['temp_max'] = main['temp_max']-273.15
        main['temp_min'] = main['temp_min']-273.15
        temperature = main['temp']
        # getting the humidity
        humidity = main['humidity']
        # getting the pressure
        pressure = main['pressure']
        # weather report
        report = data['weather']
        main['weather_report'] = report[0]['description']
        print(f"{CITY:-^30}")
        print(f"Temperature: {temperature}")
        print(f"Humidity: {humidity}")
        print(f"Pressure: {pressure}")
        print(f"Weather Report: {report[0]['description']}")
        return main
    else:
        # showing the error message
        print("Error in the HTTP request")

def load_image(img_path, show=False):
    img = cv2.imread(img_path)
    img = cv2.resize(img,(224,224))
    img = img.reshape(1,224,224,3) 
    return img


def predict(image_path): 
    image = Image.open(image_path)
    image = image.resize((224, 224))
    input_data = TF.to_tensor(image)
    input_data = input_data.view((-1, 3, 224, 224))
    output = model(input_data)
    output = output.detach().numpy()
    pred = np.argmax(output)
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


url = 'https://newsapi.org/v2/everything?'
api_key = 'ad339c3d21e94330b4287fec00bdf4bc'

def get_news():
    param_headlines = {
        'q':'farming',
        'language':"en",
        'page_size':3,
        'sort_by':"relevancy",
        'apiKey':api_key
    }

    response_headline = requests.get(url, params = param_headlines)
    response_json_headline = response_headline.json()

    responses = response_json_headline["articles"] 
    return responses 
