from django.db import models

class Vente(models.Model):
    heure_debut = models.DateField()
    heure_fin = models.DateField()
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
    vente = models.ForeignKey(to=Vente, on_delete=models.SET_NULL,null=True, blank=True)
    avance =  models.IntegerField()
    retenu = models.IntegerField()
    bonus = models.IntegerField()
    pour_boire = models.IntegerField()
    date_creation = models.DateField(auto_now=True)
    date_modification = models.DateField(auto_now=True)

    def __str__(self):
        return self.date_creation
class Monnaie(models.Model):
    vente = models.ForeignKey(to=Vente, on_delete=models.CASCADE)
    numero_ticket = models.CharField(max_length=150)
    montant = models.IntegerField()
    est_remis = models.CharField(max_length=150)
    delai = models.DateField(auto_now=False)
    date_remise = models.DateField(auto_now=False)
    date_emission = models.DateField(auto_now=False)
    
    def __str__(self):
        return self.date_emission
class Client(models.Model):
    nom =  models.CharField(max_length=150)
    prenom = models.CharField(max_length=250)
    contact = models.CharField(max_length=150)
    date_creation = models.DateField(auto_now=True)
    date_modification = models.DateField(auto_now=True)
    
    def __str__(self):
        return self.nom + self.prenom
class Credit(models.Model):
    vente = models.ForeignKey(to=Vente, on_delete=models.CASCADE)
    client = models.ForeignKey(to=Client, on_delete=models.CASCADE)
    numero_facture =  models.IntegerField()
    montant = models.IntegerField()
    payer = models.BooleanField(default=False)
    date_paie = models.DateField(auto_now=False)
    date_creation = models.DateField(auto_now=True)

    def __str__(self):
        return self.date_creation
class PerteMateriel(models.Model):
    vente = models.ForeignKey(to=Vente, on_delete=models.CASCADE)
    quantite =  models.IntegerField()
    prix_retenu = models.IntegerField()
    date_creation = models.DateField(auto_now=True)
    date_modification = models.DateField(auto_now=True)
     
    def __str__(self):
        return self.date_creation
class DepenseVente(models.Model):
    vente = models.ForeignKey(to=Vente, on_delete=models.CASCADE)
    nom = models.CharField(max_length=150)
    montant_dep = models.IntegerField()
    descriptif = models.TextField()
    date_creation = models.DateField(auto_now=True)
    date_modification = models.DateField(auto_now=True)
    
    def __str__(self):
        return self.date_creation
class ProduitVente(models.Model):
    vente = models.ForeignKey(to=Vente, on_delete=models.CASCADE)
    report = models.IntegerField()
    prix_vente = models.IntegerField()
    montant_dep = models.IntegerField()
    reste = models.IntegerField()
    avarie = models.IntegerField()
    date_creation = models.DateField(auto_now=True)
    date_modification = models.DateField(auto_now=True)
    
    def __str__(self):
        return self.date_creation
    
    # def save(sef, *args, **kwargs):
    #     self.report =
class ProduitConsigne(models.Model):
    produit_vente = models.ForeignKey(to=ProduitVente, on_delete=models.CASCADE)
    numero =  models.IntegerField()
    quantite = models.IntegerField()
    delais = models.DateField(auto_now=False)
    date_retour = models.DateField(auto_now=True)
    est_retourne = models.BooleanField(default=False)
    date_creation = models.DateField(auto_now=True)
    date_modification = models.DateField(auto_now=True)
    
    def __str__(self):
        return self.date_creation
class ProduitAvoirPris(models.Model):
    produit_vente = models.ForeignKey(to=ProduitVente, on_delete=models.CASCADE)
    numero =  models.IntegerField()
    quantite = models.IntegerField()
    date= models.DateField(auto_now=True)
    est_servi = models.BooleanField(default=False)
    delais = models.DateField(auto_now=False)
    date_servi = models.DateField(auto_now=True)
    
    def __str__(self):
        return self.date_creation
class PerteVenteProduitContenant(models.Model):
    produit_vente = models.ForeignKey(to=ProduitVente, on_delete=models.CASCADE)
    quantite_contenu_simple =  models.IntegerField()
    quantite_contenant_plein = models.IntegerField()
    quantite_contenant_vide = models.IntegerField()
    date_creation = models.DateField(auto_now=True)
    date_modification = models.DateField(auto_now=True)
    
    def __str__(self):
        return self.date_creation