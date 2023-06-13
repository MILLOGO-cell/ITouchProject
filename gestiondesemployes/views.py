from django.shortcuts import render
from .models import Employe, Poste,FicheDePaie
from .serializers import EmployeSerializer, PosteSerializer, FicheSerializer
from rest_framework import viewsets, permissions, parsers,generics
from .permissions import IsOwner
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
import logging
from rest_framework import filters
User = get_user_model()

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_image_url(request, id):
    my_object = get_object_or_404(User, id=id)
    image_url = settings.MEDIA_URL + str(my_object.photo)
    return JsonResponse({'image_url': image_url})

class PosteViewset(viewsets.ModelViewSet):
    queryset = Poste.objects.all().order_by('intitule')
    serializer_class = PosteSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = None  
    
    def perform_create(self,serializer):
        return serializer.save(owner=self.request.user)
    
    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

logger = logging.getLogger(__name__)
class EmployeViewset(viewsets.ModelViewSet):
    queryset = Employe.objects.all().order_by('nom')
    serializer_class = EmployeSerializer 
    pagination_class = None  
    parser_classes = (parsers.FormParser, parsers.MultiPartParser,parsers.FileUploadParser)
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = [filters.SearchFilter]
    search_fields = ['statut']
    
    def perform_create(self,serializer):
        return serializer.save(owner=self.request.user)
    
    def perform_update(self, serializer):
        poste_intitule = serializer.validated_data.get('poste_intitule')
        if poste_intitule:
            poste = Poste.objects.get(intitule=poste_intitule)
            serializer.validated_data['poste'] = poste
        serializer.save()
        
    def get_queryset(self):
        logger.info("Filtering employe queryset by owner: %s", self.request.user)
        return self.queryset.filter(owner=self.request.user)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"poste_queryset": Poste.objects.all()})
        return context

    def get_schema(self, request, *args, **kwargs):
        # specify the queryset parameter for the PosteSerializer
        PosteSerializer.Meta.model = Poste.objects.all()
        return super().get_schema(request, *args, **kwargs)
    
class FicheView(viewsets.ModelViewSet):
    queryset = FicheDePaie.objects.all().order_by('date_fin')
    serializer_class = FicheSerializer
    pagination_class = None
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self,serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)
     
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"fiche_queryset": self.get_queryset()})
        return context

    def get_schema(self, request, *args, **kwargs):
        FicheSerializer.Meta.model = FicheDePaie.objects.all()
        return super().get_schema(request, *args, **kwargs)
    