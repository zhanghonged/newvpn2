from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.generic.base import View
from django.views.decorators.csrf import csrf_exempt
from utils.general import get_ip, get_country, create_salt, create_md5
from .models import AndroidUser, AndroidUserToken
import json
import logging

logger = logging.getLogger('one')
logger2 = logging.getLogger('two')
logger3 = logging.getLogger(__name__)


class ClientUser(View):
    http_method_names = ['post', 'get']
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(ClientUser, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return JsonResponse("abc",safe=False)

    def post(self, request, *args, **kwargs):

        data = json.loads(request.body.decode())
        aid = data.get("aid")
        gaid = data.get("gaid")
        operators = data.get("operator")
        is_wifi = data.get("is_wifi")

        re_dict = {}
        if aid:
            ip = get_ip(request)
            try:
                ip
            except NameError:
                ip = ""
                country = ""
            else:
                country = get_country(ip)


            obj = AndroidUser.objects.filter(aid__exact=aid)
            if len(obj) == 0:
                new_obj = AndroidUser.objects.create(
                            aid = aid,
                            gaid = gaid,
                            operators = operators,
                            is_wifi = is_wifi,
                            ip = ip,
                            country = country,
                            req_num = 1
                            )
                # 生成token
                re_dict = generateToken(aid,new_obj)

            else:
                client = obj[0]
                client.req_num += 1
                client.ip = ip
                client.country = country
                client.save()
                re_dict = generateToken(aid, client)

        return JsonResponse(re_dict)

def generateToken(id,cliet_obj):
    """
    :param id: 设备id
    :param cliet_obj: 设备对象
    :return: 生成token，更新token表
    """
    re_dict = {}
    salt = create_salt(8)
    token = create_md5(str(id), salt)
    # 更新token表
    try:
        AndroidUserToken.objects.update_or_create(client=cliet_obj, defaults={"token": token,"salt":salt})
    except Exception as e:
        print(str(e))
        re_dict["token"] = ""
    else:
        re_dict["token"] = token

    return re_dict

from utils.general import check_token

class Test(View):
    http_method_names = ['post', 'get']

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(Test, self).dispatch(request, *args, **kwargs)

    @method_decorator(check_token, name='get')
    def get(self,request,*args,**kwargs):
        logger.info("get log.")
        return JsonResponse({"code":200,"method":"get"})

    @method_decorator(check_token, name='post')
    def post(self,request,*args,**kwargs):
        logger2.error("post logs.")
        logger3.error("logger3....")
        return JsonResponse({"code":200,"method":"post"})

@check_token
def test2(request):
    return JsonResponse({"test":"ok"})