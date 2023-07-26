from urllib import response
from django.shortcuts import render ,redirect 
from rest_framework import generics
from APİ.serializers import *
from .serializers import UserSerializer
from rest_framework.views import APIView , status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.http import HttpResponse
import jwt
from django.contrib.auth import logout
from django.conf import settings
import datetime

def bag(request):
    return render(request, "bag.html")


def menu(request):
    return render(request, "menu.html")

def HomePage(request):
    return render(request, "home.html")

def Register(request):
    return render(request, "register.html")

def loggout(request):
    logout(request)
    return render(request ,'logout.html')

def loggin(request) : 
    return render(request , "login.html")

class custom_login(APIView):
    def post(self,request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        SECRET_KEY = settings.SECRET_KEY

        access_token_expiration_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    
        refresh_token_expiration_time = datetime.datetime.utcnow() + datetime.timedelta(days=30)

        if user is not None and user.is_active:
            login(request, user)

            refresh_token_payload = {
                'username': username,
                'exp': refresh_token_expiration_time
                }
            
            access_token_payload = {
                'username': username,
                'exp': access_token_expiration_time
                }
            
            access_token = jwt.encode(access_token_payload, SECRET_KEY, algorithm='HS256')

            refresh_token = jwt.encode(refresh_token_payload, SECRET_KEY, algorithm='HS256')

            response_data = {
                'access_token': access_token,
                'refresh_token': refresh_token,
            }

            return JsonResponse(response_data)
        else:
            # Eğer kullanıcı bulunamaz veya hesap aktif değilse hata mesajı döndürün
            error_message = "Kullanıcı adı veya şifre yanlış veya hesap aktif değil."
            return JsonResponse({'error': error_message})
        

# def decode_jwt_token(request):
#     cookie_name = 'apiData'
#     cookie_data = request.COOKIES.get(cookie_name)
#     if cookie_data:
#         token = JsonResponse({'cookie_data': cookie_data})
#         try:
#             # JWT'yi çöz
#             decoded_token = jwt.decode(token, secret_key, algorithms=['HS256'])
#             return decoded_token
#         except jwt.ExpiredSignatureError:
#             # JWT'nin süresi dolmuş
#             return {'error': 'Token süresi dolmuş.'}
#         except jwt.InvalidTokenError:
#             # Geçersiz JWT
#             return {'error': 'Geçersiz Token.'}
#     else : 
#         return JsonResponse({'error': 'Çerez bulunamadı.'})



class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        print(user)
        return render(request, "login.html")


class ProductListCreateAPIView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, format=None):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return redirect('home-page')  
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class ProductRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    def get_object(self):
        id = self.kwargs["id"]
        return get_object_or_404(Product, id=id)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

def MyProd(request):
    prod = Product.objects.filter(user = user)
    

def showPrdAll(request):
    prod=Product.objects.all()
    return render(request, 'admin_product.html', {'prod': prod})
    

def showPrd(request):
    prodPermission=Product.objects.filter(permission = True)
    return render(request, 'products_list.html', {'prodPermission': prodPermission})


def add(request):
    return render(request, "add_product.html")
    

def update_permission(request, id):
    try:
        product = Product.objects.get(id=id)
        permission = not product.permission
        Product.objects.filter(id=id).update(permission=permission)
        return JsonResponse({'message': 'İşlem başarılı'})
    except Product.DoesNotExist:
        return JsonResponse({'message': 'Ürün bulunamadı'}, status=404)
    

