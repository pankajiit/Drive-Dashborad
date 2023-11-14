"""
URL configuration for drive_dashboard project.

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
from my_app.views import home, signup, login_handler, upload_file,show_files,delete_file,logout
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', home, name = 'home'),
    path('singup/', signup, name = 'signup'),
    path('login/', login_handler, name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('upload/',upload_file, name = "upload_file"),
    path('show_files/', show_files, name = "show_files"),
    path('delete_file/<str:file_id>/', delete_file, name='delete_file'),
]
