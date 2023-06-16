"""
URL configuration for project project.

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
from .import views

urlpatterns = [
    path('home', views.home, name='home'),
    path('signup', views.signup, name='signup'),
    path('sign_in', views.signin, name='signin'),
    path('', views.home, name='home'),
    path('signout', views.signout, name='signout'),

    path('user_profile_view', views.user_profile_view, name='user_profile_view'),
    path('user_home', views.user_home, name='user_home'),

    path('admin_home', views.admin_home, name='admin_home'),
    path('admin_user_details_view', views.admin_user_details_view, name='admin_user_details_view'),
    path('admin_user_details_edit', views.admin_user_details_edit, name='admin_user_details_edit'),
    path('admin_user_details_delete', views.admin_user_details_delete, name='admin_user_details_delete'),
    
    path('admin_user_search', views.admin_user_search, name='admin_user_search'),
    path('admin_user_details_add', views.admin_user_details_add, name='admin_user_details_add'),

    
]
