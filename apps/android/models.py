from django.db import models

# Create your models here.
class AndroidUser(models.Model):
    """
    android客户端用户
    """
    aid         = models.CharField("aid名称", max_length=128, unique=True, db_index=True)
    gaid        = models.CharField("gid名称",max_length=128, blank=True, null=True)
    ip          = models.CharField("客户ip", max_length=64, blank=True, null=True)
    country     = models.CharField("国家", max_length=32, db_index=True, blank=True, null=True)
    operators   = models.CharField("客户端网络运营商", db_index=True, max_length=128, blank=True, null=True)
    is_wifi     = models.BooleanField("客户端wifi状态")
    req_num     = models.IntegerField("请求次数")
    create_time = models.DateTimeField("记录时间", auto_now_add=True)
    last_access = models.DateTimeField("上一次请求时间", auto_now=True)

    def __str__(self):
        return self.aid

    class Meta:
        db_table = "clients"


class AndroidUserToken(models.Model):
    """
    android客户端用户 token
    """
    client = models.OneToOneField(AndroidUser,on_delete=models.CASCADE)
    token  = models.CharField("token", max_length=64)
    salt   = models.CharField("加密盐", max_length=64)

    def __str__(self):
        return self.token

    class Meta:
        db_table = "clients_token"