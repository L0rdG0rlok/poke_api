from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIRequestFactory, APIClient
from poke_api.models import Pokemon
from poke_api.serializers import PokemonSerializer
from rest_framework import status


class PokemonSerializerTestCase(TestCase):
    def setUp(self):
        # Create a user for testing
        User = get_user_model()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword", email="test@test.com"
        )

        # Create an APIRequestFactory instance
        self.factory = APIRequestFactory()

        # Create a dummy request
        self.request = self.factory.post("api/Pokemon/")
        self.request.user = self.user

        # Create a PokemonSerializer instance
        self.serializer = PokemonSerializer(context={"request": self.request})

        # Validated data for creating a Pokemon
        self.validated_data = {
            "name": "Pikachu",
            "height": 30,
            "weight": 40,
            "sprite": "pikachu.png",
            "type": "Electric",
        }

    def test_create_method_assigns_owner(self):
        """Test if create method assigns the owner to the user making the request"""
        pokemon_instance = self.serializer.create(self.validated_data)

        # Check if the owner is assigned correctly
        self.assertEqual(pokemon_instance.owner, self.user)

    def test_create_method_creates_pokemon(self):
        """Test if create method creates a Pokemon instance"""
        initial_pokemon_count = Pokemon.objects.count()

        # Call the create method
        self.serializer.create(self.validated_data)

        # Check if a Pokemon instance is created
        self.assertEqual(Pokemon.objects.count(), initial_pokemon_count + 1)

    def test_create_method_with_invalid_data(self):
        """Test create method with invalid data"""
        # Remove the 'name' field to make the data invalid
        invalid_data = self.validated_data.copy()
        del invalid_data["name"]

        # Use the Django REST framework's test client to simulate a request
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.post("/api/Pokemon/", data=invalid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_validate_method_rejects_more_than_five_pokemon(self):
        """Test validate method rejects more than five Pokemon for a user"""
        # Create 5 Pokemon for the user
        for i in range(5):
            Pokemon.objects.create(
                name=f"Pokemon{i}",
                height=30,
                weight=40,
                sprite="pokemon.png",
                type="Normal",
                owner=self.user,
            )

        # Try to create one more Pokemon
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.post("/api/Pokemon/", data=self.validated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_validate_method_allows_five_or_fewer_pokemon(self):
        """Test validate method allows creation if the user has five or fewer Pokemon"""
        # Create 4 Pokemon for the user
        for i in range(4):
            Pokemon.objects.create(
                name=f"Pokemon{i}",
                height=30,
                weight=40,
                sprite="pokemon.png",
                type="Normal",
                owner=self.user,
            )

        # Try to create one more Pokemon
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.post("/api/Pokemon/", data=self.validated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
