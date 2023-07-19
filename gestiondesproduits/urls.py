from django.urls import include, path
from rest_framework import routers
from .import views

router = routers.DefaultRouter()
router.register('produit', views.ProductViewSet)
router.register('volume', views.UniteVolumeViewSet)
router.register('categorie', views.CategorieViewSet)
router.register('sous_categorie', views.SousCategorieViewSet)
router.register('emballage', views.EmballageViewSet)
router.register('type_contenant', views.TypeContenantViewSet)
router.register('fabriquant', views.FabriquantViewSet)
router.register('fournisseur_produit', views.FournisseurProduitViewSet)
router.register('commande_produit', views.CommandeProduitViewSet)

urlpatterns = [
    path('', include(router.urls))
]