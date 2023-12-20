from django.db import models

# Custom User
from django.contrib.auth.models import AbstractUser, AnonymousUser

# Import UserManager Model
from .Usermanager import Usermanager

# JWT
from rest_framework_simplejwt.tokens import RefreshToken
# Create your models here.
from django.db import models

# Custom User
from django.contrib.auth.models import AbstractUser, AnonymousUser

# Import UserManager Model
from .Usermanager import Usermanager

# JWT
from rest_framework_simplejwt.tokens import RefreshToken
# Create your models here.


"""********************** Create your models here **********************"""

"""
******************************************************************************************************************
                                    User
******************************************************************************************************************
"""

AUTH_PROVIDERS = {'email':'email'}

#custom User
class User(AbstractUser):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    username = models.CharField(max_length=50, unique=True)
    country_code = models.CharField(max_length=6)
    phone = models.CharField(max_length=20, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=100)

    # Auth Provide
    auth_provider = models.CharField(max_length=255, blank=False, null=False,
                                     default=AUTH_PROVIDERS.get('email'))
    # Verify Account
    is_verify = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    # Account Delete
    is_deleted = models.BooleanField(default=False)

    # User Term & Condition
    user_tnc = models.BooleanField(default=False)

    # Admin
    is_staff = models.BooleanField(default=False)

    # Imp Fields
    last_login = models.DateTimeField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=50)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','phone','user_tnc']

    objects = Usermanager()

    def __unicode__(self):
        return self.id

    # Save Method with Capitalizen
    def save(self, *args, **kwargs):
        for field_name in [
            "first_name",
            "last_name",
        ]:
            val = getattr(self, field_name, False)
            if val:
                setattr(self, field_name, val.title())

        super(User, self).save(*args, **kwargs)

    # For Login - LoginSerializers

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {"refresh": str(refresh), "access": str(refresh.access_token)}

