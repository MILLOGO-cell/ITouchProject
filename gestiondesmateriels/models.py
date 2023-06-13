from django.db import models
from authentication.models import User
from shortuuid.django_fields import ShortUUIDField
import shortuuid


class Materiel(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True)
    nom = models.CharField(max_length=100)
    prix_consigne = models.CharField(max_length=350)
    date_acquisition = models.DateField(auto_now=True)
    description = models.TextField()
    stock_courant = models.CharField(max_length=50)
    is_active = models.BooleanField(default=False)
    
    def __str__(self):
        return self.nom

class Fournisseur(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True)
    enseigne = models.CharField(max_length=200)
    telephone = models.CharField(max_length=50)
    email = models.EmailField(max_length=150, null=True, blank=True)
    whatapp = models.CharField(max_length=20, null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.enseigne + self.email

class CommandeMateriel(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    quantite = models.IntegerField(null=True, blank=True)
    materiel = models.ForeignKey(to=Materiel, on_delete=models.CASCADE, null=True, blank=True)
    fournisseur = models.ForeignKey(to=Fournisseur, on_delete=models.CASCADE,null=True, blank=True)
    num_bordereaux = ShortUUIDField(length = 8, max_length = 30, prefix = "Com_mat",
        alphabet = "abc123"
    )
    nom_livreur = models.CharField(max_length=100)
    prenom_livreur = models.CharField(max_length=250)
    montant_facture = models.IntegerField()
    montant_reel_facture = models.IntegerField()
    date_creation = models.DateTimeField(auto_now_add=True,null=True,blank=True)

    def __str__(self):
        return self.num_bordereaux 
    
    class Meta:
        unique_together = []
    
    def generate_com_mat(self):
        return "Com_mat" + shortuuid.uuid()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.num_bordereaux = self.generate_com_mat()
        super().save(*args, **kwargs)
