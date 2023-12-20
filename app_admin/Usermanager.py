# cretaing Custom User Model
from django.contrib.auth.models import BaseUserManager

class Usermanager(BaseUserManager):
    # create User
    def create_user(self,email,username,phone='',password=None,**extra_fields):
        
        # condition to check value is not null.
        if not username:
            raise ValueError("Username must not be required.")
        if not phone:
            raise ValueError("Phone No. is required.")
        if not email:
            raise ValueError("Email is required.")
        
        # for saving
        user = self.model(email=self.normalize_email(email),username=username,
                          phone=phone,**extra_fields)
        
        # passwords
        user.set_password(password)
        user.is_active = True
        user.is_verify = False
        user.save()
        return user
    
    # create superuser
    def create_superuser(self,email,username,phone,password=None,**extra_fields):
        if not password:
            raise ValueError("password should not be None.")

        user = self.create_user(email,username,phone,password)

        user.is_active = True
        user.is_verify = True
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user