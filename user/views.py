from django.shortcuts import render
from django.views       import View
from django.http        import JsonResponse
# Create your views here.

class HelloView1(View):
    def get(self, request):
        return JsonResponse({'message' : '승훈님 기대하겠습니다.'})

class HelloView2(View):
    def get(self, request):
        return JsonResponse({'message' : '민기님 화이팅!'})
