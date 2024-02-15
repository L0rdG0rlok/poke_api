from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from poke_api.models import Pokemon
from poke_api.permissions import UpdateUserPokemonList


class UpdateUserPokemonListPermissionTestCase(TestCase):
    def setUp(self):
        # Create a user for testing using the custom user model
        User = get_user_model()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword", email="test@test.com"
        )

        # Create another user for testing
        self.other_user = User.objects.create_user(
            username="otheruser", password="otherpassword", email="othertest@test.com"
        )

        # Create a Pokemon owned by the first user
        self.user_pokemon = Pokemon.objects.create(
            name="Pikachu",
            height=2,
            weight=3,
            sprite="pikachu.png",
            type="Electric",
            owner=self.user,
        )

        # Create an APIClient instance
        self.client = APIClient()

    def test_has_object_permission_safe_methods(self):
        permission = UpdateUserPokemonList()

        # Simulate authentication for the request
        self.client.force_authenticate(user=self.user)

        # Make a GET request to the user's Pokemon detail endpoint
        response = self.client.get(f"/api/Pokemon/{self.user_pokemon.id}/")

        # Check if has_object_permission allows safe methods (GET)
        self.assertTrue(
            permission.has_object_permission(
                response.wsgi_request, None, self.user_pokemon
            )
        )

    def test_has_object_permission_owner(self):
        permission = UpdateUserPokemonList()

        # Simulate authentication for the request
        self.client.force_authenticate(user=self.user)

        # Make a PATCH request to the user's Pokemon detail endpoint
        response = self.client.patch(f"/api/Pokemon/{self.user_pokemon.id}/")

        # Check if has_object_permission allows the owner to edit
        self.assertTrue(
            permission.has_object_permission(
                response.wsgi_request, None, self.user_pokemon
            )
        )

    def test_has_object_permission_non_owner(self):
        """Test if has_object_permission denies non-owner from editing"""
        permission = UpdateUserPokemonList()

        # Simulate authentication for the request with a non-owner
        self.client.force_authenticate(user=self.other_user)

        # Make a PATCH request to the user's Pokemon detail endpoint
        response = self.client.patch(f"/api/Pokemon/{self.user_pokemon.id}/")

        # Check if has_object_permission denies a non-owner from editing
        self.assertFalse(
            permission.has_object_permission(
                response.wsgi_request, None, self.user_pokemon
            )
        )
