from .models import Produit, Categorie, SousCategorie, Emballage, Fabriquant, TypeContenant
from rest_framework import serializers

class CategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorie 
        fields = '__all__'

class SousCategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = SousCategorie 
        fields = '__all__'

class FabriquantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fabriquant 
        fields = '__all__'

class EmballageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emballage 
        fields = '__all__'

class TypeContenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeContenant 
        fields = '__all__'                              
                
class ProduitSerializer(serializers.HyperlinkedModelSerializer):
    image = serializers.ImageField(
        max_length=None, allow_empty_file=False, allow_null=False, use_url=True, required=False)

    class Meta:
        model = Produit
        fields = ('id', "nom", "description", "prix",
                  "seuil_min", 'image', 'categorie')
