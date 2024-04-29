"""agriculture URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from main_app.views import area_details, register, user_login, user_logout, index, training_model, weather_forecasting, history

from main_app.views import about

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('about/', about),
    path('area-details/', area_details),
    path('weather-forecasting/', weather_forecasting),
    path('training-model/', training_model),
    path('history/', history, name='history'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


admin.site.site_header  =  "Ecoscan admin"  
admin.site.site_title  =  "Ecoscan admin site"
admin.site.index_title  =  "Ecoscan Admin"
