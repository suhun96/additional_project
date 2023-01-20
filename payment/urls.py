from django.urls import path, include

from payment.views import *

urlpatterns = [
    path('resi',PaymentInfoResisterView.as_view()),
    path('check',PaymentInfoCheckView.as_view()),
    path('token',GetAcessTokenView.as_view()),
    path('merchant-uid',GetMerchantUuidView.as_view()),
    path('transaction',PaymentInquireView.as_view()),
    path('find',PaymentFindView.as_view()),
    path('is-paid',PaymentPayCheckView.as_view()),
]