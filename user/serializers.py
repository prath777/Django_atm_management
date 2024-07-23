from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    username =serializers.CharField(max_length=200,required=True)
    password =serializers.CharField(max_length =200,required=True)

    
    class Meta:  
            model = User
            # fields = ('__all__')
            fields=('username','password')
            read_only_fields =['created_at','updated_at'] 

