from django.urls import path
from .views import *


urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login_view'),
    path('logout/',logout_view,name='logout_view'),
]



