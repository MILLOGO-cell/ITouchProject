from django.db import models
from gestiondesproduits.models import Produit,Fournisseur
from authentication.models import User
from shortuuid.django_fields import ShortUUIDField

class Materiel(models.Model):
    nom = models.CharField(max_length=100)
    prix_consigne = models.IntegerField()
    date_acquisition = models.DateField(auto_now=True)
    adresse = models.CharField(max_length=200)
    description = models.TextField()
    stock_courant = models.CharField(max_length=50)
    is_active = models.BooleanField(default=False)
    
    def __str__(self):
        return self.nom

class CommandeMateriel(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    produit = models.ForeignKey(to=Produit, on_delete=models.SET_NULL,null=True, blank=True)
    fournisseur = models.OneToOneField(to=Fournisseur, on_delete=models.CASCADE,null=True, blank=True)
    num_bordereaux = ShortUUIDField(length = 8, max_length = 20, prefix = "Com_mat",
        alphabet = "abcdefg1234"
    )
    nom_livreur = models.CharField(max_length=100)
    prenom_livreur = models.CharField(max_length=250)
    montant_facture = models.IntegerField()
    montant_reel_facture = models.IntegerField()
    
    def __str__(self):
        return self.num_bordereaux 

