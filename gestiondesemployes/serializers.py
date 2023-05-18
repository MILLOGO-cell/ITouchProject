from rest_framework import serializers
from .models import Employe,Poste, FicheDePaie

class PosteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poste
        exclude = ['owner',]

class EmployeSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(
        max_length=None, allow_empty_file=False, allow_null=False, use_url=True, required=False)
    poste_intitule = serializers.SerializerMethodField()

    class Meta:
        model = Employe
        exclude = ['owner',] 

    def get_poste_intitule(self, obj):
        if obj.poste:
            return obj.poste.intitule
        else:
            return ""
        
class FicheSerializer(serializers.ModelSerializer):
    class Meta:
        model = FicheDePaie
        # exclude = ['owner',]
        fields= '__all__'

