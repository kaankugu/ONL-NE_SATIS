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


def bag(request):
    return render(request, "bag.html")

def HomePage(request):
    return render(request, "home.html")

def Register(request):
    return render(request, "register.html")

def loggout(request):
    return render(request ,'logout.html')

def loggin(request) : 
    return render(request , "login.html")


@csrf_exempt
@require_POST
def custom_login(request):
    # Kullanıcıdan gelen verileri alalım
    username = request.POST.get('username')
    password = request.POST.get('password')

    # Kullanıcıyı doğrulayalım
    user = authenticate(username=username, password=password)

    if user is not None and user.is_active:
        # Kullanıcı başarılı bir şekilde giriş yaptı
        login(request, user)

        # RefreshToken 
        refresh = RefreshToken.for_user(user)

        # Access token ve refresh token'ları alalım
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        response = HttpResponse()

        response.set_cookie('access_token', access_token, max_age=3600)  
        response.set_cookie('refresh_token', refresh_token, max_age=3600 * 24 * 30)  
        # Tokenları JSON formatında döndürelim
        response_data = {
            'access_token': access_token,
            'refresh_token': refresh_token,
        }
        return JsonResponse(response_data)

    else:
        return JsonResponse({'error': 'Invalid username or password'}, status=400)


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



def showPrdAll(request):
    prod=Product.objects.all()
    return render(request, 'admin_product.html', {'prod': prod})
    

def showPrd(request):
    prodPermission=Product.objects.filter(permission = True)
    return render(request, 'products_list.html', {'prodPermission': prodPermission})


def add(request):
    return render(request, "add_product.html")
    
def update_permission(request,id):
    prod =Product.objects.get(id=id)
    permission=not prod.permission

    Product.objects.filter(id=id).update(permission=permission)
    
    return JsonResponse({'message': 'İşlem başarılı'})
