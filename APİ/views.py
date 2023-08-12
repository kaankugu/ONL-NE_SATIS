from django.contrib.auth.hashers import make_password, check_password
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
from django.core.mail import send_mail
from django.http import  JsonResponse
from rest_framework import generics
from django.conf import settings
from APİ.serializers import *
from APİ.decorator import *
import datetime
import  random
import string
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

def forgetPassword(request,token):
    return render(request , "forgetPassword.html",{"token": token})
    
def sendEmailPage(request):
    return render(request , "sendEmail.html")

@admin_access_only
def showPrdAll(request):
    prod=Product.objects.all()
    images = ProductImage.objects.all()
    prod_images = {}
    for product in prod:
        images = ProductImage.objects.filter(product_id=product.id)
        prod_images[product.id] = images
    return render(request, 'admin_product.html', {'prod': prod , "image" : images})


def showPrd(request):
    return render(request, 'products_list.html' )


        
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
        
        

def decode_jwt_token(request):
     cookie_name = 'apiData'
     cookie_data = request.COOKIES.get(cookie_name)
     if cookie_data:
         token = JsonResponse({'cookie_data': cookie_data})
         try:
             # JWT'yi çöz
             decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
             return decoded_token
         except jwt.ExpiredSignatureError:
             return {'error': 'Token süresi dolmuş.'}
         except jwt.InvalidTokenError:
             return {'error': 'Geçersiz Token.'}
     else : 
         return JsonResponse({'error': 'Çerez bulunamadı.'})


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
    def get(self,request):
        products = Product.objects.all() 
        products_data = []

        for product in products:
            product_data = {
                "id": product.id,
                "title": product.title,
                "description": product.description,
                "price": product.price,
                "permission" : product.permission,
            }
            product_images = ProductImage.objects.filter(product=product)
            image_serializer = ProductImageSerializer( product_images, many=True)
            product_data["images"] = image_serializer.data
            
            products_data.append(product_data)
        return Response(data=products_data)


    parser_classes = [MultiPartParser]
    def post(self, request, format=None):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return redirect('home-page')  # Burada 'home-page' yerine doğru yönlendirme ismini kullanmalısınız.
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ProductRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    def get(self, request, *args, **kwargs):
        id = self.kwargs["id"]
        image =ProductImage.objects.filter(product_id = id)
        image_serializer = ProductImageSerializer( image, many=True)

        pro = Product.objects.filter(id=id)
        product_serializer = ProductSerializer(pro, many=True) 
        data = {
        'product_images': image_serializer.data,
        'product': product_serializer.data
        }
        print(data)
        return Response(data)
    
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


def generate_your_token_function():
    characters = string.digits
    token = ''.join(random.choice(characters) for _ in range(6))
    return token
 
 
def send_email_example(userEmail , token):
    subject = 'Subject of the Email'
    message  = "http://127.0.0.1:8000/updatePassword/"+token+"/"
    from_addr = settings.EMAIL_HOST_USER
    to_addr = [userEmail]
    try:
        send_mail(subject, message, from_addr, to_addr)
    except Exception as e:
        print("E-posta gönderirken bir hata oluştu:", e)


class SendEmail(APIView) : 
    def post(self,request) :
        email = request.data.get("email")   
        try:
            user = CustomUser.objects.get(email=email)
        except :
            return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            email_token = updateCode.objects.get(user=user)
            if not email_token.used and email_token.expire_date > timezone.now():
                email_token.used = True
                email_token.save()
        except updateCode.DoesNotExist:
            pass

        new_email_token, created = updateCode.objects.update_or_create(
            user=user,
            defaults={
                'token': generate_your_token_function(),
                'expire_date': timezone.now() + timezone.timedelta(hours=1),
                'used': False,
            }
        )

        response_data = {
        "success": True,
        "message": "E-posta gönderildi.",
        "redirectUrl": "/login/"
    }

        if created:  
            send_email_example(email , new_email_token.token)
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            send_email_example(email , new_email_token.token)
            return Response(response_data, status=status.HTTP_200_OK)
        


class updataPassword(APIView):
    def post(self, request):
        token = request.data.get("token")
        new_password = request.data.get("password")
        
        try:
            update = updateCode.objects.get(token=token)
            user = CustomUser.objects.get(id=update.user_id)
            time_left = update.expire_date - timezone.now()

            if time_left.total_seconds() > 0 and not update.used:
                if check_password(new_password, user.password):
                    return Response({"error": "New password cannot be the same as the old one"}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    hashed_password = make_password(new_password)
                    update.used = True
                    update.save()
                    user.password = hashed_password
                    user.save()
                    return Response(status=status.HTTP_200_OK)
            else:
                return Response({"error": "Token expired or already used"}, status=status.HTTP_400_BAD_REQUEST)
        except updateCode.DoesNotExist:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)