from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    username =serializers.CharField(max_length=200,required=True)
    initial_amount=serializers.IntegerField(required=True)


    
    class Meta:  
            model = User
            # fields = ('__all__')
            fields=('username','password','initial_amount','is_login','is_active','token',)
            # read_only_fields =['created_at','updated_at'] 
            extra_kwargs = {'password': {'write_only': True}}  # Password should not be readable
            
    
    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            initial_amount=validated_data['initial_amount']
        )
        user.set_password(validated_data['password'])  # This hashes the password
        user.save()
        return user
    # def __str__(self):
    #      return self.name
    # def __str__(self):
    #      return self.initial_amount
