from django.shortcuts import render

from main_app.models import Areas
from main_app.utils import get_news, predict, weather
import os

# Create your views here.

def index(request):
    context = {}

    context['page_name'] = 'Home'
    # context['page_title'] = 'About Us'
    context['news'] = get_news()[-1:-4:-1]
    return render(request,'index.html', context=context)




def about(request):
    context = {}

    context['page_name'] = 'About'
    context['page_title'] = 'About Us'
    return render(request,'about.html', context=context)


def area_details(request):
    context = {}

    context['page_name'] = 'Details'
    context['page_title'] = 'Details'
    context['areas'] = Areas.objects.all()


    if request.method == "POST":
        print("Post Method")
        data = request.POST
        
        area_id = data.get("area")
        area = Areas.objects.get(id=area_id)
        soils_details = area.soildetails_set.all()

        context['soil_details'] = soils_details     



    return render(request,'area-details.html', context=context)


def weather_forecasting(request):
    context = {}

    context['page_name'] = 'Weather Forecasting'
    context['page_title'] = 'Weather Forecasting'
    context['areas'] = Areas.objects.all()

    if request.method == "POST":
        print("Post Method")
        data = request.POST        
        area_id = data.get("area")
        area = Areas.objects.get(id=area_id)
        area_name = area.name

        weather_details = weather(area_name)
        # print("sdhjsghsdf",weather_details)
        context['weather_details'] = weather_details 
        context['city'] = area_name


    return render(request,'weather-forecasting.html', context=context)


def training_model(request):
    context = {}

    context['page_name'] = 'Plant Disease Detection'
    context['page_title'] = 'Plant Disease Detection'


    if request.method == "POST":
        print("Post Method")
        # data = request.POST
        # print(data)
        files = request.FILES
        print(files)

        image = files.get("img")
        # print(image.read())
        image_url = "leaf.jpg"

        with open(image_url,"wb") as f:
            for chunk in image.chunks():
                f.write(chunk)

        title,description,symptoms,prevent,supplement_name = predict(image_url)
  
        #Prediction
        context['plant_details'] = {
            "p1":title,
            "p2":description,
            "p3":symptoms,
            "p4":prevent,
            "p5":supplement_name
      
            } 

        os.remove(image_url)



    return render(request,'test.html', context=context)
