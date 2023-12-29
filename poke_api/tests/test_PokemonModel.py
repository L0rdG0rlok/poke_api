from django.test import TestCase
from poke_api.models import Pokemon, UserProfile


class PokemonModelTest(TestCase):
    """Tests Pokemon Model"""
    def setUp(self):
        # Create a Pokemon instance for testing
        self.user = UserProfile.objects.create()
        self.pokemon = Pokemon.objects.create(
            name='Pikachu',
            height=30,
            weight=40,
            sprite='pikachu.png',
            type='Electric',
            owner=self.user
        )

    def test_pokemon_str_method(self):
        """Test the __str__ method of Pokemon model"""
        self.assertEqual(str(self.pokemon), 'Pikachu')
