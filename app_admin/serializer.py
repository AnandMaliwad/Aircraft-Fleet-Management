from rest_framework import serializers
from .models  import User

# Rest Frame Work - Authentication Failed
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.password_validation import validate_password

# Regular Expression
import re

# Authentication
from django.contrib import auth


class Userserializer(serializers.ModelSerializer):
    password = serializers.CharField(
        min_length=6,max_length=20,write_only=True)
    
    class Meta:
        model = User
        fields = ['first_name','last_name','username','country_code',
                  'phone','email','password','user_tnc','last_login']

        read_only_fields = ['last_login']
    
    def validate(self, validated_data):
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        username = validated_data.get('username')
        country_code = validated_data.get('country_code')
        phone = validated_data.get('phone')
        email = validated_data.get('email')
        password = validated_data.get('password')
        user_tnc = validated_data.get('user_tnc')

        # Exists Data
        username_exists = User.objects.filter(username=username)
        email_exists = User.objects.filter(email=email)
        phone_exists = User.objects.filter(phone=phone)

        
        if len(password) < 6 or len(password) > 25:
            raise serializers.ValidationError({"Password_Length":(
                "Passwords must be bewtween 6  to 25 Characters.")})
        elif user_tnc != True:
            raise serializers.ValidationError(
                {"user_tnc": ("Please agree to all the term and condition")})
        # Exists
        elif username_exists:
            raise serializers.ValidationError(
                {"username_exists": ("username already is existed.")})
        elif email_exists:
            raise serializers.ValidationError(
                {"email_exists": ("Email is already existed.")})
        elif phone_exists:
            raise serializers.ValidationError(
                {'phone_exists': ("Phone Number is already exists.")})
        # Validation
        # Email
        # elif not re.match('^[a-zA-Z].[a-zA-Z\.]*@archesoftronix.com', email):
        elif not re.match('^[a-zA-Z0-9_+&*-]+(?:\\.[a-zA-Z0-9_+&*-]+)*@(?:[a-zA-Z0-9-]+\\.)+[a-zA-Z]{2,7}$', email):
            raise serializers.ValidationError(
                {'email_validation': ("Please, Enter the Company E-Mail.")})
        # Username
        elif not re.match('^[a-zA-Z0-9].[a-zA-Z0-9\.\-_]*[a-zA-Z0-9]$', username):
            raise serializers.ValidationError(
                {"Username_validation": ("Username must be Alphanumeric & Special Character ('-','.','_')")})
        # Country Code
        elif not re.match('^[+][0-9]*$', country_code):
            raise serializers.ValidationError(
                {"Country Code":("Country must be start with '+', and Numeric")})
        # Phone
        # Phone Digit
        elif not phone.isdigit():
            raise serializers.ValidationError(
                {"Phonedigit": ("Phone number must be numeric")})
        # Phone Length
        elif len(phone) < 8 or len(phone) > 12:
            raise serializers.ValidationError(
                {"Phonelength": ("Phone must be bewtween 8  to 12 Characters")})
        # First Name
        elif not re.match("^[a-zA-Z]*$", first_name):
            raise serializers.ValidationError(
                {"FirstName_validation": ("First Name must be alphbet.")})
        # Last Name
        elif not re.match("^[a-zA-Z]*$", last_name):
            raise serializers.ValidationError(
                {"Last_Name_validation": ("Last Name must be alphbet.")})
        
        return validated_data
    


