from django.shortcuts import render
from django.views       import View
from django.http        import JsonResponse
# Create your views here.

class HelloView1(View):
    def get(self, request):
        return JsonResponse({'message' : 'Your success is up to your efforts. 👍'})

class HelloView2(View):
    def get(self, request):
        return JsonResponse({'message' : 'The road to success and the road to failure are almost exactly the same. 👍'})
