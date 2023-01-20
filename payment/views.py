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

class PaymentFindView(View):
    def get(self, request):
        imp_uid = request.GET.get('imp_uid')
        response = yamuzin_iamport.find(imp_uid= imp_uid)

        return JsonResponse({'message' : response})

class PaymentPayCheckView(View):
    def get(self, request):
        imp_uid = request.GET.get('imp_uid')
        response = yamuzin_iamport.is_paid(100, imp_uid = imp_uid)

        return JsonResponse({'message' : response})

class ImportPaymentView(View):
    def post(self, request):
        data = request.POST
        print(data)

        pay_load = data['pay_load']
        imp_uid = data['imp_uid']
        
        # Step1. pay_load 저장
        new_payload = ImportPayload.objects.create(
            pg             = pay_load['pg'],     
            pay_method     = pay_load['pay_method'],
            merchant_uid   = pay_load['merchant_uid'],
            name           = pay_load['name'],
            amount         = pay_load['amount'],
            buyer_email    = pay_load['buyer_email'],
            buyer_name     = pay_load['buyer_name'],
            buyer_tel      = pay_load['buyer_tel'],
            buyer_postcode = pay_load['buyer_postcode'],
        )

        # Step2. pay_load 의 amount 와 pg서버에 등록된 금액 비교.
        check_amount = new_payload.amount
        is_paid = yamuzin_iamport.is_paid(amount= check_amount, imp_uid = imp_uid)

        if not is_paid == True:
            cancel_payment = yamuzin_iamport.cancel('금액 대조 불일치', imp_uid = imp_uid)
            return JsonResponse({'message' : '거래가 취소 되었습니다.'}, status = 403)

        # Step3. 성공한 결제 내역 DB에 저장.
        ImportSuccess.objects.create(
            imp_uid = imp_uid,
            merchant_uid = new_payload.merchant_uid
        )
        
        # Step4. 결제 내역 전송.
        context = yamuzin_iamport.find(imp_uid= imp_uid)

        return JsonResponse({'message' : '결제에 성공했습니다', '결제 내역' : context}, status = 200)
