from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('utilisateurs/', include('authentication.urls')),
    path('employes/', include('gestiondesemployes.urls')),
    path('produits/', include('gestiondesproduits.urls')),
]
