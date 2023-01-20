from django.shortcuts import render
from django.views import View
from iamport    import Iamport
from my_settings import *
from django.http import *
import requests, json

class PaymentInfoResisterView(View):
    def get(self, request):
        mid = 'merchant_test'
        amount = 12000

        try:
            response = yamuzin_iamport.prepare(amount= amount, merchant_uid= mid)
            
            return JsonResponse({'message' : response})
        except Iamport.ResponseError as e:
            return JsonResponse({'message' : e}, 403)
        except Iamport.HttpError as http_error:
            return JsonResponse({'message' : 'http error'}, 403)

class PaymentInfoCheckView(View):
    def get(self, request):
        mid = 'merchant_test'
        amount = 12000
        try:
            response = yamuzin_iamport.prepare_validate(amount= amount, merchant_uid= mid)
            
            return JsonResponse({'message' : response})        
        except Iamport.ResponseError as e:
            return JsonResponse({'message' : e}, 403)
        except Iamport.HttpError as http_error:
            return JsonResponse({'message' : 'http error'}, 403)

class GetAcessTokenView(View):
    def get_token(self):
        access_data = {
            'imp_key': IAMPORT_KEY,
            'imp_secret': IAMPORT_SECRET_KEY
        }

        url = 'https://api.iamport.kr/users/getToken'

        req = requests.post(url, data=access_data)
        access_res = req.json()

        if access_res['code'] == 0:
            token =  access_res['response']['access_token']
            return token
        else:
            return None

    def get(self, request):
        
        token = self.get_token()
        
        if token == None:
            return JsonResponse({'message' : 'error'}) 
        return JsonResponse({'message' : token})
