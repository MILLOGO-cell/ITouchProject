from django.db import models
from authentication.models import User
from shortuuid.django_fields import ShortUUIDField
import shortuuid

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
    image = models.ImageField(upload_to='images/',blank=True,null=True)
    poste = models.ForeignKey(Poste, null=True, blank=True, on_delete=models.SET_NULL)
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

    def get_poste_intitule(self):
        if self.poste:
            return self.poste.intitule
        else:
            return ""


class FicheDePaie(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE,null=True, blank=True)
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE, null=True, blank=True)
    num_fich = ShortUUIDField( max_length = 100, prefix = "Fiche_",
        alphabet = "abc123"
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
        return self.num_fich
    
    def generate_num_fich(self):
        return "Fiche_paie_" + shortuuid.uuid()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.num_fich = self.generate_num_fich()
        super().save(*args, **kwargs)
    