from django.db import models
from authentication.models import User
from shortuuid.django_fields import ShortUUIDField

class Categorie(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE,null=True, blank=True)
    nom = models.CharField(max_length=150) 
    
    def __str__(self):
        return self.nom 
    
class SousCategorie(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE,null=True, blank=True)
    nom = models.CharField(max_length=150)
    categorie = models.OneToOneField(Categorie,
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
    fabriquant = models.OneToOneField(Fabriquant, on_delete=models.SET_NULL, 
        null=True, blank=True)
    nom = models.CharField(max_length=150) 
    
    def __str__(self):
        return self.nom 

class TypeContenant(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE,null=True, blank=True)
    fabriquant = models.OneToOneField(Fabriquant,on_delete=models.SET_NULL, null=True, blank=True)
    nom = models.CharField(max_length=150) 
    prix_consigne = models.IntegerField(default=0)
    nombreContenant = models.IntegerField(default=0)
    
    def __str__(self):
        return self.nom 
    
class Produit(models.Model): 
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE,null=True, blank=True)
    categorie = models.OneToOneField(Categorie,on_delete=models.SET_NULL, null=True, blank=True )
    type_contenant = models.OneToOneField(TypeContenant,
        on_delete=models.SET_NULL, null=True, blank=True )
    nom = models.CharField(max_length=150)
    image = models.ImageField(upload_to='images/',blank=True,null=True)
    prix = models.CharField(max_length=50)
    seuil_min = models.IntegerField(default=10)
    description = models.TextField()
    is_active = models.BooleanField(default=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.nom 

class Fournisseur(models.Model):
    enseigne = models.CharField(max_length=100)
    email = models.EmailField(unique=True, null=True, blank=True)
    telephone = models.CharField(max_length=100)
    adresse = models.CharField(max_length=200)
    
    def __str__(self):
        return self.enseigne
    
class CommandeProduit(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    produit = models.ForeignKey(to=Produit, on_delete=models.SET_NULL,null=True, blank=True)
    fournisseur = models.OneToOneField(to=Fournisseur, on_delete=models.CASCADE,null=True, blank=True)
    num_bordereaux = ShortUUIDField(length = 8, max_length = 20, prefix = "Com_prod",
        alphabet = "abcdefg1234"
    )
    nom_livreur = models.CharField(max_length=100)
    prenom_livreur = models.CharField(max_length=250)
    montant_facture = models.IntegerField()
    montant_reel_facture = models.IntegerField()
    prix_achat_prod = models.IntegerField()
    quantite_prod = models.IntegerField()
    nombre_contenant_retourne = models.IntegerField()
    date = models.DateField(auto_now_add=True)
    # nombre_contenant_du = models.IntegerField()
    # prix_achat_contenant = models.IntegerField()
    # quantite_contenant = models.IntegerField()
    # prix_achat_emballage =  models.IntegerField()
    # quantite_emballage = models.IntegerField()
    
    def __str__(self):
        return self.num_bordereaux 

