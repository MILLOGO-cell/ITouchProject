from django.urls import include, path
from rest_framework import routers
from .import views

router = routers.DefaultRouter()
router.register('employe', views.EmployeViewset)
router.register('poste', views.PosteViewset)
router.register('etat_service', views.EtatServiceViewset)
router.register('fiche_de_paie', views.FicheView)
router.register(r'employes/fiche_de_paie/last', views.LastPaySlipView, basename='last_pay_slip')

urlpatterns = [
     path('', include(router.urls)),
]