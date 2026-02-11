from django.shortcuts import render
from rest_framework import generics
from .serializers import CustomUserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = CustomUserSerializer

    def get_object(self):
        return self.request.user


class PasswordChangeView(APIView):

    def update(self, request):

        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')

        if new_password != confirm_password:
            return Response({'error': 'Passwords do not match'}, status=400)

        user = request.user
        if not user.check_password(old_password):
            return Response({'error': 'Invalid old password'}, status=400)
        
        if len(new_password) < 8:
            return Response({'error': 'Password must be at least 8 characters'}, status=400)

        user.set_password(new_password)
        user.save()
        return Response({'message': 'Password changed successfully'})

# Create your views here.
class RegisterView(APIView):
    def post(self, request):
        # Handle user registration logic here
        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED) 
       
