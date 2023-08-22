from django.urls import include, path
from rest_framework import routers
from .import views

router = routers.DefaultRouter()
router.register('ventes', views.VenteViewSet)
router.register('avances_retenus', views.AvanceRetenuViewSet)
router.register('monnaie', views.MonnaieViewSet)
router.register('clients', views.ClientViewSet)
router.register('credits', views.CreditViewSet)
router.register('pertes_materiels', views.PerteMaterielViewSet)
router.register('depenses_ventes', views.DepenseVenteViewSet)
router.register('produit_ventes', views.ProduitVenteViewSet)
router.register('produit_consignes', views.ProduitConsigneViewSet)
router.register('produit_avoir_pris', views.ProduitAvoirPrisViewSet)
router.register('pertes_contenants', views.PerteVenteProduitContenantViewSet)
urlpatterns = [
    path('', include(router.urls)),
    path('vente-precedente/', views.VenteViewSet.as_view({'get': 'vente_precedente'}), name='vente-precedente'),
    path('produitvente/latest_produitvente_for_product/<int:produit_id>/', views.ProduitVenteViewSet.as_view({'get': 'latest_produitvente_for_product'}), name='latest_produitvente_for_product'),
    path('produitsventes/vente/<int:vente_id>/', views.ProduitVenteViewSet.as_view({'get': 'list_produits_vente_by_vente'}), name='produitsvente-by-vente'),
    path('statistiques/', views.StatistiquesView.as_view(), name='statistiques'),
]