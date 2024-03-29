from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from rest_framework_simplejwt.tokens import RefreshToken 
class UserManager(BaseUserManager):
    
    def create_user(self,username,email,password=None):
        
        if username is None:
            raise TypeError('Users should have a username')
        if email is None:
            raise TypeError('Users should have a email')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self,username,email,password=None):
        
        if password is None:
            raise TypeError('Password should not be none')

        user = self.create_user(username,email,password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user 

class User(AbstractBaseUser,PermissionsMixin):
    username = models.CharField(max_length=255, db_index=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    photo = models.ImageField(upload_to='images/',blank=True,null=True)
    company = models.CharField(max_length=50,blank=True,null=True)
    verification_code = models.CharField(max_length=6, null=True)
    reset_code = models.CharField(max_length=6, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    selected_country = models.ForeignKey('gestiondesproduits.Pays', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    objects = UserManager()
    
    def __str__(self):
        return self.email 
    
    def tokens(self):
        refresh=RefreshToken.for_user(self)
        return {
            'refresh':str(refresh),
            'access':str(refresh.access_token)
        }