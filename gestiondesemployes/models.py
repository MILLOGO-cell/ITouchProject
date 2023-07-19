from django.db import models
from authentication.models import User
from shortuuid.django_fields import ShortUUIDField
import shortuuid
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.http import HttpResponseBadRequest
class Poste(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE,null=True, blank=True)
    intitule = models.CharField(max_length=150, unique=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.intitule
     
    def clean(self):
        super().clean()
        # Vérifier si un autre poste avec le même intitulé existe pour le même utilisateur
        if Poste.objects.filter(owner=self.owner, intitule=self.intitule).exists():
            raise ValidationError("Ce poste existe déjà pour cet utilisateur.")
        
class EtatService(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE,null=True, blank=True)
    etat_service = models.CharField(max_length=50)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.etat_service 
     
    def clean(self):
        super().clean()
        # Vérifier si un autre état de service avec le même nom existe pour le même utilisateur
        if EtatService.objects.filter(owner=self.owner, etat_service=self.etat_service).exists():
            raise ValidationError("Cet état de service existe déjà pour cet utilisateur.")
class Employe(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True, blank=True)
    statut = models.ForeignKey(EtatService, on_delete=models.CASCADE, null=True, blank=True)
    nom = models.CharField(max_length=150, null=True, blank=True)
    prenom = models.TextField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    poste = models.ForeignKey(Poste, null=True, blank=True, on_delete=models.SET_NULL)
    infoPiece = models.TextField( null=True, blank=True)
    telephone = models.CharField(max_length=20, null=True, blank=True)
    whatsapp = models.CharField(max_length=20,null=True,blank=True)
    infoPersoContact = models.TextField( null=True, blank=True)
    salaire_base = models.CharField(max_length=50, null=True,blank=True)
    Commentaire = models.TextField(null=True, blank=True)
    motif = models.CharField(max_length=50, null=True, blank=True)
    taux_salaire = models.CharField(max_length=50, null=True, blank=True)
    date_attribution_poste=models.DateTimeField(auto_now_add=False,null=True,blank=True)
    date_debut_poste = models.DateTimeField(null=True, blank=True)
    date_fin_poste = models.DateTimeField(null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nom} {self.prenom}"

    def get_poste_intitule(self):
        if self.poste:
            return self.poste.intitule
        else:
            return ""

    
        
    def clean(self):
        super().clean()
        if self.pk:
            fiche_de_paie_existe = FicheDePaie.objects.filter(employe=self).exists()
            if fiche_de_paie_existe and self.statut_id != self._original_statut_id:
                raise ValidationError("Impossible de changer le statut de l'employé. Veuillez générer la fiche de paie avant de modifier le statut.")
        
class FicheDePaie(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE,null=True, blank=True)
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE, null=True, blank=True)
    num_fich = ShortUUIDField( max_length = 100, prefix = "Fiche_",
        alphabet = "ab12"
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
        return "Fiche_" + shortuuid.uuid()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.num_fich = self.generate_num_fich()
        super().save(*args, **kwargs)
    