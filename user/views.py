import json
from user.models        import *
from django.views       import View
from django.http        import JsonResponse
# Create your views here.

class HelloView1(View):
    def get(self, request):
        return JsonResponse({'message' : 'Your success is up to your efforts. π'})

class HelloView2(View):
    def get(self, request):
        return JsonResponse({'message' : 'The road to success and the road to failure are almost exactly the same. π'})

class KakaoSignInView(View):
    def post(self, request):
        data = json.loads(request.body)
        kakao_data = data.get('kakao_data')
        try:
            KakaoUser.objects.create(
                email = kakao_data['email'],    
                name  = kakao_data['name'],    
                tel   = kakao_data['tel'],
                post_code = '123-002'
            )
            return JsonResponse({'message' : 'νμκ°μμ΄ μλ£λμμ΅λλ€.'}, status = 200)
        except Exception:
            return JsonResponse({'message' : 'νμκ°μμ΄ μ€ν¨νμ΅λλ€.'}, status = 403)

class KaKaoLogInView(View):
    def get(self, request):
        kakao_email = request.GET.get('kakao_email')

        try:
            target_user = KakaoUser.objects.get(email = kakao_email)
            profile = {
                'μ΄λ¦'    : target_user.name,
                'μ νλ²νΈ' : target_user.tel,
                'μ°νΈλ²νΈ' : target_user.post_code
            }
            
            return JsonResponse({'profile' : profile}, status = 200)
        except KakaoUser.DoesNotExist:
            return JsonResponse({'message' : 'μ‘΄μ¬νμ§ μλ μ μ μλλ€.'}, status = 403)
