from django.db import models

class ImportRequest(models.Model):
    pg = models.CharField(max_length=100)
    pay_method = models.CharField(max_length=100)
    merchant_uid = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    amount = models.PositiveIntegerField()
    buyer_email = models.CharField(max_length=100)
    buyer_name = models.CharField(max_length=100)
    buyer_tel = models.CharField(max_length=100)
    buyer_postcodde = models.CharField(max_length=100)

    class Meta:
        db_table = 'iamport_req_sheet'

class ImportSuccess(models.Model):
    imp_uid = models.CharField(max_length=100)
    merchant_uid = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add= True)

    class Meta:
        db_table = 'iamport_success'
