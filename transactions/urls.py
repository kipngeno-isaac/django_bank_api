from django.conf.urls import url 
from . import views 
 
urlpatterns = [ 
    url('/list', views.index),
    url('/add', views.store),
]
