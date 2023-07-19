from django.db import models
from authentication.models import User
from gestiondesemployes.models import Employe
from shortuuid.django_fields import ShortUUIDField
import shortuuid
from gestiondesmateriels.models import Materiel 
from gestiondesproduits.models import Produit
from django.db.models.signals import pre_save, pre_init
from django.dispatch import receiver
from django.utils import timezone
from django.db.models import Sum

class Monnaie(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE,null=True, blank=True)
    numero_ticket = ShortUUIDField(length = 8, max_length = 100, prefix = "tick_num",
        alphabet = "ab12"
    )
    montant = models.IntegerField()
    est_remis = models.BooleanField(default=False)
    delai = models.CharField(max_length=100, null=True,blank=True)
    date_remise = models.CharField(max_length=100, null=True,blank=True)
    date_emission = models.DateField(auto_now=True)
    
    def __str__(self):
        return self.date_emission 
    def generate_numero_ticket(self):
        return "Num_" + shortuuid.uuid()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.numero_ticket = self.generate_numero_ticket()
        super().save(*args, **kwargs)


class Vente(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True, blank=True)
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE, null=True, blank=True)
    monnaie = models.ForeignKey(Monnaie, on_delete=models.CASCADE, null=True, blank=True)
    nv_fond_caisse = models.IntegerField(null=True, blank=True)
    rep_fond_caisse = models.IntegerField(null=True, blank=True)
    recette = models.IntegerField(null=True, blank=True)
    autre_recette = models.IntegerField(null=True, blank=True)
    recette_attendue = models.IntegerField(null=True, blank=True)
    surplus = models.IntegerField(null=True, blank=True)
    manquant = models.IntegerField(null=True, blank=True)
    est_inventaire = models.BooleanField(default=False)
    # date_debut = models.DateTimeField(auto_now_add=False,null=True,blank=True)
    date_debut = models.CharField(max_length=250,null=True,blank=True)
    date_fin = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now_add=True,null=True,blank=True)

    def __str__(self):
        return str(self.date_creation)
    
    def calculate_recette_attendue(self):
        recette_attendue = self.produitvente_set.aggregate(total_recette=Sum('prix_vente'))['total_recette']
        self.recette_attendue = recette_attendue or 0
        self.surplus = max(0, self.recette_attendue - self.recette)
        self.manquant = max(0, self.recette - self.recette_attendue)
    
    def save(self, *args, **kwargs):
        if self.date_fin is not None:
            self.calculate_recette_attendue()
        else:
            self.recette_attendue = None
            self.surplus = None
            self.manquant = None
        super().save(*args, **kwargs)

@receiver(pre_save, sender=Vente)
def set_date_debut_rep_fond_caisse(sender, instance, **kwargs):
    previous_sale = Vente.objects.filter(owner=instance.owner).exclude(pk=instance.pk).order_by('-date_creation').first()
    if previous_sale:
        if previous_sale.date_fin is not None:
            instance.date_debut = previous_sale.date_fin
            instance.rep_fond_caisse = previous_sale.nv_fond_caisse
        else:
            raise Exception("La vente précédente n'est pas terminée, impossible de créer une nouvelle vente.")
    elif not Vente.objects.exists():
        instance.date_debut = timezone.now()
        instance.rep_fond_caisse = 0




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
    numero_facture =  ShortUUIDField(length = 8, max_length = 100, prefix = "cred_",
        alphabet = "ab12"
    )
    montant = models.IntegerField()
    payer = models.BooleanField(default=False)
    date_paie = models.CharField(max_length=50,null=True,blank=True)
    date_creation = models.DateField(auto_now=True)

    def __str__(self):
        return self.date_creation
    
    def generate_numero_facture(self):
        return "cred_" + shortuuid.uuid()

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
    quantite = models.IntegerField(null=True, blank=True)
    report = models.IntegerField(null=True, blank=True)
    prix_vente = models.IntegerField(null=True, blank=True)
    reste = models.IntegerField()
    avarie = models.IntegerField()
    date_creation = models.DateField(auto_now=True)
    date_modification = models.DateField(auto_now=True)
    
    def __str__(self):
        return str(self.date_creation)

    def save(self, *args, **kwargs):
        if self.produit:
            self.prix_vente = int(self.produit.prix) if self.produit.prix is not None else 0

        # if self.pk is None:
        #     # Nouvelle instance de ProduitVente, initialiser report avec reste du précédent
        #     previous_produitvente = ProduitVente.objects.filter(
        #         vente=self.vente,
        #         produit=self.produit
        #     ).order_by('-date_creation').first()
        #     if previous_produitvente:
        #         self.report = previous_produitvente.reste
        #     else:
        #         self.report = 0

        # super().save(*args, **kwargs)
        # if self.produit and  int(self.produit.stock_courant) :
        #     self.produit.stock_courant = int(self.produit.stock_courant)-1
        #     self.produit.save()
        super().save(*args, **kwargs)

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
    prix_consigne = models.IntegerField(null=True, blank=True)
    date_creation = models.DateField(auto_now=True)
    date_modification = models.DateField(auto_now=True)
    
    def __str__(self):
        return self.date_creation