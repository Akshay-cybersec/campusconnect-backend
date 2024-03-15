from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from home.models import campusconnect
from home.serializers import campusconnect_ser,top_students_Serializer,kt_students_Serializer,message_serializer
from rest_framework.decorators import api_view
from django.db import IntegrityError
from rest_framework.decorators import action
import requests

# Create your views here.

class CampusViewSet(viewsets.ModelViewSet):
    queryset=campusconnect.objects.all()
    serializer_class=campusconnect_ser
    filter_backends=[SearchFilter]
    search_fields=['roll_no','branch']

@api_view(['GET'])
def kt_records(self, branch):
    queryset = campusconnect.objects.filter(branch=branch,kt=True)
    print(queryset)
    serializer = kt_students_Serializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
    
@api_view(['GET'])
def top_students(self, branch):
    branch_name = branch
    queryset = campusconnect.objects.filter(branch=branch_name)
    top = queryset.order_by('-percentage').values()[:3]
    serializer = top_students_Serializer(top, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def total_count(self, branch):
    queryset = campusconnect.objects.filter(branch=branch) 
    count = queryset.count()
    return Response({'count': count}, status=status.HTTP_200_OK)

@api_view(['POST'])
def register_campusconnect(request):
    data = request.data
    try:
        campusconnect_instance = campusconnect.objects.create(
            name=data.get('name', ''),
            roll_no=(data.get('roll_no', '')).replace(" ",""),
            enr_no=data.get('enr_no', ''),
            phno=data.get('phno', ''),
            parents_phno=data.get('parents_phno', ''),
            addr=data.get('addr', ''),
            branch=(data.get('branch', '')).replace(" ",""),
            percentage=data.get('percentage', ''),
            email=data.get('email', ''),
            kt=data.get('kt', False),
            chatid=data.get('chatid', '')
        )
        return Response({"message": "Record Created Successfully"})
    except IntegrityError:
        return Response({"error": "Roll no already exist! Roll number must be unique."}, status=status.HTTP_409_CONFLICT)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["DELETE"])
def delete_campusconnect(request, rollno):
    try:
        campusconnect_instance = campusconnect.objects.get(roll_no=rollno)
        campusconnect_instance.delete()
        return JsonResponse({'message': f'{rollno} deleted successfully'}, status=200)
    except campusconnect.DoesNotExist:
        return JsonResponse({'message': f'{rollno}  not found'}, status=404)

@api_view(["GET"])
def botmessage(request,message):
    try:
        response = requests.post("http://localhost:8181/webhooks/rest/webhook", json={'message': message})
        
        if response.ok:
            return Response(response.json(), status=response.status_code)
        else:
            return Response({'error': 'Failed to send message to bot'}, status=response.status_code)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(["POST"])
def message(request):
    roll_no = request.data.get('id')
    message = request.data.get('message')
    chatid=[]
    for i in roll_no.split(","):
        queryset = campusconnect.objects.filter(roll_no=i)
        if queryset.exists():
            campus_object = queryset.first()
            chatid.append(campus_object.chatid)
        else:
            response_data = {
                'status': 'Sorry chat not found'
            }
            return JsonResponse(response_data)
    for i in chatid:
        if(i==""):
            continue
        param={'chat_id':i,'text':message}
        requests.post("https://api.telegram.org/bot6926341079:AAGCvn15z1ZAZY-lSMKsVUohdXKFdcBh004/sendmessage",param)
    response_data = {
        'status': 'Message Sent successfully to '+roll_no
    }
        
    return JsonResponse(response_data)