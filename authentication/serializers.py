from rest_framework import serializers
from .models import User
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from django.utils.encoding import smart_str,smart_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from django.db.models import Q
from rest_framework import status
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from gestiondesproduits.models import Pays
class UserSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField(
        max_length=None, allow_empty_file=False, allow_null=False, use_url=True, required=False)
    # selected_country = serializers.PrimaryKeyRelatedField(queryset=Pays.objects.all(), required=False)
    class Meta:
        model = User
        fields = ('email', 'username', 'photo','company', )
        extra_kwargs = {
            'photo': {'required': False},
            'company': {'required': False},
        }
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['old_password'] == attrs['new_password']:
            raise serializers.ValidationError("Le nouveau mot de passe doit être différent de l'ancien.")
        return attrs
class UserEditSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField(
        max_length=None, allow_empty_file=False, allow_null=False, use_url=True, required=False)
    selected_country = serializers.PrimaryKeyRelatedField(queryset=Pays.objects.all(), required=False)
    class Meta:
        model = User
        fields = ('id','username','email' ,'photo','company','selected_country')
        extra_kwargs = {
            'email': {'required': False},
            'username': {'required': False},
            'photo': {'required': False},
            'company': {'required': False},
            'selected_country': {'required': False},
        }
    def partial_update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.photo = validated_data.get('photo', instance.photo)
        instance.company = validated_data.get('company', instance.company)
        instance.selected_country = validated_data.get('selected_country', instance.selected_country)
        instance.save()
        return instance

 
class RegisterSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField( 
        max_length=None, allow_empty_file=False, allow_null=False, use_url=True, required=False)
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)
    
    confirm_password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)
    
    verification_code = serializers.CharField(max_length=6, required=False)

    extra_kwargs = {
            'photo': {'required': False},
        }
   
    def validate(self,attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')
        
        if not username.isalnum():
            raise serializers.ValidationError("Le nom d'utilisateur doit contenir des caractères alphanumériques")

        try:
            validate_email(email)
       
        except ValidationError:
            raise serializers.ValidationError("Adresse e-mail invalide")

        return attrs
    
    def validate_password(self,attrs):
        password= self.initial_data.get("password")
        confirm_password= self.initial_data.get("confirm_password")
        if not password or not confirm_password:
            raise serializers.ValidationError('Veuillez entrer votre mot de passe')
        if password != confirm_password:
            raise serializers.ValidationError('Les mots de passe ne correspondent pas!')
        return attrs

    class Meta:
        model=User 
        fields=['email','username','company','password','confirm_password','photo','verification_code']
        
        
    def create(self, validated_data):
        email = validated_data['email']
        username = validated_data['username']
        if User.objects.filter(Q(email=email) | Q(username=username)).exists():
            errors = {}
            if User.objects.filter(email=email).exists():
                errors['email'] = ['Un utilisateur avec cette adresse e-mail existe déjà.']
            if User.objects.filter(username=username).exists():
                errors['username'] = ['Un utilisateur avec ce nom d\'utilisateur existe déjà.']
            print(errors)
            raise serializers.ValidationError(errors, code=status.HTTP_409_CONFLICT)
        user = User.objects.create(
            username=username,
            email=email,
        )
        user.set_password(validated_data['password'])
        user.verification_code = get_random_string(length=6, allowed_chars='0123456789')
        user.save()

        return user

class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)
    verification_code = serializers.CharField(max_length=6, required=True)
    class Meta:
        model = User
        fields = ['token','verification_code']

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password =serializers.CharField(max_length=68, min_length=6,write_only=True)
    company =serializers.CharField(max_length=68, min_length=1,read_only=True)
    username = serializers.CharField(max_length=255, min_length=3,read_only=True)
    tokens =serializers.CharField(max_length=68, min_length=6,read_only=True)
    # selected_country = serializers.SerializerMethodField(source='get_selected_country')
    class Meta:
        model = User
        fields = ['email','password','username','company','tokens',  ]
    
    # def get_selected_country(self, user):
    #     selected_country = user.selected_country
    #     if selected_country:
    #         print("selected$*******",selected_country)
    #         return  selected_country
    #     return None
      
    def validate(self,attrs):
        email=attrs.get('email', '')
        password=attrs.get('password', '')
        user=auth.authenticate(email=email,password=password)
        
        if not user:
            raise AuthenticationFailed('Identifiants invalides, veuillez recommencer!',)
        if not user.is_active:
            raise AuthenticationFailed('Compte désactivé, veuillez activer votre compte!',)
        if not user.is_verified:
            raise AuthenticationFailed('Email non vérifiée',)
         
        return {
            'email':user.email,
            'username': user.username,
            'company': user.company,
            'tokens':user.tokens,
            # 'selected_country': self.get_selected_country(user) 
        }
        
    
class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email =serializers.EmailField(min_length=2)
    
    class Meta:
        field= ["email"]

class PasswordResetSerializer(serializers.Serializer):
   email = serializers.EmailField()
   code = serializers.IntegerField()
   password = serializers.CharField(min_length=8, write_only=True)

   def validate(self, data):
        email = data.get('email')
        code = data.get('code')
        password = data.get('password')
        if not User.objects.filter(email=email, reset_code=code).exists():
            raise serializers.ValidationError('Code de vérification invalide')
        return data

 
    