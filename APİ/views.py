from django.shortcuts import render
from rest_framework import generics
from APİ.serializers import RegisterSerializer
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken






class CustomLoginView(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        
        if user is None or not user.is_active:
            return Response({'error': 'Invalid username or password'}, status=400)

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        user_data = {
            'id': user.id,
            'username': user.username,
        }

        return Response({
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': user_data,
        })


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        print(user)
        return render(request, "login.html")




def HomePage(request):
    return render(request, "home.html")

def Register(request):
    return render(request, "register.html")

def logout(request):
    logout(request)
    return redirect('login')

def loggin(request) : 
    return render(request , "login.html")