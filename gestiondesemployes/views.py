from django.shortcuts import render
from .models import Employe, Poste
from .serializers import EmployeSerializer, PosteSerializer 
from rest_framework import viewsets, permissions
from .permissions import IsOwner

class PosteViewset(viewsets.ModelViewSet):
    queryset = Poste.objects.all()
    serializer_class = PosteSerializer
    # permission_classes = (permissions.IsAuthenticated,)
    
    # def perform_create(self,serializer):
    #     return serializer.save(owner=self.request.user)
    
    # def get_queryset(self):
    #     return self.queryset.filter(owner=self.request.user)

class EmployeViewset(viewsets.ModelViewSet):
    queryset = Employe.objects.all()
    serializer_class = EmployeSerializer 
    # permission_classes = (permissions.IsAuthenticated,)
    
    # def perform_create(self,serializer):
    #     return serializer.save(owner=self.request.user)
    
    # def get_queryset(self):
    #     return self.queryset.filter(owner=self.request.user)
