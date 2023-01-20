import json
from user.models        import *
from django.views       import View
from django.http        import JsonResponse
# Create your views here.

class HelloView1(View):
    def get(self, request):
        return JsonResponse({'message' : 'Your success is up to your efforts. 👍'})

class HelloView2(View):
    def get(self, request):
        return JsonResponse({'message' : 'The road to success and the road to failure are almost exactly the same. 👍'})

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
            return JsonResponse({'message' : '회원가입이 완료되었습니다.'}, status = 200)
        except Exception:
            return JsonResponse({'message' : '회원가입이 실패했습니다.'}, status = 403)

class KaKaoLogInView(View):
    def get(self, request):
        kakao_email = request.GET.get('kakao_email')

        try:
            target_user = KakaoUser.objects.get(email = kakao_email)
            profile = {
                '이름'    : target_user.name,
                '전화번호' : target_user.tel,
                '우편번호' : target_user.post_code
            }
            
            return JsonResponse({'profile' : profile}, status = 200)
        except KakaoUser.DoesNotExist:
            return JsonResponse({'message' : '존재하지 않는 유저입니다.'}, status = 403)
