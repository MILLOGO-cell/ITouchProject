from rest_framework import serializers
from .models import Employe,Poste, FicheDePaie,EtatService
class PosteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poste
        exclude = ['owner',]

 
class EtatServiceSerializer(serializers.ModelSerializer):
     class Meta:
        model = EtatService
        exclude = ['owner']
        
 
class EmployeSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(
        max_length=None, allow_empty_file=False, allow_null=False, use_url=True, required=False)
    poste = serializers.PrimaryKeyRelatedField(
        queryset=Poste.objects.all(), write_only=True)
    poste_details = PosteSerializer(source='poste', read_only=True)
    statut = serializers.PrimaryKeyRelatedField(
        queryset=EtatService.objects.all(), write_only=True)
    statut_details = EtatServiceSerializer(source='statut', read_only=True)

    class Meta:
        model = Employe
        exclude = ['owner',]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')
        if request.method == 'GET':
            data['poste_details'] = PosteSerializer(instance.poste, context={'request': request}).data
            data['statut_details'] = EtatServiceSerializer(instance.statut, context={'request': request}).data
        return data
    
    def validate(self, data):
        owner = self.context['request'].user
        nom = data.get('nom')
        prenom = data.get('prenom')
        email = data.get('email')

        employe_instance = self.instance  # Récupérer l'instance de l'employé en cours de mise à jour
        if Employe.objects.filter(owner=owner, nom=nom, prenom=prenom).exclude(pk=employe_instance.pk).exists():
            raise serializers.ValidationError("Un employé avec le même nom et prénom existe déjà pour cet utilisateur.")

        if email and Employe.objects.filter(owner=owner, email=email).exclude(pk=employe_instance.pk).exists():
            raise serializers.ValidationError("Un employé avec le même email existe déjà pour cet utilisateur.")

        return data

    def create(self, validated_data):
        poste = validated_data.pop('poste', None)
        statut = validated_data.pop('statut', None)
        employe = Employe.objects.create(poste=poste, statut=statut, **validated_data)
        return employe



    
class FicheSerializer(serializers.ModelSerializer):
    class Meta:
        model = FicheDePaie
        exclude = ['owner']

