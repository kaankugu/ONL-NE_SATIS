from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView , status
from django.shortcuts import  get_object_or_404
from django.shortcuts import render , redirect 
from rest_framework.response import  Response
from django.contrib.auth import authenticate
from .serializers import UserSerializer
from django.contrib.auth import logout
from django.http import  JsonResponse
from rest_framework import generics
from django.conf import settings
from APİ.serializers import *
from APİ.decorator import *
import datetime
import jwt


@login_required(login_url='/login/')
def bag(request):
    return render(request, "bag.html")

def No_page(request,exception): 
    return render(request, "404.html", {})


def menu(request):
    return render(request, "menu.html")

def HomePage(request):
    return render(request, "home.html")


def loggin(request) : 
    return render(request , "login.html")


def Register(request):
    return render(request, "register.html")


def loggout(request):
    logout(request)
    return render(request ,'logout.html')


@superuser_access_only
def update(request): 
    return render(request , "superuser_permission.html")



@login_required(login_url='/login/')
def add(request):
    return render(request, "add_product.html")
    

@admin_access_only
def showPrdAll(request):
    prod=Product.objects.all()
    return render(request, 'admin_product.html', {'prod': prod})


def showPrd(request):
    prodPermission=Product.objects.filter(permission = True)
    return render(request, 'products_list.html', {'prodPermission': prodPermission})


        
class custom_login(APIView):
    def post(self,request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(username=email, password=password)
        SECRET_KEY = settings.SECRET_KEY

        access_token_expiration_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    
        refresh_token_expiration_time = datetime.datetime.utcnow() + datetime.timedelta(days=30)

        if user :
            login(request, user)

            refresh_token_payload = {
                'email':email ,
                'exp': refresh_token_expiration_time
                }
            
            access_token_payload = {
                'email': email,
                'exp': access_token_expiration_time
                }
            
            access_token = jwt.encode(access_token_payload, SECRET_KEY, algorithm='HS256')

            refresh_token = jwt.encode(refresh_token_payload, SECRET_KEY, algorithm='HS256')

            response_data = {
                'access_token': access_token,
                'refresh_token': refresh_token,
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Geçersiz eposta veya parola.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        

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


class All_User(APIView) :
    def get(self, request):
        user = CustomUser.objects.all()
        serializer = UserSerializer(user , many = True)
        return Response(serializer.data)


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return render(request, "login.html")
    

class ProductListCreateAPIView(APIView):
    parser_classes = [MultiPartParser]
    def post(self, request):
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



class update_permission(APIView):
    def post(self, request):
        try:
            id = request.data.get("id")
            product = Product.objects.get(id=id)
            permission = not product.permission
            Product.objects.filter(id=id).update(permission=permission)
            return JsonResponse({'message': 'İşlem başarılı'})
        except Product.DoesNotExist:
            return JsonResponse({'message': 'Ürün bulunamadı'}, status=404)
        

class UpdateUserAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        typePerm = request.data.get('typePerm')
        print(email ,  typePerm)
        if not email or not typePerm:
            return JsonResponse({'message': 'E-posta ve yetki türü bilgilerini eksiksiz gönderin.'}, status=400)

        try:
            user = CustomUser.objects.get(email=email)
            if typePerm == "admin":
                user.is_admin = not user.is_admin
            elif typePerm == "superuser":
                user.is_superuser = not user.is_superuser
            elif typePerm == "seller":
                user.is_seller = not user.is_seller
            else:
                return JsonResponse({'message': 'Geçersiz yetki türü'}, status=400)

            user.save()
            return JsonResponse({'message': 'İşlem başarılı'})
        except CustomUser.DoesNotExist:
            return JsonResponse({'message': 'Kullanıcı bulunamadı'}, status=404)


