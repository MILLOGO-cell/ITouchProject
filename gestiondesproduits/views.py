
from rest_framework import viewsets,status
from .serializers import ProduitSerializer, ProduitRetrieveSerializer,CategorieSerializer,SousCategorieCreateSerializer,SousCategorieRetrieveSerializer,FabriquantSerializer,EmballageCreateSerializer,PaysSerializer,EmballageRetrieveSerializer,TypeContenantCreateSerializer,TypeContenantRetrieveSerializer,CommandeProduitDetailsSerializer,CommandeProduitIdsSerializer,FournisseurProduitSerializer,UniteVolumeSerializer
from .models import Produit, Categorie, SousCategorie,Fabriquant,Emballage,TypeContenant,FournisseurProduit,CommandeProduit,UniteVolume,Pays
from rest_framework import viewsets, permissions,parsers
from .permissions import IsOwner
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from .models import SousCategorie
from django.core.exceptions import ValidationError
from django.db.models import Q
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Produit.objects.all().order_by('nom')
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.FileUploadParser)
    pagination_class = None
    serializer_classes = {
        'create': ProduitSerializer,
        'update': ProduitSerializer,
        'partial_update': ProduitSerializer,
        'retrieve': ProduitRetrieveSerializer,
        'list': ProduitRetrieveSerializer,
    }
    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, ProduitRetrieveSerializer)

    def perform_create(self, serializer):
        commun = self.request.data.get('commun', False)
        if not commun:
            # serializer.save(owner=self.request.user)
            serializer.save( )
        else:
            serializer.save()

    def get_queryset(self):
        queryset_user = Produit.objects.filter(owner=self.request.user)  # Récupérer les produits de l'utilisateur
        pays_id = self.request.GET.get('pays_id', None)  # Récupérer l'ID du pays choisi par l'utilisateur depuis les paramètres de la requête
        if pays_id:
            pays = Pays.objects.get(id=pays_id)
            queryset_common = Produit.objects.filter(Q(pays=pays) | (Q(pays__isnull=True) & Q(owner__isnull=True)))  # Récupérer les produits communs par pays
        else:
            queryset_common = Produit.objects.filter(owner__isnull=True)  # Récupérer tous les produits communs (sans pays spécifié)

        queryset = queryset_user.union(queryset_common)  # Combiner les deux ensembles de requêtes
        return queryset
    
class CategorieViewSet(viewsets.ModelViewSet):
    queryset = Categorie.objects.all().order_by('nom')
    serializer_class = CategorieSerializer 
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = None
    
    def perform_create(self,serializer):
        return serializer.save(owner=self.request.user)
    
    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)
    
class UniteVolumeViewSet(viewsets.ModelViewSet):
    queryset = UniteVolume.objects.all().order_by('valeur')
    serializer_class = UniteVolumeSerializer 
    permission_classes = (permissions.AllowAny,)
    pagination_class = None
    
    def perform_create(self,serializer):
        return serializer.save(owner=self.request.user)
    
    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    # def get_queryset(self):
    #     user = self.request.user
    #     return UniteVolume.objects.filter(Q(owner=user) | Q(owner=None)).order_by('valeur')

class SousCategorieViewSet(viewsets.ModelViewSet):
    queryset = SousCategorie.objects.all().order_by('nom')
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = None
    serializer_classes = {
        'create': SousCategorieCreateSerializer,
        'update': SousCategorieCreateSerializer,
        'partial_update': SousCategorieCreateSerializer,
        'retrieve': SousCategorieRetrieveSerializer,
        'list': SousCategorieRetrieveSerializer,
    }
    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, SousCategorieRetrieveSerializer)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

class FabriquantViewSet(viewsets.ModelViewSet):
    queryset = Fabriquant.objects.all().order_by('nom')
    serializer_class = FabriquantSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = None

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)
    
class EmballageViewSet(viewsets.ModelViewSet):
    queryset = Emballage.objects.all().order_by('nom')
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = None
    serializer_classes = {
        'create': EmballageCreateSerializer,
        'update': EmballageCreateSerializer,
        'partial_update': EmballageCreateSerializer,
        'retrieve': EmballageRetrieveSerializer,
        'list': EmballageRetrieveSerializer,
    }
    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, EmballageRetrieveSerializer)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

class TypeContenantViewSet(viewsets.ModelViewSet):
    queryset = TypeContenant.objects.all().order_by('nom')
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = None
    
    serializer_classes = {
        'create': TypeContenantCreateSerializer,
        'update': TypeContenantCreateSerializer,
        'partial_update': TypeContenantCreateSerializer,
        'retrieve': TypeContenantRetrieveSerializer,
        'list': TypeContenantRetrieveSerializer,
    }
    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, TypeContenantRetrieveSerializer)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)
    
class FournisseurProduitViewSet(viewsets.ModelViewSet):
    queryset = FournisseurProduit.objects.all().order_by('enseigne')
    serializer_class = FournisseurProduitSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None

    def perform_create(self,serializer):
        return serializer.save(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)
         
class CommandeProduitViewSet(viewsets.ModelViewSet):
    queryset = CommandeProduit.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None

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


class PaysViewset(viewsets.ModelViewSet):
    queryset = Pays.objects.all()
    # permission_classes = [permissions.IsAuthenticated]
    pagination_class = None
    serializer_class = PaysSerializer
    
     