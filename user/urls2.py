from django.urls import path, include

from user.views import *

urlpatterns = [
    path('sign-in',KakaoSignInView.as_view()),
    path('log-in',KaKaoLogInView.as_view())
]