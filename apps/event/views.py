from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.http import JsonResponse
from django.conf import settings
import json

class Event(View):

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(Event, self).dispatch(request, *args, **kwargs)

    def post(self,request,*args,**kwargs):
        result = {"code": 400}
        data = json.loads(request.body.decode())
        if data:
            es = settings.ES
            res = es.index(index="2event",doc_type="test",body=data)
            # print(res)
            result["code"] = 200
        return JsonResponse(result)