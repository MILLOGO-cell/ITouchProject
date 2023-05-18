from django.urls import include, path
from rest_framework import routers
from .import views

router = routers.DefaultRouter()
router.register('materiel', views.MaterielViewSet)
router.register('fournisseur', views.FournisseurViewSet)
router.register('commande_materiel', views.CommandeMaterielViewSet)
urlpatterns = [
     path('', include(router.urls))
]