
from django.contrib import admin
from django.urls import path,include
from home.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/',include('home.urls')),
    path('campusconnectpost/', register_campusconnect, name='register_student'),
    path('campusconnectdelete/<str:rollno>', delete_campusconnect, name='delete_campusconnect'),
    # add at the last

]

