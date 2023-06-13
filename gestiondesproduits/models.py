from django.db import models
from authentication.models import User
from shortuuid.django_fields import ShortUUIDField
import shortuuid

class Categorie(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE,null=True, blank=True)
    nom = models.CharField(max_length=150) 
    
    def __str__(self):
        return self.nom 
    
class SousCategorie(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE,null=True, blank=True)
    nom = models.CharField(max_length=150)
    categorie = models.ForeignKey(Categorie,
        on_delete=models.SET_NULL, null=True, blank=True)
   
    def __str__(self):
        return self.nom 

class Fabriquant(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE,null=True, blank=True)
    nom = models.CharField(max_length=150) 
    
    def __str__(self):
        return self.nom 

class Emballage(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE,null=True,blank=True)
    fabriquant = models.ForeignKey(Fabriquant, on_delete=models.SET_NULL, 
        null=True, blank=True)
    nom = models.CharField(max_length=150) 
    
    def __str__(self):
        return self.nom 

class TypeContenant(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE,null=True, blank=True)
    fabriquant = models.ForeignKey(Fabriquant,on_delete=models.SET_NULL, null=True, blank=True)
    nom = models.CharField(max_length=150) 
    prix_consigne = models.CharField(max_length=100)
    nombreContenant = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nom 
    
class Produit(models.Model): 
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE,null=True, blank=True)
    categorie = models.ForeignKey(Categorie,on_delete=models.SET_NULL, null=True, blank=True )
    type_contenant = models.ForeignKey(TypeContenant,
        on_delete=models.SET_NULL, null=True, blank=True )
    stock_courant = models.CharField(max_length=50,null=True, blank=True)
    nom = models.CharField(max_length=150)
    image = models.ImageField(upload_to='images/',blank=True,null=True)
    prix = models.CharField(max_length=50)
    seuil_min = models.CharField(max_length=50)
    description = models.TextField()
    is_active = models.BooleanField(default=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.nom 

class FournisseurProduit(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True)
    enseigne = models.CharField(max_length=200)
    telephone = models.CharField(max_length=50)
    email = models.EmailField(max_length=150, null=True, blank=True)
    whatapp = models.CharField(max_length=20, null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.enseigne + self.email
    
class CommandeProduit(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    produit = models.ForeignKey(to=Produit, on_delete=models.SET_NULL,null=True, blank=True)
    fournisseur = models.ForeignKey(to=FournisseurProduit, on_delete=models.CASCADE,null=True, blank=True)
    num_bordereaux = ShortUUIDField(length = 8, max_length = 100, prefix = "Com_prod",
        alphabet = "abc123"
    )
    nom_livreur = models.CharField(max_length=100)
    prenom_livreur = models.CharField(max_length=250)
    montant_facture = models.IntegerField()
    montant_reel_facture = models.IntegerField()
    prix_achat_prod = models.IntegerField()
    quantite = models.IntegerField(null=True, blank=True)
    nombre_contenant_retourne = models.IntegerField()
    date = models.DateField(auto_now_add=True)
    nombre_contenant_du = models.IntegerField(null=True,blank=True)
    prix_achat_contenant = models.IntegerField(null=True,blank=True)
    quantite_contenant = models.IntegerField(null=True,blank=True)
    prix_achat_emballage =  models.IntegerField(null=True,blank=True)
    quantite_emballage = models.IntegerField(null=True,blank=True)
    
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


