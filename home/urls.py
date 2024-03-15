from django.contrib import admin
from django.urls import path,include
from home.views import CampusViewSet
from rest_framework import routers
from home.views import register_campusconnect, top_students,kt_records,total_count,message,botmessage

router=routers.DefaultRouter()
router.register(r'campusconnectapi',CampusViewSet)

urlpatterns = [
    path('',include(router.urls)),
    path('campusconnectpost/', register_campusconnect, name='register_student'),
    path('branch_top/<str:branch>', top_students, name='branch_top'),
    path('kt_record/<str:branch>', kt_records, name='kt_record'),
    path('total_count/<str:branch>', total_count, name='total_counts'),
    path('message', message, name='message_send'),
    path('botmessage/<str:message>', botmessage, name='botmessagedone'),
]
