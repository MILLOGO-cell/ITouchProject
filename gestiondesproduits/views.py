
from rest_framework import viewsets
from .serializers import ProduitSerializer, CategorieSerializer,SousCategorieSerializer,FabriquantSerializer,EmballageSerializer,TypeContenantSerializer,CommandeProduitDetailsSerializer,CommandeProduitIdsSerializer,FournisseurProduitSerializer
from .models import Produit, Categorie, SousCategorie,Fabriquant,Emballage,TypeContenant,FournisseurProduit,CommandeProduit
from rest_framework import viewsets, permissions,parsers
from .permissions import IsOwner
from rest_framework.pagination import PageNumberPagination


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Produit.objects.all().order_by('nom')
    serializer_class = ProduitSerializer
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (parsers.FormParser, parsers.MultiPartParser,parsers.FileUploadParser)
    pagination_class = PageNumberPagination
    
    def perform_create(self,serializer):
        return serializer.save(owner=self.request.user)
    
class CategorieViewSet(viewsets.ModelViewSet):
    queryset = Categorie.objects.all().order_by('nom')
    serializer_class = CategorieSerializer 
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = PageNumberPagination
    
    def perform_create(self,serializer):
        return serializer.save(owner=self.request.user)
    
class SousCategorieViewSet(viewsets.ModelViewSet):
    queryset = SousCategorie.objects.all().order_by('nom')
    serializer_class = SousCategorieSerializer 
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = PageNumberPagination
    
    def perform_create(self,serializer):
        return serializer.save(owner=self.request.user)
    
class FabriquantViewSet(viewsets.ModelViewSet):
    queryset = Fabriquant.objects.all().order_by('nom')
    serializer_class = FabriquantSerializer 
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = PageNumberPagination
    
    def perform_create(self,serializer):
        return serializer.save(owner=self.request.user)
    
class EmballageViewSet(viewsets.ModelViewSet):
    queryset = Emballage.objects.all().order_by('nom')
    serializer_class = EmballageSerializer 
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = PageNumberPagination
    
    def perform_create(self,serializer):
        return serializer.save(owner=self.request.user)
    
class TypeContenantViewSet(viewsets.ModelViewSet):
    queryset = TypeContenant.objects.all().order_by('nom')
    serializer_class = TypeContenantSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = PageNumberPagination
    
    def perform_create(self,serializer):
        return serializer.save(owner=self.request.user)
    
class FournisseurProduitViewSet(viewsets.ModelViewSet):
    queryset = FournisseurProduit.objects.all().order_by('enseigne')
    serializer_class = FournisseurProduitSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PageNumberPagination

    def perform_create(self,serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)
     

    
class CommandeProduitViewSet(viewsets.ModelViewSet):
    queryset = CommandeProduit.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PageNumberPagination

    def perform_create(self,serializer):
        serializer.save(owner=self.request.user)
        
        # Mettre à jour le stock de matériel
        commande = serializer.instance
        produit = commande.produit
        
        # Calculer le nouveau stock
        nouveau_stock = int(produit.stock_courant) + commande.quantite
        
        # Mettre à jour le stock de matériel
        produit.stock_courant = str(nouveau_stock)
        produit.save()

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update' or self.action == 'partial_update':
            return CommandeProduitIdsSerializer
        return CommandeProduitDetailsSerializer

 