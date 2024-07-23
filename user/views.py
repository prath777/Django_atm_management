from django.shortcuts import render
from django.http import HttpResponse

from rest_framework.views import APIView  
from rest_framework.response import Response  
from rest_framework import status  
from .models import User  
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated

from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from django.core.exceptions import ObjectDoesNotExist

import utils as utl

class UserView(APIView):  
    def get(self, request):  
        return Response({"status": "success", "data": "Login successful"}, status=status.HTTP_200_OK)  

    def post(self, request):  
        serializer =UserSerializer(data=request.data) 
        if serializer.is_valid():  
            print("validated")
            serializer.save()  
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)  
        else:  
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)  


@api_view(['POST'])
def user_login(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')

        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            return Response({'error': 'Username Not found'}, status=status.HTTP_404_NOT_FOUND)
        if(user.password!=password):
            return Response({'error': 'Incorrect Password'}, status=status.HTTP_400_BAD_REQUEST)

       
        if user:
            access_token = utl.generate_access_token(user)
            return Response({'token': access_token}, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class RefreshTokenView(APIView):
    def post(self, request):
        refresh_token = request.data.get('refresh')

        payload = utl.decode_token(refresh_token)
        if not payload:
            return Response({'error': 'Invalid or expired refresh token'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            user = User.objects.get(id=payload['user_id'])
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        new_access_token = utl.generate_access_token(user)

        return Response({'access': new_access_token})
    