from django.conf.urls import url 
from . import views 
 
urlpatterns = [ 
    # url('list', views.user_list),
    # url('create', views.user_create),
    url('register', views.register_api),
    url('login', views.login_api),

]
