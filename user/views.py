from urllib import request
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView  
from rest_framework.response import Response  
from rest_framework import status  
from .models import User,Transaction
from .serializers import UserSerializer,TransactionSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view,permission_classes
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator

import utils as utl

class UserView(APIView):  
    def get(self, request):  
        return Response({"status": "success", "data": "Login successful"}, status=status.HTTP_200_OK)  

    def post(self, request):  
        serializer =UserSerializer(data=request.data) 
        if serializer.is_valid():  
            serializer.save()  
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)  
        else:  
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)  
     
     

@api_view(['POST'])
def user_login(request):
    try:
        if request.method == 'POST':
        
            username = request.data.get('username')
            password = request.data.get('password')
            user = User.objects.get(username=username)
    except ObjectDoesNotExist:
            return Response({'error':'Username Not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if not (user.check_password(password)):
            return Response({'error': 'Incorrect Password'}, status=status.HTTP_400_BAD_REQUEST)
    if user:
            access_token = utl.generate_access_token(user)
            user.is_login=True #Set login is True
            user.is_active=True #Setting user is active or not
            user.token = str(access_token)
            user.save()

            user_data = UserSerializer(user).data
            return Response({'token': access_token, 'data':user_data}, status=status.HTTP_200_OK)

    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@utl.is_auth
def user_logout(request):
          user_id=request.user_id
          user=User.objects.get(id=user_id)
          user.is_login=False
          user.token=""
          user.save()
          return Response({"message":"you are logged out successfully"},status=status.HTTP_200_OK)


@api_view(['POST'])
@utl.is_auth
def deposit_amount(request):
    try:
        user_id = request.user_id  # This should be set by the is_auth decorator
        deposit_amount = request.data.get('deposit_amount')
        
        if not isinstance(deposit_amount, (int, float)) or deposit_amount <= 0:
            return Response({"error": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)
        
        user_instance = User.objects.get(id=user_id)
        
        # Update the user's initial amount  
        current_amount = user_instance.initial_amount
        new_initial_amount = current_amount + deposit_amount
        user_instance.initial_amount = new_initial_amount
        
        transaction = Transaction.objects.create(user_id=user_instance, deposit_amount=deposit_amount, withdraw_amount=0,transaction_type="Deposit")
        transaction.save()
        user_instance.save()

        return Response({"message": "Amount deposited successfully"}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
@api_view(['POST'])
@utl.is_auth     
def withdraw_amount(request):
    try:
        user_id = request.user_id  # This should be set by the is_auth decorator

        withdraw_amount = request.data.get('withdraw_amount')

        if not isinstance(withdraw_amount, (int, float)) or withdraw_amount <= 0:
            return Response({"error": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)
        
        user_instance=User.objects.get(id=user_id)
         
        #Update the users initial amount
        current_amount=user_instance.initial_amount
        new_initial_amount=current_amount-withdraw_amount
        user_instance.initial_amount =new_initial_amount    
        transaction = Transaction.objects.create(user_id=user_instance, deposit_amount=0, withdraw_amount=withdraw_amount,transaction_type="Withdraw")
        transaction.save()
        user_instance.save()  

        return Response({"message": "Amount Withdraw successfully"}, status=status.HTTP_200_OK)  

    except Exception as e:
        return Response({'error>>': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['POST'])
@utl.is_auth   
def get_balance(request):
    try:
        user_id=request.user_id
        user_instance=User.objects.get(id=user_id)
        balance= user_instance.initial_amount
        transaction = Transaction.objects.create(user_id=user_instance, deposit_amount=0, withdraw_amount=0,transaction_type="Balance check",get_balance=balance)
        user_instance.save()
        transaction.save()
        return Response({"balance": balance}, status=status.HTTP_200_OK)
    except Exception as e:
          return Response({'error>>': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])  
@utl.is_auth   
def show_transaction(request):
        try:
          user_id=request.user_id
          user=User.objects.get(id=user_id)

          transaction_type = request.query_params.get('transaction_type')
          if transaction_type in ['deposit','withdraw']:
               transaction=Transaction.objects.filter(user_id=user_id,transaction_type=transaction_type)
          else:
               transaction=request.Transaction.objects.filter(user_id=user_id)
    
          transaction_data = TransactionSerializer(transaction, many=True).data

          return Response({"transactions":transaction_data},status=status.HTTP_200_OK)
         
        except user.DoesNotExist():
             
             return Response({"Error":"User doesn't Exist"},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:

            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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


