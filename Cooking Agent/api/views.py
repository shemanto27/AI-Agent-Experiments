from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import *
from agents.agent import process_instruction

class AgentView(APIView):
    def post(self, request):
        serializer = instruction_serializer(data=request.data)
        # input validation
        if serializer.is_valid():
            instruction = serializer.validated_data['instruction']
            
            #process the instruction using agent
            try:
                agent_response = process_instruction(instruction)
                
            except Exception as e:
                return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            #return the response
            response = {"response" : agent_response}
            response_data = response_serializer(data=response)
            if response_data.is_valid():
                return Response(response_data.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
