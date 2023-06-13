from django.db import models
from authentication.models import User
from gestiondesemployes.models import Employe
from shortuuid.django_fields import ShortUUIDField
import shortuuid
from gestiondesmateriels.models import Materiel 
from gestiondesproduits.models import Produit

class Monnaie(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE,null=True, blank=True)
    numero_ticket = ShortUUIDField(length = 8, max_length = 100, prefix = "tick_num",
        alphabet = "abc123"
    )
    montant = models.IntegerField()
    est_remis = models.BooleanField(default=False)
    delai = models.CharField(max_length=100, null=True,blank=True)
    date_remise = models.CharField(max_length=100, null=True,blank=True)
    date_emission = models.DateField(auto_now=True)
    
    def __str__(self):
        return self.date_emission 
    def generate_numero_ticket(self):
        return "Ticket_" + shortuuid.uuid()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.numero_ticket = self.generate_numero_ticket()
        super().save(*args, **kwargs)


class Vente(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE,null=True, blank=True)
    heure_debut = models.CharField(max_length=25)
    heure_fin = models.CharField(max_length=25)
    employe=models.ForeignKey(Employe, on_delete=models.CASCADE, null=True, blank=True)
    monnaie=models.ForeignKey(Monnaie, on_delete=models.CASCADE, null=True, blank=True)
    nv_fond_caisse = models.IntegerField()
    rep_fond_caisse = models.IntegerField()
    recette = models.IntegerField()
    autre_recette = models.IntegerField()
    manquant_surplus = models.IntegerField()
    est_inventaire = models.BooleanField(default=False) 
    date_creation = models.DateField(auto_now=True)
    date_modification = models.DateField(auto_now=True)

    def __str__(self):
        return self.date_creation
    
class AvanceRetenu(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE,null=True, blank=True)
    vente = models.ForeignKey(to=Vente, on_delete=models.SET_NULL,null=True, blank=True)
    employe = models.ForeignKey(to=Employe, on_delete=models.SET_NULL,null=True, blank=True)
    avance =  models.IntegerField()
    retenu = models.IntegerField()
    bonus = models.IntegerField()
    pour_boire = models.IntegerField()
    date_creation = models.DateField(auto_now=True)
    date_modification = models.DateField(auto_now=True)

    def __str__(self):
        return self.date_creation
    

class Client(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE,null=True, blank=True)
    nom =  models.CharField(max_length=150)
    prenom = models.CharField(max_length=250)
    contact = models.CharField(max_length=150)
    date_creation = models.DateField(auto_now=True)
    date_modification = models.DateField(auto_now=True)
    
    def __str__(self):
        return self.nom + self.prenom 
    
    
class Credit(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE,null=True, blank=True)
    vente = models.ForeignKey(to=Vente, on_delete=models.CASCADE)
    client = models.ForeignKey(to=Client, on_delete=models.CASCADE)
    numero_facture =  ShortUUIDField(length = 8, max_length = 100, prefix = "credit_",
        alphabet = "abc124"
    )
    montant = models.IntegerField()
    payer = models.BooleanField(default=False)
    date_paie = models.CharField(max_length=50,null=True,blank=True)
    date_creation = models.DateField(auto_now=True)

    def __str__(self):
        return self.date_creation
    
    def generate_numero_facture(self):
        return "fact_" + shortuuid.uuid()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.numero_facture = self.generate_numero_facture()
        super().save(*args, **kwargs)

class PerteMateriel(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE,null=True, blank=True)
    vente = models.ForeignKey(to=Vente, on_delete=models.CASCADE)
    materiel = models.ForeignKey(to=Materiel, on_delete=models.CASCADE,null=True, blank=True)
    quantite =  models.IntegerField()
    prix_retenu = models.IntegerField()
    date_creation = models.DateField(auto_now=True)
    date_modification = models.DateField(auto_now=True)
     
    def __str__(self):
        return self.date_creation
    
class DepenseVente(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE,null=True, blank=True)
    vente = models.ForeignKey(to=Vente, on_delete=models.CASCADE)
    nom = models.CharField(max_length=150)
    montant_dep = models.IntegerField()
    descriptif = models.TextField()
    date_creation = models.DateField(auto_now=True)
    date_modification = models.DateField(auto_now=True)
    
    def __str__(self):
        return self.date_creation
    
class ProduitVente(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE,null=True, blank=True)
    vente = models.ForeignKey(to=Vente, on_delete=models.CASCADE)
    produit = models.ForeignKey(to=Produit, on_delete=models.CASCADE,null=True, blank=True)
    report = models.IntegerField()
    prix_vente = models.IntegerField()
    montant_dep = models.IntegerField()
    reste = models.IntegerField()
    avarie = models.IntegerField()
    date_creation = models.DateField(auto_now=True)
    date_modification = models.DateField(auto_now=True)
    
    def __str__(self):
        return self.date_creation
    
     
class ProduitConsigne(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE,null=True, blank=True)
    produit_vente = models.ForeignKey(to=ProduitVente, on_delete=models.CASCADE)
    numero =  ShortUUIDField(length = 8, max_length = 100, prefix = "num_",
        alphabet = "abc123"
    )
    quantite = models.IntegerField()
    delais = models.CharField(max_length=50,null=True,blank=True)
    date_retour = models.DateField(auto_now=True)
    est_retourne = models.BooleanField(default=False)
    date_creation = models.DateField(auto_now=True)
    date_modification = models.DateField(auto_now=True)
    
    def __str__(self):
        return self.date_creation
    def generate_numero(self):
        return "num_" + shortuuid.uuid()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.numero = self.generate_numero()
        super().save(*args, **kwargs)

class ProduitAvoirPris(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE,null=True, blank=True)
    produit_vente = models.ForeignKey(to=ProduitVente, on_delete=models.CASCADE,null=True, blank=True)
    numero =  ShortUUIDField(length = 8, max_length = 100, prefix = "num_",
        alphabet = "abc123"
    )
    quantite = models.IntegerField()
    date= models.DateField(auto_now=True)
    est_servi = models.BooleanField(default=False)
    delais = models.CharField(max_length=50,null=True,blank=True)
    date_servi = models.DateField(auto_now=True)
    
    def __str__(self):
        return self.date_creation
    
    def generate_numero(self):
        return "num_" + shortuuid.uuid()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.numero = self.generate_numero()
        super().save(*args, **kwargs)
class PerteVenteProduitContenant(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE,null=True, blank=True)
    produit_vente = models.ForeignKey(to=ProduitVente, on_delete=models.CASCADE)
    quantite_contenu_simple =  models.IntegerField()
    quantite_contenant_plein = models.IntegerField()
    quantite_contenant_vide = models.IntegerField()
    date_creation = models.DateField(auto_now=True)
    date_modification = models.DateField(auto_now=True)
    
    def __str__(self):
        return self.date_creation