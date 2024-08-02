from .views import UserView, user_login,user_logout,deposit_amount,withdraw_amount,get_balance
from django.urls import path

from .views import UserView, RefreshTokenView
# from rest_framework.authtoken.views import obtain_auth_token
  
urlpatterns = [  

    path('signup',UserView.as_view()),
    path('login/', user_login, name='login'),
    path('logout/' ,user_logout, name='logout'),

    path('deposit/',deposit_amount,name='deposit'),
    path('withdraw/', withdraw_amount ,name='withdraw'),
    path('balance/', get_balance ,name='balance'),
]  



