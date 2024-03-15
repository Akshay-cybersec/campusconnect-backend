from rest_framework import serializers
from home.models import campusconnect

class campusconnect_ser(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=campusconnect
        fields = ['name', 'roll_no', 'enr_no', 'phno', 'parents_phno', 'addr', 'branch', 'percentage', 'email', 'kt', 'chatid']

class top_students_Serializer(serializers.ModelSerializer):
    class Meta:
        model = campusconnect
        fields = ['name','percentage','branch']

class kt_students_Serializer(serializers.ModelSerializer):
    class Meta:
        model = campusconnect
        fields = ['roll_no','name']

class message_serializer(serializers.ModelSerializer):
    class Meta:
        model = campusconnect
        fields = ['chatid']