from rest_framework import serializers
from .models import Vente, AvanceRetenu,Monnaie,Client,Credit,PerteMateriel,DepenseVente,ProduitVente,ProduitConsigne,ProduitAvoirPris,PerteVenteProduitContenant
from rest_framework.exceptions import ValidationError
from gestiondesproduits.serializers import ProduitSerializer
from gestiondesproduits.models import Produit


class MonnaieSerializer(serializers.ModelSerializer):
    
     class Meta:
        model = Monnaie 
        exclude= ['owner'] 

class VenteSerializer(serializers.ModelSerializer):
    monnaie = MonnaieSerializer(required=False)

    class Meta:
        model = Vente 
        exclude = ['owner']  

    def create(self, validated_data):
        monnaie_data = validated_data.pop('monnaie', None)
        vente = Vente.objects.create(**validated_data)

        if monnaie_data:
            Monnaie.objects.create(vente=vente, **monnaie_data)

        return vente

    def update(self, instance, validated_data):
        monnaie_data = validated_data.pop('monnaie', None)

        # Update the vente instance
        instance = super().update(instance, validated_data)

        if monnaie_data:
            monnaie_serializer = MonnaieSerializer(instance.monnaie, data=monnaie_data)
            if monnaie_serializer.is_valid():
                monnaie = monnaie_serializer.save()
                instance.monnaie = monnaie
                instance.save()
            else:
                raise ValidationError(monnaie_serializer.errors)

        return instance
 
class AvanceRetenuSerializer(serializers.ModelSerializer):
    
     class Meta:
        model = AvanceRetenu 
        exclude= ['owner'] 
        


class ClientSerializer(serializers.ModelSerializer):
    
     class Meta:
        model = Client 
        exclude= ['owner'] 
        
class CreditSerializer(serializers.ModelSerializer):
    
     class Meta:
        model = Credit 
        exclude= ['owner'] 
        
class PerteMaterielSerializer(serializers.ModelSerializer):
    
     class Meta:
        model = PerteMateriel 
        exclude= ['owner'] 
        
class DepenseVenteSerializer(serializers.ModelSerializer):
    
     class Meta:
        model = DepenseVente 
        exclude= ['owner'] 

class ProduitVenteDetailsSerializer(serializers.ModelSerializer):
    produit_details = ProduitSerializer(source='produit', read_only=True)

    class Meta:
        model = ProduitVente
        exclude = ['owner']


class ProduitVenteSerializer(serializers.ModelSerializer):
    produit = serializers.PrimaryKeyRelatedField(
        queryset=Produit.objects.all(), write_only=True)

    class Meta:
        model = ProduitVente
        exclude = ['owner']

    def create(self, validated_data):
        produit = validated_data.pop('produit', None)
        produit_vente = ProduitVente.objects.create(produit=produit, **validated_data)
        return produit_vente

class ProduitConsigneSerializer(serializers.ModelSerializer):
    
     class Meta:
        model = ProduitConsigne 
        exclude= ['owner'] 

class ProduitAvoirPrisSerializer(serializers.ModelSerializer):
    
     class Meta:
        model = ProduitAvoirPris 
        exclude= ['owner'] 

class PerteVenteProduitContenantSerializer(serializers.ModelSerializer):
    
     class Meta:
        model = PerteVenteProduitContenant 
        exclude= ['owner'] 