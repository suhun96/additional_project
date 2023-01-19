from django.urls import path, include

from user.views import *

urlpatterns = [
    path('hello-moon',HelloView1.as_view()),
    path('hello-kim',HelloView1.as_view())
]