class CreateAdminUserSerializers(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, max_length=50,
                                     write_only=True, required=True, style={"input_type": "password",
                                                                            "placeholder": "Password"},)

    class Meta:
        model = User

        fields = [
            'email', 'username', 'country_code', 'phone', 'password', 'first_name', 'last_name', 'user_tnc', 'last_login',
        ]

        read_only_fields = ['last_login',]

    # Validate Data

    def validate(self, validated_data):
        email = validated_data.get('email')
        username = validated_data.get('username')
        country_code = validated_data.get('country_code')
        phone = validated_data.get('phone')
        password = validated_data.get('password')
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        user_tnc = validated_data.get('user_tnc')

        # Exists Data
        username_exists = User.objects.filter(username=username)
        email_exists = User.objects.filter(email=email)
        phone_exists = User.objects.filter(phone=phone)

        if len(password) < 6 or len(password) > 25:
            raise serializers.ValidationError({"Password_Length": (
                "Passwords must be bewtween 6  to 25 Characters.")})
        elif user_tnc != True:
            raise serializers.ValidationError(
                {"user_tnc": ("Please agree to all the term and condition")})
        # Exists
        elif username_exists:
            raise serializers.ValidationError(
                {"username_exists": ("username already is existed.")})
        elif email_exists:
            raise serializers.ValidationError(
                {"email_exists": ("Email is already existed.")})
        elif phone_exists:
            raise serializers.ValidationError(
                {'phone_exists': ("Phone Number is already exists.")})
        # Validation
        # Email
        elif not re.match('^[a-zA-Z].[a-zA-Z\.]*@archesoftronix.com', email):
            raise serializers.ValidationError(
                {'email_validation': ("Please, Enter the Company E-Mail.")})
        # Username
        elif not re.match('^[a-zA-Z0-9].[a-zA-Z0-9\.\-_]*[a-zA-Z0-9]$', username):
            raise serializers.ValidationError(
                {"Username_validation": ("Username must be Alphanumeric & Special Character ('-','.','_')")})
        # Country Code
        elif not re.match('^[+][0-9]*$', country_code):
            raise serializers.ValidationError(
                {"Country Code": ("Country must be start with '+', and Numeric")})
        # Phone
        # Phone Digit
        elif not phone.isdigit():
            raise serializers.ValidationError(
                {"Phonedigit": ("Phone number must be numeric")})
        # Phone Length
        elif len(phone) < 8 or len(phone) > 12:
            raise serializers.ValidationError(
                {"Phonelength": ("Phone must be bewtween 8  to 12 Characters")})
        # First Name
        elif not re.match("^[a-zA-Z]*$", first_name):
            raise serializers.ValidationError(
                {"FirstName_validation": ("First Name must be alphbet.")})
        # Last Name
        elif not re.match("^[a-zA-Z]*$", last_name):
            raise serializers.ValidationError(
                {"Last_Name_validation": ("Last Name must be alphbet.")})

        return validated_data

    # Create user
    def create(self, validated_data):

        return User.objects.create_superuser(**validated_data)



# Admin Login
class AdminLoginSerializers(serializers.ModelSerializer):

    email = serializers.EmailField(max_length=100)
    password = serializers.CharField(max_length=25, min_length=6,
                                     write_only=True)

    username = serializers.CharField(max_length=100, read_only=True)
    username = serializers.CharField(max_length=100, read_only=True)
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = User.objects.get(email=obj['phone'])
        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }

    class Meta:
        model = User
        fields = ["email", "password", "username", "country_code",
                  "phone", 'tokens',  'last_login']

        read_only_fields = ['country_code', 'phone', 'last_login']

    def validate(self, attrs):
        email = attrs.get("email", "")
        password = attrs.get("password", "")
        # filtered_user_by_email = User.objects.filter(email=email)

        user = auth.authenticate(email=email, password=password)

        # if filtered_user_by_email.exists() and filtered_user_by_email[0].auth_provider != 'email':
        #     raise AuthenticationFailed(
        #         detail=_('Please continue your login using') + filtered_user_by_email[0].auth_provider)

        # Raise AuthenticationFailed
        if not user:
            raise serializers.ValidationError(
                {"Invalid_Credentials": ('Invalid credentials, try again')})
        elif not user.is_active:
            raise serializers.ValidationError(
                {"IsActive": ('Your Account is disable. Please contact Admin')})
        elif not user.is_verify:
            raise serializers.ValidationError(
                {"Isverify": ('Email is not verified')})
        elif not user.is_staff or not user.is_superuser:
            raise serializers.ValidationError(
                {"Normal_User": ('Only, Admin will allow to login.')})

        return {
            "username": user.username,
            "email": user.email,
            "tokens": user.tokens,

        }