# from django.contrib import admin
# from django.urls import path
#
# urlpatterns = [
#     path('admin/', admin.site.urls)
# ]


from .views import UserView, user_login
from django.urls import path

from .views import UserView, RefreshTokenView
  
urlpatterns = [  

    path('signup',UserView.as_view()),

    path('login/', user_login, name='login'),
    
    path('api/token/refresh/', RefreshTokenView.as_view(), name='token_refresh'),
    
]  



