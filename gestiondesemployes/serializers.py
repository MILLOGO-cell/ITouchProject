from rest_framework import serializers
from .models import Employe,Poste

class PosteSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Poste
        exclude = ['owner',]
        
class EmployeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Employe
        exclude = ['owner',]
    
        
 
        
