from django.urls import path
from app_accounts.views import *


urlpatterns = [
    path('candi-register/',candiateSignUp,name='profile'),
    path('verify/',candiateVerify,name='verify-candi'),
    path('login/',candiateLogIn,name='login'),
    path('signout/',logoutView,name='logoff'),
    path('revier-register/',reviewersignUp,name='reviewr'),
    path('revier-verify/',reviwerverify,name='verify-revier'),
    path('revier-login/',reviwerlogIn,name='login-revier'),
    path('',index),
    path('user_detail/<blog_id>/',candid_details,name='user_detail'),
    path('add-comment/<blog_id>/',addComment,name='add-comment'),
    path('home/',home),
]