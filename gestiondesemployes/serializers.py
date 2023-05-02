from rest_framework import serializers
from .models import Employe,Poste

class PosteSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Poste
        # exclude = ['owner',]
        fields=('__all__')
        
class EmployeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Employe
        # exclude = ['owner',]
    
        fields=('__all__')
 
        
