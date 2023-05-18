from rest_framework import serializers
from .models import Materiel, CommandeMateriel, Fournisseur
from django.shortcuts import get_object_or_404

class FournisseurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fournisseur
        exclude = ['owner']

class MaterielSerializer(serializers.ModelSerializer):
    class Meta:
        model = Materiel
        exclude = ['owner']

        
class CommandeMaterielIdsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommandeMateriel
        exclude = ['owner']
        

    def create(self, validated_data):
        commande = CommandeMateriel.objects.create(**validated_data)
        return commande
    
class CommandeMaterielDetailsSerializer(serializers.ModelSerializer):
    fournisseur = FournisseurSerializer()
    materiel = MaterielSerializer()

    class Meta:
        model = CommandeMateriel
        # fields = ['id', 'fournisseur', 'materiel', 'quantite', 'num_bordereaux', 'nom_livreur', 'prenom_livreur', 'montant_facture', 'montant_reel_facture', 'date_creation']
        exclude = ['owner']
        
