from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Users
from .serializers import UsersSerializer
from rest_framework.parsers import JSONParser
import jwt
import json, datetime

KEY = 'SecReTkeY'

# Create your views here.

def authentication(token):
    token_decoded = jwt.decode(token, KEY, algorithms='HS256')

    try:
        obj = Users.objects.get(id=token_decoded['id'], pw=token_decoded['pw'])
    except:
        return 401
    else:
        return 200

@csrf_exempt
def refresh_token(request):
    token = json.loads(request.body)['refresh_token']

    try:
        obj = Users.objects.get(refresh_token=token)
    except:
        return HttpResponse(status=401)
    else:
        access_token = jwt.encode({'update': str(datetime.datetime.now()), 'id': obj.id, 'pw': obj.pw}, KEY, algorithm='HS256')
    return JsonResponse({'status': '200', 'data': {'access_token': access_token}}, status=200)

@csrf_exempt
def users_list(request):
    try:
        auth_code = authentication(request.COOKIES['access_token'])
    except:
        return HttpResponse(status=401)
    else:
        if auth_code == 401:
            return HttpResponse(status=401)

    if request.method == 'GET':
        searchId = request.GET.get('search', '')
        query_set = Users.objects.filter(id__contains=searchId).order_by('id')
        serializer = UsersSerializer(query_set, many=True)

        data = {'users': []}
        for i in serializer.data:
            data['users'].append(dict(i))

        return JsonResponse({'data': data}, safe=False, status=200)

@csrf_exempt
def signup(request):
    data = JSONParser().parse(request)
    serializer = UsersSerializer(data = data)

    if serializer.is_valid():
        serializer.save()
        return JsonResponse({'status': 200}, status=201)
    return JsonResponse({'message': serializer.errors, 'status': 400})

@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        search_id = data['id']
        try:
            obj = Users.objects.get(id = search_id)
        except:
            return HttpResponse(status=400)
        else:
            now_time = str(datetime.datetime.now())
            access_token = jwt.encode({'update': now_time, 'id': data['id'], 'pw': data['pw']}, KEY, algorithm='HS256')
            refresh_token = jwt.encode({'update': now_time, 'id': data['id']}, KEY, algorithm='HS256')
            obj.refresh_token = refresh_token
            obj.save()

            return JsonResponse({'status': '200', 'data': {'access_token': access_token, 'refresh_token': refresh_token}}, status=200)
