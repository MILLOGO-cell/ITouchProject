from django.contrib import admin
from .models import Vente,ProduitVente,PerteMateriel,PerteVenteProduitContenant,ProduitConsigne,ProduitAvoirPris,Monnaie,DepenseVente,Credit,Client,AvanceRetenu

admin.site.register(AvanceRetenu)
admin.site.register(Client)
admin.site.register(Credit)
admin.site.register(DepenseVente)
admin.site.register(Monnaie)
admin.site.register(ProduitAvoirPris)
admin.site.register(ProduitConsigne)
admin.site.register(PerteMateriel)
admin.site.register(PerteVenteProduitContenant)
admin.site.register(ProduitVente)
admin.site.register(Vente)
