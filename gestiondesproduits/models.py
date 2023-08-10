from django.db import models
from authentication.models import User
from django.contrib.auth import get_user_model
from shortuuid.django_fields import ShortUUIDField
import shortuuid
from django.db.models import UniqueConstraint, Q
from django.core.exceptions import ValidationError

class Categorie(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE,null=True, blank=True)
    nom = models.CharField(max_length=150) 
    def __str__(self):
        return self.nom   
    def save(self, *args, **kwargs):
        if Categorie.objects.filter(owner=self.owner, nom=self.nom).exclude(pk=self.pk).exists():
            raise ValidationError("Une catégorie avec le même nom existe déjà pour cet utilisateur.")
        super().save(*args, **kwargs)
    
class SousCategorie(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE,null=True, blank=True)
    nom = models.CharField(max_length=150)
    categorie = models.ForeignKey(Categorie,
        on_delete=models.SET_NULL, null=True, blank=True)
   
    def __str__(self):
        return self.nom 
    class Meta:
        constraints = [
            UniqueConstraint(fields=['owner', 'categorie', 'nom'], name='unique_owner_sous-categorie_nom')
        ]
    
    def save(self, *args, **kwargs):
        if SousCategorie.objects.filter(owner=self.owner, nom=self.nom).exclude(pk=self.pk).exists():
            raise ValidationError("Une sous-catégorie avec le même nom existe déjà pour cet utilisateur.")
        super().save(*args, **kwargs) 
         
    def clean(self):
        # Vérifier l'unicité du nom du type de contenant pour le fabricant spécifique à l'utilisateur
        if SousCategorie.objects.filter(
            owner=self.owner, fabriquant=self.categorie, nom=self.nom
        ).exclude(pk=self.pk).exists():
            raise ValidationError(
                f"Une catégorie avec le nom '{self.nom}' existe déjà pour cette sous-catégorie"
            )

class Fabriquant(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE,null=True, blank=True)
    nom = models.CharField(max_length=150) 
    
    def __str__(self):
        return self.nom 
    
    def save(self, *args, **kwargs):
        if Fabriquant.objects.filter(owner=self.owner, nom=self.nom).exclude(pk=self.pk).exists():
            raise ValidationError("Un fabriquant avec le même nom existe déjà pour cet utilisateur.")
        super().save(*args, **kwargs)
        
class Emballage(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE,null=True,blank=True)
    fabriquant = models.ForeignKey(Fabriquant, on_delete=models.SET_NULL, 
        null=True, blank=True)
    nom = models.CharField(max_length=150) 
    
    def __str__(self):
        return self.nom 
    class Meta:
        constraints = [
            UniqueConstraint(fields=['owner', 'fabriquant', 'nom'], name='unique_owner_emballage_nom')
        ]
    
    def save(self, *args, **kwargs):
        if Emballage.objects.filter(owner=self.owner, nom=self.nom).exclude(pk=self.pk).exists():
            raise ValidationError("Un emballage avec le même nom existe déjà pour cet utilisateur.")
        super().save(*args, **kwargs)
        
    
class TypeContenant(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE,null=True, blank=True)
    fabriquant = models.ForeignKey(Fabriquant,on_delete=models.SET_NULL, null=True, blank=True)
    nom = models.CharField(max_length=150) 
    prix_consigne = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nom 

    class Meta:
        constraints = [
            UniqueConstraint(fields=['owner', 'fabriquant', 'nom',], name='unique_owner_typecontenant_nom')
        ]
    
    def save(self, *args, **kwargs):
        if TypeContenant.objects.filter(owner=self.owner, nom=self.nom).exclude(pk=self.pk).exists():
            raise ValidationError("Un type de contenant avec le même nom existe déjà pour cet utilisateur.")
        super().save(*args, **kwargs)  
        
     
class UniteVolume(models.Model):
    # owner = models.ForeignKey(to=User, on_delete=models.CASCADE,null=True, blank=True)
    valeur = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.valeur 
    
    # def save(self, *args, **kwargs):
    #     if self.owner and UniteVolume.objects.filter(owner=self.owner, valeur=self.valeur).exclude(pk=self.pk).exists():
    #         raise ValidationError("Un volume avec la même valeur existe déjà pour cet utilisateur.")
    #     super().save(*args, **kwargs)
        
class Pays(models.Model):
    nom = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nom


class Produit(models.Model): 
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE,null=True, blank=True)
    sous_categorie = models.ForeignKey(SousCategorie,on_delete=models.SET_NULL, null=True, blank=True )
    type_contenant = models.ForeignKey(TypeContenant,
        on_delete=models.SET_NULL, null=True, blank=True )
    stock_courant = models.CharField(max_length=50,null=True, blank=True)
    nom = models.CharField(max_length=150)
    image = models.ImageField(upload_to='images/',blank=True,null=True)
    prix = models.CharField(max_length=50,null=True, blank=True)
    seuil_min = models.CharField(max_length=50,null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    volume = models.ForeignKey(UniteVolume,on_delete=models.SET_NULL, null=True, blank=True)
    brouillon = models.BooleanField(default=True,blank=True)
    commun = models.BooleanField(default=False)
    pays = models.ForeignKey(Pays, on_delete=models.SET_NULL, null=True, blank=True)
    en_vente = models.BooleanField(default=False,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.nom 
    
    def save(self, *args, **kwargs):
        # Si le produit est défini comme "commun", définir le propriétaire sur None
        if self.commun:
            self.owner = None
        
        super().save(*args, **kwargs)

        
class FournisseurProduit(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True)
    enseigne = models.CharField(max_length=200)
    telephone = models.CharField(max_length=50)
    email = models.EmailField(max_length=150, null=True, blank=True)
    whatsapp = models.CharField(max_length=20, null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.enseigne + self.email
    
    def save(self, *args, **kwargs):
        # Vérifier si un autre produit de l'utilisateur a le même nom  
        if FournisseurProduit.objects.filter(owner=self.owner, enseigne=self.enseigne).exclude(pk=self.pk).exists():
            raise ValidationError("Un fournisseur avec le même nom existe déjà pour cet utilisateur.")
        super().save(*args, **kwargs)
    
class CommandeProduit(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    produit = models.ForeignKey(to=Produit, on_delete=models.SET_NULL,null=True, blank=True)
    fournisseur = models.ForeignKey(to=FournisseurProduit, on_delete=models.CASCADE,null=True, blank=True)
    num_bordereaux = ShortUUIDField(length = 8, max_length = 100, prefix = "prod_",
        alphabet = "ab12"
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
        return "prod_" + shortuuid.uuid()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.num_bordereaux = self.generate_com_mat()
        super().save(*args, **kwargs)


