from django.urls import include, path
from rest_framework import routers
from .import views

router = routers.DefaultRouter()
router.register('employe', views.EmployeViewset)
router.register('poste', views.PosteViewset)
urlpatterns = [
     path('', include(router.urls))
]