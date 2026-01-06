from .views import MariageViewSet, DocumentMariageViewSet, HommeViewSet, FemmeViewSet, test, envoyer_planning_manuel, statut_envoi
from rest_framework.routers import DefaultRouter
from django.urls import path, include


router = DefaultRouter()
router.register(r'mariages', MariageViewSet, basename='mariage')
router.register(r'documents', DocumentMariageViewSet, basename='documentmariage')
router.register(r'hommes', HommeViewSet, basename='homme')
router.register(r'femmes', FemmeViewSet, basename='femme')
#router.register(r'test', test, basename='test')
#router.register(r'envoyer-planning', envoyer_planning_manuel, basename='envoyer_planning')
#router.register(r'statut-envoi', statut_envoi, basename='statut_envoi')

urlpatterns = [
    path("", include(router.urls)),
    path("envoyer-planning/", envoyer_planning_manuel, name="envoyer_planning_manuel"),
    path("statut-envoi/", statut_envoi, name="statut_envoi"),
    #path("test-whatsapp/", test_whatsapp, name="test_whatsapp"),
]