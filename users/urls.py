from django.conf.urls import url 
from . import views 
 
urlpatterns = [ 
    url('/list', views.user_list),
    url('/create', views.user_create),

]
