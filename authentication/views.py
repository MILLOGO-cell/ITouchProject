
from django.contrib.auth import get_user_model
from rest_framework import generics, status, views, permissions
from .serializers import RegisterSerializer,LoginSerializer,EmailVerificationSerializer,ResetPasswordEmailRequestSerializer,PasswordResetSerializer,UserSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .renderers import UserRenderer
from django.utils.encoding import smart_str,smart_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import Util
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, permissions,parsers
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.conf import settings
import random
from django.utils import timezone

User = get_user_model()


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_image_url(request, id):
    my_object = get_object_or_404(User, id=id)
    image_url = settings.MEDIA_URL + str(my_object.photo)
    return JsonResponse({'image_url': image_url})

class RegisterView(generics.GenericAPIView):
    
    serializer_class = RegisterSerializer
    renderer_classes =(UserRenderer,)
    parser_classes = (parsers.FormParser, parsers.MultiPartParser,parsers.FileUploadParser)
    
    def post(self, request):
        user = request.data 
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])
        
        # Generer un code de vérification à 6 chiffres
        verification_code = random.randint(100000, 999999)
        
        # Enregistrer le code de vérification dans le modèle utilisateur
        user.verification_code = verification_code
        user.save()
        
        # Envoyer l'email de vérification
        email_body = 'Bonjour ' + user.username + ', utilise ce code pour activer votre compte : ' + str(verification_code)
        data = {'email_body': email_body, 'to_email': user.email, 'email_subject': "Vérification d'email"}
        Util.send_email(data)
        
        return Response(user_data, status=status.HTTP_201_CREATED)


class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer
   
    def get(self, request):
        code = request.GET.get('verification_code')
        if not code:
            return Response({'error':'Code de vérification non communiqué'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(verification_code=code)
        except User.DoesNotExist:
            return Response({'error':"Le code de vérification n'a pas été trouvé"}, status=status.HTTP_400_BAD_REQUEST)

        if user.is_verified:
            return Response({'error':'Email déjà vérifié'}, status=status.HTTP_400_BAD_REQUEST)

        # Verifier si le code de verification a expiré(10 minutes)
        time_elapsed = timezone.now() - user.created_at
        if time_elapsed.total_seconds() > 600:
            return Response({'error':'Le code de vérification a expiré'}, status=status.HTTP_400_BAD_REQUEST)

        # Marquer l'utilisateur comme vérifié
        user.is_verified = True
        user.save()
        # Vérifier si l'utilisateur a été vérifié, sinon le supprimer
        if not user.is_verified:
            user.delete()
            return Response({'error': 'L\'utilisateur a été supprimé car le code de vérification a expiré.'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'email':'Activé avec succès'}, status=status.HTTP_200_OK)
  
class LogiAPIView(generics.GenericAPIView):
    serializer_class=LoginSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        return Response(serializer.data,status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_info(request):
    user = request.user
    data = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'photo': user.photo.url if user.photo else None,
    }
    return Response(data, status=status.HTTP_200_OK)   

class UserEditView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (parsers.FormParser, parsers.MultiPartParser,parsers.FileUploadParser)

    def get_object(self):
        return self.request.user

class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class= ResetPasswordEmailRequestSerializer   
    
    def post(self,request):
        serializer = self.serializer_class(data=request.data)        
        email = request.data['email']
        
        if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
                # Generer un code de vérification à 6 chiffres
                code = random.randint(100000, 999999)
                user.reset_code = code
                user.save()
                email_body = f'Bonjour,\n utilise le code {code} pour vérifier votre adresse e-mail et réinitialiser votre mot de passe.'
                data = {'email_body': email_body, 'to_email': user.email, 'email_subject': 'Vérification d\'adresse e-mail'}
                Util.send_email(data)

        return Response({'success': 'Nous vous avons envoyé un e-mail avec un code de vérification'}, status=status.HTTP_200_OK)
    
class PasswordResetView(views.APIView):
        
    serializer_class = PasswordResetSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            code = serializer.validated_data['code']
            password = serializer.validated_data['password']
            try:
                user = User.objects.get(email=email, reset_code=code)
                user.set_password(password)
                user.reset_code = None
                user.save()
                email_body = f'Bonjour,\n votre mot de passe a été réinitailiser avec succès.'
                data = {'email_body': email_body, 'to_email': user.email, 'email_subject': 'Réinitialisation de mot de passe'}
                Util.send_email(data)
                return Response({'success': 'Votre mot de passe a été réinitialisé avec succès'}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({'error': 'Code de vérification invalide'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)