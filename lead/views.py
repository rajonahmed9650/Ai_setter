from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from .models import Question,LeadScoringRule
from .serializers import QuestionSerializer,LeadScroingRuleSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


# Create your views here.


class QuestionListApiView(APIView):
    authentication_classes = []
    permission_classes = [IsAuthenticated]
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

class QuestionDetailsApiView(APIView):
    authentication_classes = []
    permission_classes = [IsAuthenticated]
    def get_obj(self,pk):
        try:
            return Question.objects.get(pk=pk)
        except Question.DoesNotExist:
            return None
        
    def get(self,request,pk):
        question = self.get_obj(pk)
        if not question:
            return Response({"error":"Question not found"},status=status.HTTP_404_NOT_FOUND)
        serializer = QuestionSerializer(question)
        return Response(serializer.data,status=status.HTTP_200_OK)
    def put(self,request,pk):
        question = self.get_obj(pk)
        if not question:
            return Response({"error":"Question not found"},status=status.HTTP_404_NOT_FOUND)
        serializer = QuestionSerializer(question,data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,pk):
        question = self.get_obj(pk)
        if not question:
            return Response({"error":"Question not found"})
        question.delete()
        return Response({"message":"Question deleted successfully"})
    

class LeadScoringApiView(APIView):
    authentication_classes = []
    permission_classes = [IsAuthenticated]
    def get(self,request):
        leadscores = LeadScoringRule.objects.all()
        serializers = LeadScroingRuleSerializer(leadscores,many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)
    def post(self,request):
        serializer = LeadScroingRuleSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)

class LeadScoringDetailsView(APIView):
    authentication_classes = []
    permission_classes = [IsAuthenticated]
    def get_Obj(self,pk):
        try:
            return LeadScoringRule.objects.get(pk=pk)
        except LeadScoringRule.DoesNotExist:
            return None
        
    def get(self,request,pk):
        leadscore = self.get_Obj(pk)
        if not leadscore:
            return Response({"error":"LeadScore not found"},status=status.HTTP_404_NOT_FOUND)
        serializer = LeadScroingRuleSerializer(leadscore)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def put(self,request,pk):
        leadscore = self.get_Obj(pk)
        if not leadscore:
            return Response({"error":"LeadScore not found"},status=status.HTTP_404_NOT_FOUND)
        serializer = LeadScroingRuleSerializer(leadscore,data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,pk):
        leadscore = self.get_Obj(pk)
        if not leadscore:
            return Response({"error":"LeadScore not found"},status=status.HTTP_404_NOT_FOUND)
        leadscore.delete()
        return Response({"message":"Leadscore deleted successfully"}) 
        
    
        
            
    



        

