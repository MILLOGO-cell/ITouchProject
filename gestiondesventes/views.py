from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from .serializers import VenteSerializer, AvanceRetenuSerializer,MonnaieSerializer,ClientSerializer,CreditSerializer,PerteMaterielSerializer, DepenseVenteSerializer,StatistiquesSerializer,ProduitVenteSerializer,ProduitConsigneSerializer,ProduitAvoirPrisSerializer,PerteVenteProduitContenantSerializer,ProduitVenteDetailsSerializer
from .models import Vente, AvanceRetenu,Monnaie,Client,Credit,PerteMateriel,DepenseVente,ProduitVente,ProduitConsigne,ProduitAvoirPris,PerteVenteProduitContenant
from rest_framework import viewsets, permissions
from .permissions import IsOwner
from rest_framework.exceptions import ValidationError
from django.db.models.signals import pre_save
from django.dispatch import receiver
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ProduitVente
from django.db.models import Sum
from django.db.models.functions import Coalesce
from datetime import datetime, timedelta
from gestiondesproduits.models import Produit
from gestiondesproduits.serializers import ProduitSerializer
from django.db.models import F, Value
import pytz
from django.utils import timezone
class VenteViewSet(viewsets.ModelViewSet):
    queryset = Vente.objects.all()
    serializer_class = VenteSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = None

    def perform_create(self, serializer):
        monnaie_data = self.request.data.get('monnaie')
        vente = serializer.save(owner=self.request.user)

        if monnaie_data:
            monnaie_serializer = MonnaieSerializer(data=monnaie_data)
            if monnaie_serializer.is_valid():
                monnaie = monnaie_serializer.save(owner=self.request.user)
                vente.monnaie = monnaie
                vente.save()
            else:
                raise ValidationError(monnaie_serializer.errors)

        return vente
    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user).order_by('-date_creation')

    @action(detail=False, methods=['GET'])
    def vente_precedente(self, request):
        # Récupérer la vente précédente pour l'utilisateur actuel
        vente_precedente = Vente.objects.filter(owner=self.request.user).order_by('-date_creation').first()

        if vente_precedente:
            serializer = self.get_serializer(vente_precedente)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

class MonnaieViewSet(viewsets.ModelViewSet):
    queryset = Monnaie.objects.all()
    serializer_class = MonnaieSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = None
    
    def perform_create(self,serializer):
        return serializer.save(owner=self.request.user)
    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)
    
class AvanceRetenuViewSet(viewsets.ModelViewSet):
    queryset = AvanceRetenu.objects.all()
    serializer_class = AvanceRetenuSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = None
    def perform_create(self,serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)
class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = None
    def perform_create(self,serializer):
        return serializer.save(owner=self.request.user)
    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)
class CreditViewSet(viewsets.ModelViewSet):
    queryset = Credit.objects.all()
    serializer_class = CreditSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = None
    def perform_create(self,serializer):
        return serializer.save(owner=self.request.user)
    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)
class PerteMaterielViewSet(viewsets.ModelViewSet):
    queryset = PerteMateriel.objects.all()
    serializer_class = PerteMaterielSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = None
    def perform_create(self,serializer):
        return serializer.save(owner=self.request.user)
    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)
class DepenseVenteViewSet(viewsets.ModelViewSet):
    queryset = DepenseVente.objects.all()
    serializer_class = DepenseVenteSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = None
    def perform_create(self,serializer):
        return serializer.save(owner=self.request.user)
    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)
    

class ProduitVenteViewSet(viewsets.ModelViewSet):
    queryset = ProduitVente.objects.all()
    serializer_class = ProduitVenteSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = None

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProduitVenteDetailsSerializer
        return ProduitVenteSerializer

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        vente_id = request.data.get('vente')
        vente = get_object_or_404(Vente, id=vente_id)

        produit_vente_data = request.data.copy()
        produit_vente_data['owner'] = request.user.id

        produit_vente_serializer = self.get_serializer(data=produit_vente_data)
        produit_vente_serializer.is_valid(raise_exception=True)
        produit_vente = produit_vente_serializer.save(vente=vente, owner=request.user)

        headers = self.get_success_headers(produit_vente_serializer.data)
        return Response(produit_vente_serializer.data, status=status.HTTP_201_CREATED, headers=headers)
       
    @action(detail=False, methods=['GET'])
    def latest_produitvente_for_product(self, request, produit_id=None):
        latest_produitvente = ProduitVente.objects.filter(produit_id=produit_id).order_by('-date_creation').first()

        if latest_produitvente:
            serializer = self.get_serializer(latest_produitvente)
            return Response(serializer.data)
        else:
            return Response({'message': 'Aucun enregistrement de ProduitVente pour le produit donné.'})
    @action(detail=False, methods=['GET'])
    def list_produits_vente_by_vente(self, request, vente_id=None):
        produits_vente = ProduitVente.objects.filter(vente_id=vente_id)
        serializer = self.get_serializer(produits_vente, many=True)
        return Response(serializer.data)

class ProduitConsigneViewSet(viewsets.ModelViewSet):
    queryset = ProduitConsigne.objects.all()
    serializer_class = ProduitConsigneSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = None
    def perform_create(self,serializer):
        return serializer.save(owner=self.request.user)
    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)
class ProduitAvoirPrisViewSet(viewsets.ModelViewSet):
    queryset = ProduitAvoirPris.objects.all()
    serializer_class = ProduitAvoirPrisSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = None
    def perform_create(self,serializer):
        return serializer.save(owner=self.request.user)
    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)
class PerteVenteProduitContenantViewSet(viewsets.ModelViewSet):
    queryset = PerteVenteProduitContenant.objects.all()
    serializer_class = PerteVenteProduitContenantSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = None
    def perform_create(self,serializer):
        return serializer.save(owner=self.request.user)
    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)
    


class StatistiquesView(APIView):
    def get(self, request, format=None):
        # Calculer les trois produits les plus vendus
        top_produits = ProduitVente.objects.values('produit').annotate(
            quantite_vendue=Coalesce(Sum('quantite'), 0)
        ).order_by('-quantite_vendue')[:3]

        top_produits_ids = [item['produit'] for item in top_produits]

        produits = Produit.objects.filter(id__in=top_produits_ids)
        top_produits_serialized = ProduitSerializer(produits, many=True).data

          # Calculer la recette mensuelle
        current_date = timezone.now()
        first_day_of_month = current_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0, tzinfo=pytz.UTC)
        recette_mensuelle = Vente.objects.filter(date_creation__gte=first_day_of_month).aggregate(recette_mensuelle=Sum(Coalesce('recette', Value(0))))['recette_mensuelle']

        # Calculer le total des pertes mensuelles
        total_pertes = Vente.objects.filter(date_creation__gte=first_day_of_month).aggregate(total_pertes=Sum(Coalesce('manquant', Value(0))))['total_pertes']

        statistiques_data = {
            'top_produits': top_produits_serialized,
            'recette_mensuelle': recette_mensuelle,
            'total_pertes': total_pertes,
        }


        serializer = StatistiquesSerializer(statistiques_data)
        return Response(serializer.data)
