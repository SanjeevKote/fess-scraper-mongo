"""
URL configuration for FessScrapper_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from FessApp.views import Deloitte, guardian,sodalitas,hbr,common

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('myfess/', Gardian.Fess_Gardian_Post, name='Gardian'),
    # path('myfess/deloitte/',Deloitte.Fess_Deloitte_Post,name='Deloitte'),
    # path('myfess/sodalitas/',sodalitas.Fess_Sodalitas_Post,name='sodalitas'),
    # path('myfess/hbr/',hbr.Fess_hbr_Post,name='hrbr'),
    path('myfess/',common.Fess_split_Post,name='fess')
]
