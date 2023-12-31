from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import filters

from drf_spectacular.utils import extend_schema, extend_schema_view


from poke_api import serializers
from poke_api import models
from poke_api import permissions


@extend_schema(tags=['Operations on User Profiles'])
@extend_schema_view(list=extend_schema(description="List Users", summary="List Users"),
                    retrieve=extend_schema(summary="Get a User Profile"))
class UserProfileViewset(viewsets.ModelViewSet):
    """Handle creating and updating Profiles"""
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = [TokenAuthentication,]
    permission_classes = [permissions.UpdateOwnProfile,]
    filter_backends = [filters.SearchFilter,]
    search_fields = ['username', 'email',]


class PokemonViewSet(viewsets.ModelViewSet):
    """Handle creating and updating Pokemon"""
    serializer_class = serializers.PokemonSerializer
    queryset = models.Pokemon.objects.all()
    authentication_classes = [TokenAuthentication,]
    permission_classes = [permissions.UpdateUserPokemonList, IsAuthenticatedOrReadOnly]
