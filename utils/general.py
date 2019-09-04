import geoip2.database
from random import Random
import hashlib
import os, re, json
from android.models import AndroidUserToken
from django.http import JsonResponse

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
geo_file = os.path.join(BASE_DIR,'utils') + os.sep + 'GeoLite2-Country-new.mmdb'

def check_token(fun):
    """
    装饰器
    检测客户端token是否合法
    """
    def inner(request, *args, **kwargs):
        ctoken = request.META.get("HTTP_TOKEN")
        if request.method == "POST":
            data = json.loads(request.body.decode())
            id = data.get("aid")
        else:
            id = request.GET.get("aid")

        if ctoken and id:
            token_obj = AndroidUserToken.objects.filter(token=ctoken).first()
            if token_obj:
                client_id = token_obj.client.aid
                if client_id == id:
                    return fun(request, *args, **kwargs)

        return JsonResponse("token验证失败",safe=False)

    return inner

def get_ip(request):
    """
    根据客户端request获取客户端ip
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]#所以这里是真实的ip
    else:
        ip = request.META.get('REMOTE_ADDR')#这里获得代理ip
    return ip.strip()

def internal(ipadd):
    """
    判断是否是私网IP
    """
    a=re.findall(r'^((192\.168)|(10\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d))|(172\.(1[6-9]|2[0-9]|3[0-1])))\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)$',ipadd)
    if a:
        return True
    else:
        return False

def get_country(ip):
    """
    根据ip返回国家代码
    :param ip:
    :return: 国家代码
    """
    reader =geoip2.database.Reader(geo_file)
    try:
        response = reader.country(ip)
    except Exception as e:
        # logger.error("ip: %s解析失败,%s" % (ip, str(e)))
        if internal(ip):
            return "private"
        else:
            return "nofind"
    else:
        country = response.country.iso_code
        return country

def create_salt(length=4):
    """
    获取4位随机数组成的salt值
    """
    salt = ""
    chars = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789"
    len_chars = len(chars) - 1
    random = Random()
    for i in range(length):
        salt += chars[random.randint(0,len_chars)]
    return salt

def create_md5(s,salt):
    """
    md5 加盐加密
    """
    md5_obj = hashlib.md5()
    md5_obj.update((s + salt).encode("utf-8"))
    return md5_obj.hexdigest()