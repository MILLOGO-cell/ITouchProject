from django.contrib import admin
from .models import Poste,Employe,FicheDePaie,EtatService

admin.site.register(Poste)
admin.site.register(Employe)
admin.site.register(FicheDePaie)
admin.site.register(EtatService)