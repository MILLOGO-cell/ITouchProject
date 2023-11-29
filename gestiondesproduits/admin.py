from django.contrib import admin
from .models import Produit, Categorie,SousCategorie,TypeContenant,Emballage,Fabriquant, Pays,FournisseurProduit,CommandeProduit,UniteVolume

admin.site.register(Produit)
admin.site.register(Categorie)
admin.site.register(SousCategorie)
admin.site.register(TypeContenant)
admin.site.register(Emballage)
admin.site.register(Fabriquant)
admin.site.register(Pays)
admin.site.register(FournisseurProduit)
admin.site.register(UniteVolume)
admin.site.register(CommandeProduit)
