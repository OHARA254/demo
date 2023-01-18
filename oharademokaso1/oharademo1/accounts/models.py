from django.db import models

from django.contrib.auth.models import AbstractUser, PermissionsMixin

class CustomUser(AbstractUser):

        class Meta:
                verbose_name_plural = 'ユーザー情報'
                db_table = 'custom_user'

        nickname = models.CharField(max_length=50,default=('大原'))
        address =models.CharField(max_length=300, null=True,blank=True)
        tel = models.CharField(max_length=50,null=True,blank=True)
        birth = models.CharField(max_length=50, null=True,blank=True)
        booking_kazu = models.IntegerField(default=0) 
        post_code = models.IntegerField(default=('4801234'))
        burakku = models.BooleanField(default=False)
    
