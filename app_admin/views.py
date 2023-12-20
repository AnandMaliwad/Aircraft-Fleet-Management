from django.shortcuts import render
from django.template.loader import get_template
import re
# Date Time
from datetime import datetime

# rest framework
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework import status,views
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

# Simple Json Web Token
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication

# URLS
from django.urls import reverse

# System Modules
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import (
    smart_str,
    force_str,
    smart_bytes,
    DjangoUnicodeDecodeError,
)

# JWT
import jwt

# Custom Util
# from app_Admin.util import SendEmail

from .models import User
from .serializer import (
    Userserializer,
    CreateAdminUserSerializers,
    AdminLoginSerializers,
)

# Create your views here.



class RegisterView(GenericAPIView):
    serializer_class = Userserializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]
    def post(self,request):
        serializer = Userserializer(request.data)
        
        if serializer.is_valid():
            serializer.save()
            user_data = serializer.data
            return Response({
                "responseCode": 200,
                "responseMessage": ("User is Successfully registered. send Email for Verifing on your registerd Email"),
                "responseData": user_data, },
                status=status.HTTP_201_CREATED)
        else:
            if serializer.errors.get('Password_Length'):
                return Response({
                    "responseCode": 400,
                    "responseMessage": ("Passwords must be bewtween 6  to 25 Characters.")},
                    status=status.HTTP_400_BAD_REQUEST)
            elif serializer.errors.get('user_tnc'):
                return Response({
                    "responseCode": 400,
                    "responseMessage": ("Please agree to all the term and condition")},
                    status=status.HTTP_400_BAD_REQUEST)
            # Exists
            elif serializer.errors.get('username_exists'):
                return Response({
                    "responseCode": 400,
                    "responseMessage": ("Username already is existed.")},
                    status=status.HTTP_400_BAD_REQUEST)
            elif serializer.errors.get('email_exists'):
                return Response({
                    "responseCode": 400,
                    "responseMessage": ("Email already is existed.")},
                    status=status.HTTP_400_BAD_REQUEST)
            elif serializer.errors.get('phone_exists'):
                return Response({
                    "responseCode": 400,
                    "responseMessage": ("Phone Number already is existed.")},
                    status=status.HTTP_400_BAD_REQUEST)
            # Validation
            elif serializer.errors.get('email_validation'):
                return Response({
                    "responseCode": 400,
                    "responseMessage": ("Please, Enter the Company E-Mail.")},
                    status=status.HTTP_400_BAD_REQUEST)
            elif serializer.errors.get('Phonedigit'):
                return Response({
                    "responseCode": 400,
                    "responseMessage": ("Phone number must be numeric")},
                    status=status.HTTP_400_BAD_REQUEST)
            elif serializer.errors.get('Phonelength'):
                return Response({
                    "responseCode": 400,
                    "responseMessage": ('Phone must be bewtween 8  to 12 Characters')},
                    status=status.HTTP_400_BAD_REQUEST)
            elif serializer.errors.get('FirstName_validation'):
                return Response({
                    "responseCode": 400,
                    "responseMessage": ('First Name must be alphbet.')},
                    status=status.HTTP_400_BAD_REQUEST)
            elif serializer.errors.get('Last_Name_validation'):
                return Response({
                    "responseCode": 400,
                    "responseMessage": ('Last Name must be alphbet.')},
                    status=status.HTTP_400_BAD_REQUEST)
            return Response({"responseCode": 400, "responseMessage": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class AdminRegisterView(GenericAPIView):
    serializer_class = CreateAdminUserSerializers
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]
    def post(self,request):
        serializer = Userserializer(data = request.data)
        
        if serializer.is_valid():
            serializer.save()
            user_data = serializer.data
            return Response({
                "responseCode": 200,
                "responseMessage": ("User is Successfully registered. send Email for Verifing on your registerd Email"),
                "responseData": user_data, },
                status=status.HTTP_201_CREATED)
        else:
            if serializer.errors.get('Password_Length'):
                return Response({
                    "responseCode": 400,
                    "responseMessage": ("Passwords must be bewtween 6  to 25 Characters.")},
                    status=status.HTTP_400_BAD_REQUEST)
            elif serializer.errors.get('user_tnc'):
                return Response({
                    "responseCode": 400,
                    "responseMessage": ("Please agree to all the term and condition")},
                    status=status.HTTP_400_BAD_REQUEST)
            # Exists
            elif serializer.errors.get('username_exists'):
                return Response({
                    "responseCode": 400,
                    "responseMessage": ("Username already is existed.")},
                    status=status.HTTP_400_BAD_REQUEST)
            elif serializer.errors.get('email_exists'):
                return Response({
                    "responseCode": 400,
                    "responseMessage": ("Email already is existed.")},
                    status=status.HTTP_400_BAD_REQUEST)
            elif serializer.errors.get('phone_exists'):
                return Response({
                    "responseCode": 400,
                    "responseMessage": ("Phone Number already is existed.")},
                    status=status.HTTP_400_BAD_REQUEST)
            # Validation
            elif serializer.errors.get('email_validation'):
                return Response({
                    "responseCode": 400,
                    "responseMessage": ("Please, Enter the Company E-Mail.")},
                    status=status.HTTP_400_BAD_REQUEST)
            elif serializer.errors.get('Phonedigit'):
                return Response({
                    "responseCode": 400,
                    "responseMessage": ("Phone number must be numeric")},
                    status=status.HTTP_400_BAD_REQUEST)
            elif serializer.errors.get('Phonelength'):
                return Response({
                    "responseCode": 400,
                    "responseMessage": ('Phone must be bewtween 8  to 12 Characters')},
                    status=status.HTTP_400_BAD_REQUEST)
            elif serializer.errors.get('FirstName_validation'):
                return Response({
                    "responseCode": 400,
                    "responseMessage": ('First Name must be alphbet.')},
                    status=status.HTTP_400_BAD_REQUEST)
            elif serializer.errors.get('Last_Name_validation'):
                return Response({
                    "responseCode": 400,
                    "responseMessage": ('Last Name must be alphbet.')},
                    status=status.HTTP_400_BAD_REQUEST)
            return Response({"responseCode": 400, "responseMessage": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


# Admin Login
class AdminLoginViews(GenericAPIView):

    serializer_class = AdminLoginSerializers
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]

    parser_classes = [MultiPartParser]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        # lang = self.request.headers["Accept-Language"]

        if serializer.is_valid(raise_exception=True):

            email = request.data["email"]
            GetUserIDLogin = User.objects.get(email=email).id
            temp = User.objects.filter(id=GetUserIDLogin).update(
                last_login=datetime.now())

            user = User.objects.get(id=GetUserIDLogin)

            user_Data = {"email": user.email,
                         "username": user.username,
                         "last_login": user.last_login}

            token = {'refresh': user.tokens()['refresh'],
                     'access': user.tokens()['access']}

            return Response({
                "responseCode": 200,
                "responseMessage": ("Login Successfully. {}").format(user.username),
                "responseData": user_Data,
                "token": token
            }, status=status.HTTP_200_OK)

        else:
            if serializer.errors.get("Invalid_Credentials"):
                return Response({
                    "responseCode": 400,
                    "responseMessage": ("Invalid credentials, try again")},
                    status=status.HTTP_400_BAD_REQUEST)

            elif serializer.errors.get("IsActive"):
                return Response({
                    "responseCode": 400,
                    "responseMessage": ("Your Account is disable. Please contact Admin")},
                    status=status.HTTP_400_BAD_REQUEST)

            elif serializer.errors.get("Isverify"):
                return Response({
                    "responseCode": 400,
                    "responseMessage": ("Email is not verified")},
                    status=status.HTTP_400_BAD_REQUEST)

            elif serializer.errors.get("Normal_User"):
                return Response({
                    "responseCode": 400,
                    "responseMessage": ("Admin will allow to login.")},
                    status=status.HTTP_400_BAD_REQUEST)

        return Response({"responseCode": 400, "responseMessage": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

