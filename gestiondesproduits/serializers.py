from .models import Produit, Categorie, SousCategorie, Emballage, Fabriquant, TypeContenant,FournisseurProduit,CommandeProduit
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status

class CategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorie 
        exclude =['owner']
        
class SousCategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = SousCategorie 
        exclude =['owner']


class FabriquantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fabriquant 
        exclude =['owner']


class EmballageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emballage 
        exclude =['owner']


class TypeContenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeContenant 
        exclude =['owner']
                              
                
class ProduitSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(read_only=True)
    image = serializers.ImageField(
        max_length=None, allow_empty_file=False, allow_null=False, use_url=True, required=False)
    categorie = serializers.PrimaryKeyRelatedField(queryset=Categorie.objects.all())
    type_contenant = serializers.PrimaryKeyRelatedField(queryset=TypeContenant.objects.all())

    class Meta:
        model = Produit
        # exclude = ['owner']
        exclude =['owner']



    
class FournisseurProduitSerializer(serializers.ModelSerializer):
    class Meta:
        model = FournisseurProduit 
        exclude =['owner']

class CommandeProduitIdsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommandeProduit
        exclude = ['owner']    

    def create(self, validated_data):
        commande = CommandeProduit.objects.create(**validated_data)
        return commande
    
    
class CommandeProduitDetailsSerializer(serializers.ModelSerializer):
    fournisseur = FournisseurProduitSerializer()
    produit = ProduitSerializer()

    class Meta:
        model = CommandeProduit
        exclude = ['owner']