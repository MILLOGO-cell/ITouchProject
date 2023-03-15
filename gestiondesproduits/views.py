
from rest_framework import viewsets
from .serializers import ProduitSerializer, CategorieSerializer,SousCategorieSerializer,FabriquantSerializer,EmballageSerializer,TypeContenantSerializer
from .models import Produit, Categorie, SousCategorie,Fabriquant,Emballage,TypeContenant
from rest_framework import viewsets, permissions,parsers
from .permissions import IsOwner

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Produit.objects.all().order_by('nom')
    serializer_class = ProduitSerializer
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (parsers.FormParser, parsers.MultiPartParser,parsers.FileUploadParser)
    
    def perform_create(self,serializer):
        return serializer.save(owner=self.request.user)
    
class CategorieViewSet(viewsets.ModelViewSet):
    queryset = Categorie.objects.all().order_by('nom')
    serializer_class = CategorieSerializer 
    permission_classes = (permissions.IsAuthenticated,)
    
    def perform_create(self,serializer):
        return serializer.save(owner=self.request.user)
    
class SousCategorieViewSet(viewsets.ModelViewSet):
    queryset = SousCategorie.objects.all().order_by('nom')
    serializer_class = SousCategorieSerializer 
    permission_classes = (permissions.IsAuthenticated,)
    
    def perform_create(self,serializer):
        return serializer.save(owner=self.request.user)
    
class FabriquantViewSet(viewsets.ModelViewSet):
    queryset = Fabriquant.objects.all().order_by('nom')
    serializer_class = FabriquantSerializer 
    permission_classes = (permissions.IsAuthenticated,)
    
    def perform_create(self,serializer):
        return serializer.save(owner=self.request.user)
    
class EmballageViewSet(viewsets.ModelViewSet):
    queryset = Emballage.objects.all().order_by('nom')
    serializer_class = EmballageSerializer 
    permission_classes = (permissions.IsAuthenticated,)
    
    def perform_create(self,serializer):
        return serializer.save(owner=self.request.user)
    
class TypeContenantViewSet(viewsets.ModelViewSet):
    queryset = TypeContenant.objects.all().order_by('nom')
    serializer_class = TypeContenantSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def perform_create(self,serializer):
        return serializer.save(owner=self.request.user)