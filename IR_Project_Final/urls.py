"""
Definition of urls for IR_Project.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin

from app import views
from django.conf.urls import url,include

urlpatterns = [
    path('', views.home, name='home'),
    url(r'^search/', include('app.urls', namespace='app')),
    path('admin/', admin.site.urls),
]
