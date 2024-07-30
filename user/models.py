from django.db import models

from django.contrib.auth.hashers import make_password,check_password

#Creating user model

class User(models.Model):
    username=models.CharField(max_length=50,unique=True) 
    password=models.CharField(max_length=500)
    initial_amount=models.IntegerField(default=0)
    is_login=models.BooleanField(default=False)
    is_active=models.BooleanField(default=False) 
    token=models.CharField(max_length=200,default='None')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # deposit_amount=models.FloatField(default=0)
    

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    
    class Meta:
            # db_table = 'user'
            indexes = [
            models.Index(fields=['username','password']),
            ]
    

class Transaction(models.Model):
    user_id=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    deposit_amount=models.FloatField(max_length=20)

    withdraw_amount=models.FloatField(max_length=20)
    transaction_type=models.CharField(default="Blank",max_length=50)


    class Meta:
                # db_table = 'user'
                indexes = [
                models.Index(fields=['deposit_amount','withdraw_amount','transaction_type']),
                ]



    
