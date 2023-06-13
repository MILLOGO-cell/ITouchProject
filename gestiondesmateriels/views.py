from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Materiel, CommandeMateriel, Fournisseur
from rest_framework.pagination import PageNumberPagination
from .serializers import MaterielSerializer,FournisseurSerializer,CommandeMaterielDetailsSerializer,CommandeMaterielIdsSerializer

class MaterielViewSet(viewsets.ModelViewSet):
    queryset = Materiel.objects.all().order_by('nom')
    serializer_class = MaterielSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None

    def perform_create(self,serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

 
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class FournisseurViewSet(viewsets.ModelViewSet):
    queryset = Fournisseur.objects.all().order_by('enseigne')
    serializer_class = FournisseurSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None

    def perform_create(self,serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)
     

    
class CommandeMaterielViewSet(viewsets.ModelViewSet):
    queryset = CommandeMateriel.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None

    def perform_create(self,serializer):
        serializer.save(owner=self.request.user)
        
        # Mettre à jour le stock de matériel
        commande = serializer.instance
        materiel = commande.materiel
        
        # Calculer le nouveau stock
        nouveau_stock = int(materiel.stock_courant) + commande.quantite
        
        # Mettre à jour le stock de matériel
        materiel.stock_courant = str(nouveau_stock)
        materiel.save()

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update' or self.action == 'partial_update':
            return CommandeMaterielIdsSerializer
        return CommandeMaterielDetailsSerializer

     
 
    