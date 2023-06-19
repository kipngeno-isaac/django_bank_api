from django.conf.urls import url 
from . import views 
 
urlpatterns = [ 
    url('list', views.index),
    url('deposit', views.deposit),
    url('withdraw', views.withdraw),
]
