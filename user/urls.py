# from django.contrib import admin
# from django.urls import path
#
# urlpatterns = [
#     path('admin/', admin.site.urls)
# ]


from .views import UserView, user_login,user_logout,deposit_amount,withdraw_amount
from django.urls import path

from .views import UserView, RefreshTokenView
  
urlpatterns = [  

    path('signup',UserView.as_view()),

    path('login/', user_login, name='login'),

    path('logout/' ,user_logout, name='logout'),
    
    # path('api/token/refresh/', RefreshTokenView.as_view(), name='token_refresh'),
    
    path('deposit/',deposit_amount,name='deposit'),
    path('withdraw/', withdraw_amount ,name='withdraw')

]  



