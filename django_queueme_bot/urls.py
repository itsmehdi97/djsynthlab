"""django_queueme_bot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include
# import django.views.defaults


import django

def custom_page_not_found(request):
    return django.views.defaults.page_not_found(request, None)
def custom_server_error(request):
    return django.views.defaults.server_error(request)



urlpatterns = [
    path('', admin.site.urls),
    path('users/', include('users.urls')),
    # path(r'^404/$', django.views.defaults.page_not_found, name='404'),
    # path(r'^500/$', django.views.defaults.server_error, name='500'),
    path("404/", custom_page_not_found),
]