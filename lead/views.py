from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from .models import Question
from .serializers import QuestionSerializer
from rest_framework.response import Response
# Create your views here.
class QuestionListApiView(APIView):
    def get(self,request):
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions,many=True)
        return  Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self,request):
        serializer = QuestionSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
        

