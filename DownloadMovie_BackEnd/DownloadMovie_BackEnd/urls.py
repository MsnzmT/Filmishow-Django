"""DownloadMovie_BackEnd URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from backend.views import *
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', signup),
    path('login/', obtain_auth_token),
    path('logout/', LogOut.as_view()),
    path('home/', show_all_film),
    path('upload-film/', upload_film),
    path('comment/', add_comment),
    path('category/horror/', filter_films),
    path('category/drum/', filter_films),
    path('category/fantasy/', filter_films),
    path('category/action/', filter_films),
    path('category/comedy/', filter_films),
    path('search/', search_film),
]
