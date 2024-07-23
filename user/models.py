from django.db import models

#Creating user model

class User(models.Model):
    username=models.CharField(max_length=50,unique=True)
    password=models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
            # db_table = 'user'
            indexes = [
            models.Index(fields=['username','password']),
            ]


    
