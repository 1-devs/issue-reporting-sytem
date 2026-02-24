from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from ..serializers.signupSer import LeadercreationSerializer
from ..permissions import IsLeader

class RegisterView(APIView):
    def post(self, request):
        # Handle user registration logic here
        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED) 

class LeaderCreationView(generics.CreateAPIView):
    serializer_class = LeadercreationSerializer
    permission_classes = [IsLeader]

    def perform_create(self, serializer):
        serializer.save()