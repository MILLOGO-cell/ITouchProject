from django.contrib import admin
from .models import Materiel,CommandeMateriel,Fournisseur

admin.site.register(Materiel)
admin.site.register(CommandeMateriel)
admin.site.register(Fournisseur)
