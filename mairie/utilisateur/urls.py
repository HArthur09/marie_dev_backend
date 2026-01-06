from .views import UserViewSet
from rest_framework.routers import DefaultRouter
from django.urls import path, include


router = DefaultRouter()
router.register(r'Users', UserViewSet, basename='user')

urlpatterns = [
    path("", include(router.urls))
]
