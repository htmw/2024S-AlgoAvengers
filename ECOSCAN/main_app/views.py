from django.shortcuts import render
import random
from main_app.models import Areas
from main_app.utils import get_news, predict, weather
import os
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import LeafDiseaseHistory

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('/')

# Create your views here.

@login_required
def index(request):
    context = {}

    context['page_name'] = 'Home'
    # context['page_title'] = 'About Us'
    context['news'] = get_news()[-1:-4:-1]
    return render(request,'index.html', context=context)



@login_required
def about(request):
    context = {}

    context['page_name'] = 'About'
    context['page_title'] = 'About Us'
    return render(request,'about.html', context=context)

@login_required
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

@login_required
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

@login_required
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
        
        
        image_url = f"processed/leaf_{random.randint(1111111111,9999999999)}.jpg"
        path = os.getcwd()+'//'+image_url

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

        
        history_entry = LeafDiseaseHistory.objects.create(
            user=request.user,
            image=path,
            disease_name=title,
            description=description,
            symptoms=symptoms,
            prevent=prevent,
            supplement_name=supplement_name
        )
        
        
        #os.remove(image_url)



    return render(request,'test.html', context=context)


@login_required
def history(request):
    user_history = LeafDiseaseHistory.objects.filter(user=request.user)
    context = {'user_history': user_history}
    return render(request, 'history.html', context=context)