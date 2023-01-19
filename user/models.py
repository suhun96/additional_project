from django.db import models

# Create your models here.

class KakaoUser(models.Model):
    email = models.CharField(max_length = 100, blank= False)
    name  = models.CharField(max_length = 60, blank= False)
    tel   = models.CharField(max_length = 20, blank= False)
    created_at = models.DateTimeField(auto_now_add= True)

    class Meta:
        db_table = 'kakao_users'
