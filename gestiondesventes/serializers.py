from rest_framework import serializers
from .models import Vente, AvanceRetenu,Monnaie,Client,Credit,PerteMateriel,DepenseVente,ProduitVente,ProduitConsigne,ProduitAvoirPris,PerteVenteProduitContenant

class VenteSerializer(serializers.ModelSerializer):
    
     class Meta:
        model = Vente 
        fields = '__all__'
        
class AvanceRetenuSerializer(serializers.ModelSerializer):
    
     class Meta:
        model = AvanceRetenu 
        fields = '__all__'
        
class MonnaieSerializer(serializers.ModelSerializer):
    
     class Meta:
        model = Monnaie 
        fields = '__all__'

class ClientSerializer(serializers.ModelSerializer):
    
     class Meta:
        model = Client 
        fields = '__all__'
        
class CreditSerializer(serializers.ModelSerializer):
    
     class Meta:
        model = Credit 
        fields = '__all__'
        
class PerteMaterielSerializer(serializers.ModelSerializer):
    
     class Meta:
        model = PerteMateriel 
        fields = '__all__'
        
class DepenseVenteSerializer(serializers.ModelSerializer):
    
     class Meta:
        model = DepenseVente 
        fields = '__all__'

class ProduitVenteSerializer(serializers.ModelSerializer):
    
     class Meta:
        model = ProduitVente 
        fields = '__all__'

class ProduitConsigneSerializer(serializers.ModelSerializer):
    
     class Meta:
        model = ProduitConsigne 
        fields = '__all__'

class ProduitAvoirPrisSerializer(serializers.ModelSerializer):
    
     class Meta:
        model = ProduitAvoirPris 
        fields = '__all__'

class PerteVenteProduitContenantSerializer(serializers.ModelSerializer):
    
     class Meta:
        model = PerteVenteProduitContenant 
        fields = '__all__'