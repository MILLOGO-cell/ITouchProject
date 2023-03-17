from rest_framework import serializers
from .models import User
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from django.utils.encoding import smart_str,smart_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)
    
    confirm_password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)
    
   
    def validate(self,attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')
        if not username.isalnum():
            raise serializers.ValidationError("Le nom d'utilisateur doit contenir des caractères alphanumeriques")
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
        fields=['email','username','password','confirm_password',]
        
        
    def create(self, validated_data):
        # return User.objects.create_user(**validated_data)
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        # user.set_password(validated_data['confirm_password'])
        user.save()

        return user
class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)
    
    class Meta:
        model = User
        fields = ['token']

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password =serializers.CharField(max_length=68, min_length=6,write_only=True)
    username = serializers.CharField(max_length=255, min_length=3,read_only=True)
    tokens =serializers.CharField(max_length=68, min_length=6,read_only=True)
    
    class Meta:
        model = User
        fields = ['email','password','username','tokens']
        
    def validate(self,attrs):
        email=attrs.get('email', '')
        password=attrs.get('password', '')
        
        user=auth.authenticate(email=email,password=password)
        
        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Accont disabled, contact admin')
        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified')
        
        return {
            'email':user.email,
            'username': user.username,
            'tokens':user.tokens
        }
        
        return super().validate(attrs)
    
class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email =serializers.EmailField(min_length=2)
    
    class Meta:
        field= ["email"]

class PasswordTokenCheckApiSerializer(serializers.Serializer):
    
    class Meta:
        fields=[]
class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=6, max_length=68,write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)
    uidb64 = serializers.CharField(min_length=1,write_only=True)
    
    class Meta:
        fields=['password', 'token', 'uidb64']
        
    def validate(self, attrs):
        try:
            password= attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')
            
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)  
            
            user.set_password(password)
            user.save()
            return (user) 
        except Exception as e:
                raise AuthenticationFailed('The reset link is invalid', 401)   
        return super().validate(attrs)