from django.db import models

# Create your models here.
class campusconnect(models.Model):
    name=models.CharField(max_length=100,default='')
    roll_no=models.CharField(max_length=10,default='',primary_key=True)
    enr_no=models.CharField(max_length=10,default='')
    phno=models.CharField(max_length=10,default='')
    parents_phno=models.CharField(max_length=10,default='')
    addr=models.TextField(max_length=100,default='')
    branch=models.CharField(max_length=100,default='')
    percentage=models.IntegerField()
    email=models.CharField(max_length=50,default='')
    kt=models.BooleanField(default=False)
    chatid=models.CharField(max_length=50,default='')
