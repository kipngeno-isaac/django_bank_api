from django.conf.urls import url 
from . import views 
 
urlpatterns = [ 
    url('list', views.index),
    url('<int:user_id>', views.get_transactions),
    url('deposit', views.deposit),
    url('withdraw', views.withdraw),
    url('transfer', views.transfer),
]
