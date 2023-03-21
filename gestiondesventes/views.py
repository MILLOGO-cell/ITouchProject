from rest_framework import viewsets
from .serializers import VenteSerializer, AvanceRetenuSerializer,MonnaieSerializer,ClientSerializer,CreditSerializer,PerteMaterielSerializer, DepenseVenteSerializer,ProduitVenteSerializer,ProduitConsigneSerializer,ProduitAvoirPrisSerializer,PerteVenteProduitContenantSerializer
from .models import Vente, AvanceRetenu,Monnaie,Client,Credit,PerteMateriel,DepenseVente,ProduitVente,ProduitConsigne,ProduitAvoirPris,PerteVenteProduitContenant
from rest_framework import viewsets, permissions
from .permissions import IsOwner

class VenteViewSet(viewsets.ModelViewSet):
    queryset = Vente.objects.all()
    serializer_class = VenteSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def perform_create(self,serializer):
        return serializer.save(owner=self.request.user)
    
class AvanceRetenuViewSet(viewsets.ModelViewSet):
    queryset = AvanceRetenu.objects.all()
    serializer_class = AvanceRetenuSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self,serializer):
        return serializer.save(owner=self.request.user)

class MonnaieViewSet(viewsets.ModelViewSet):
    queryset = Monnaie.objects.all()
    serializer_class = MonnaieSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self,serializer):
        return serializer.save(owner=self.request.user)

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self,serializer):
        return serializer.save(owner=self.request.user)
    
class CreditViewSet(viewsets.ModelViewSet):
    queryset = Credit.objects.all()
    serializer_class = CreditSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self,serializer):
        return serializer.save(owner=self.request.user)

class PerteMaterielViewSet(viewsets.ModelViewSet):
    queryset = PerteMateriel.objects.all()
    serializer_class = PerteMaterielSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self,serializer):
        return serializer.save(owner=self.request.user)
class DepenseVenteViewSet(viewsets.ModelViewSet):
    queryset = DepenseVente.objects.all()
    serializer_class = DepenseVenteSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self,serializer):
        return serializer.save(owner=self.request.user)
    
class ProduitVenteViewSet(viewsets.ModelViewSet):
    queryset = ProduitVente.objects.all()
    serializer_class = ProduitVenteSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self,serializer):
        return serializer.save(owner=self.request.user)
    
class ProduitConsigneViewSet(viewsets.ModelViewSet):
    queryset = ProduitConsigne.objects.all()
    serializer_class = ProduitConsigneSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self,serializer):
        return serializer.save(owner=self.request.user)
    
class ProduitAvoirPrisViewSet(viewsets.ModelViewSet):
    queryset = ProduitAvoirPris.objects.all()
    serializer_class = ProduitAvoirPrisSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self,serializer):
        return serializer.save(owner=self.request.user)
    
class PerteVenteProduitContenantViewSet(viewsets.ModelViewSet):
    queryset = PerteVenteProduitContenant.objects.all()
    serializer_class = PerteVenteProduitContenantSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self,serializer):
        return serializer.save(owner=self.request.user)