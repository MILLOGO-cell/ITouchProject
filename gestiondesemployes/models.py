from django.db import models
from authentication.models import User
from shortuuid.django_fields import ShortUUIDField

class Poste(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE,null=True, blank=True)
    intitule = models.CharField(max_length=150)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.intitule
        
class Employe(models.Model):
    ETAT_DE_SERVICE =(
        ('ACTIF','Actif'),('INACTIF','Inactif'),('CONGES','Congés'),
        ('SUSPENDU','Suspendu'),('RENVOYE','Renvoyé'),
    )
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE,null=True, blank=True)
    nom = models.CharField(max_length=150)
    prenom = models.CharField(max_length=255)
    email = models.EmailField(unique=True, null=True, blank=True)
    poste = models.OneToOneField(Poste, null=True, blank=True,on_delete=models.SET_NULL)
    statut = models.CharField(max_length=9, choices=ETAT_DE_SERVICE, default='INACTIF')
    infoPiece = models.CharField(max_length=255)
    telephone = models.CharField(max_length=20)
    infoPersoContact = models.CharField(max_length=255)
    salaire_base = models.CharField(max_length=50,null=True)
    Commentaire = models.TextField(null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.nom + self.prenom

class FicheDePaie(models.Model):
    num_fich = ShortUUIDField(length = 8, max_length = 20, prefix = "Fiche_paie",
        alphabet = "abcdefg1234"
    )
    date_debut = models.DateField(auto_now_add=True)
    date_fin = models.DateField(auto_now_add=True)
    pertes = models.IntegerField()
    manquants = models.IntegerField()
    pour_boires = models.IntegerField()
    bonus = models.IntegerField()
    credit = models.IntegerField()
    avances_retenues = models.IntegerField()
    salaire_base = models.IntegerField()
    salaire_recu = models.IntegerField()
    montant_correction = models.IntegerField()
    commentaire = models.TextField()
    
    def __str__(self):
        return self.num_fiche
    
    