from django.views import View
from django.contrib.auth.models import User
from django.http import JsonResponse
import json


class UsernameValidation(View):
    def post(self,request):
        data = json.loads(request.body)
        username = data['username']

        if not str(username).isalnum():
            return JsonResponse({'username_error':'Username should only contain alphanumeric characters'},status=400)
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error':'Username Exists'},status=409)

        return JsonResponse({'username_valid':True})

