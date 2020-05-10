from django.conf.urls import url,include
from . import views

app_name="app"
urlpatterns = [
    url('', views.home, name="home"),
    url(r'^index.html$', views.home, name="search"),
    
]

