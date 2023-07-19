from .models import Produit, Categorie, SousCategorie, Emballage, Fabriquant, TypeContenant,FournisseurProduit,CommandeProduit,UniteVolume
from rest_framework import serializers

class CategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorie 
        exclude =['owner']

class SousCategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = SousCategorie 
        exclude =['owner']     

class SousCategorieCreateSerializer(serializers.ModelSerializer):
    categorie = serializers.PrimaryKeyRelatedField(queryset=Categorie.objects.all(), write_only=True)
    class Meta:
        model = SousCategorie
        exclude = ['owner']

    def create(self, validated_data):
        categorie = validated_data.pop('categorie', None)
        sous_categorie = SousCategorie.objects.create(categorie=categorie, **validated_data)
        return sous_categorie


class SousCategorieRetrieveSerializer(serializers.ModelSerializer):
    categorie_details = CategorieSerializer(source='categorie', read_only=True)

    class Meta:
        model = SousCategorie
        fields = ['id', 'nom', 'categorie_details']
    
class FabriquantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fabriquant 
        exclude =['owner']


class EmballageCreateSerializer(serializers.ModelSerializer):
    fabriquant = serializers.PrimaryKeyRelatedField(queryset=Fabriquant.objects.all(), write_only=True)
    class Meta:
        model = Emballage 
        exclude =['owner']
    
    def create(self, validated_data):
        fabriquant = validated_data.pop('fabriquant', None)
        emballage = Emballage.objects.create(fabriquant=fabriquant, **validated_data)
        return emballage
class EmballageRetrieveSerializer(serializers.ModelSerializer):
    fabriquant_details = FabriquantSerializer(source='fabriquant', read_only=True)
    class Meta:
        model = Emballage 
        fields = ['id', 'nom', 'fabriquant_details']


class TypeContenantCreateSerializer(serializers.ModelSerializer):
    fabriquant = serializers.PrimaryKeyRelatedField(queryset=Fabriquant.objects.all(), write_only=True)
    class Meta:
        model = TypeContenant 
        exclude =['owner']
    def create(self, validated_data):
        fabriquant = validated_data.pop('fabriquant', None)
        type_contenant = TypeContenant.objects.create(fabriquant=fabriquant, **validated_data)
        return type_contenant
class TypeContenantRetrieveSerializer(serializers.ModelSerializer):

    fabriquant_details = FabriquantSerializer(source='fabriquant', read_only=True)
    class Meta:
        model = TypeContenant 
        fields = ['id', 'nom', 'fabriquant_details']
class UniteVolumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UniteVolume 
        exclude =['owner']                             
                
class ProduitSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(
        max_length=None, allow_empty_file=False, allow_null=False, use_url=True, required=False)
    sous_categorie = serializers.PrimaryKeyRelatedField(queryset=SousCategorie.objects.all())
    type_contenant = serializers.PrimaryKeyRelatedField(queryset=TypeContenant.objects.all())
    volume = serializers.PrimaryKeyRelatedField(queryset=UniteVolume.objects.all())

    class Meta:
        model = Produit
        exclude = ['owner',]

    def validate(self, data):
        owner = self.context['request'].user
        nom = data.get('nom')
        produit_instance = self.instance   
        
        if Produit.objects.filter(owner=owner, nom=nom).exclude(pk=produit_instance.pk).exists():
            raise serializers.ValidationError("Un produit avec le même intitulé existe déjà pour cet utilisateur.")
        return data 
    
    def create(self, validated_data):
        sous_categorie = validated_data.pop('sous_categorie', None)
        type_contenant = validated_data.pop('type_contenant', None)
        volume = validated_data.pop('volume', None)
        produit = Produit.objects.create(sous_categorie=sous_categorie, type_contenant=type_contenant, volume=volume, **validated_data)
        return produit    
               
class ProduitRetrieveSerializer(serializers.ModelSerializer):
    sous_categorie_details = SousCategorieSerializer(source='sous_categorie', read_only=True)
    type_contenant_details = TypeContenantRetrieveSerializer(source='type_contenant', read_only=True)
    volume_details = UniteVolumeSerializer(source='volume', read_only=True)
    class Meta:
        model = Produit
        fields = ['id',  'sous_categorie_details','type_contenant_details','volume_details','nom','stock_courant','image','prix','seuil_min','description','brouillon','en_vente','created_at','updated_at']

    
    
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