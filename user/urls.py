from django.urls import path, include

from user.views import *

urlpatterns = [
    path('hello',HelloView.as_view())
]