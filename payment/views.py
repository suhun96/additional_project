from django.shortcuts import render
from django.views import View
from iamport    import Iamport
from my_settings import *
from django.http import *
import requests, json , uuid
from payment.models import *

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
            response = yamuzin_iamport.prepare_validate(merchant_uid= mid, amount = amount)
            
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

class GetMerchantUuidView(View):
    def get(self, request):
        new_uuid = uuid.uuid4()
        return JsonResponse({'message' : new_uuid})

class PaymentInquireView(View):
    def post(self, request):
        data = request.POST
        token = data['token']
        # imp_uid = data['imp_uid']
        merchant_uid = data['merchant_uid']

        url =  f"https://api.iamport.kr/payments/find/{merchant_uid}"
        headers = {'Authorization' : token}

        req = requests.post(url, headers= headers)
        res = req.json()
        print(res)
        if res['code'] == 0:
            context = {
                'imp_id' : res['response']['imp_uid'],
                'merchant_order' : res['response']['merchant_uid'],
                'amount' : res['response']['amount'],
                'status' : res['response']['status'],
                'pay_method'  : res['response']['pay_method'],
                'receipt_url' : res['response']['receipt_url']
            }

            return JsonResponse({'message' : context})
        if res['code'] == -1:
            message = res['message']
            print(message)
            return JsonResponse({'message' : message})


        # # 야무진 서버에 complete 정보 저장
        # new_success = ImportSuccess.objects.create(
        #     imp_uid = imp_uid,
        #     merchant_uid = merchant_uid
        # )





