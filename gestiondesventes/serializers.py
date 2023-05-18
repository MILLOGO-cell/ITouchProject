from rest_framework import serializers
from .models import Vente, AvanceRetenu,Monnaie,Client,Credit,PerteMateriel,DepenseVente,ProduitVente,ProduitConsigne,ProduitAvoirPris,PerteVenteProduitContenant

class MonnaieSerializer(serializers.ModelSerializer):
    
     class Meta:
        model = Monnaie 
        exclude= ['owner'] 

class VenteSerializer(serializers.ModelSerializer):
    monnaie = MonnaieSerializer(required=False)
    class Meta:
        model = Vente 
        exclude= ['owner']  

    def create(self, validated_data):
        monnaie_data = validated_data.pop('monnaie', None)
        vente = Vente.objects.create(**validated_data)

        if monnaie_data:
            Monnaie.objects.create(vente=vente, **monnaie_data)

        return vente
 
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

class ProduitVenteSerializer(serializers.ModelSerializer):
    
     class Meta:
        model = ProduitVente 
        exclude= ['owner'] 

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