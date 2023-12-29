from django.urls import path, include

from rest_framework.routers import DefaultRouter

from rest_framework.authtoken import views as authview
from poke_api import views

router = DefaultRouter()
router.register('profile', views.UserProfileViewset)
router.register('Pokemon', views.PokemonViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('token/', authview.obtain_auth_token)
]
