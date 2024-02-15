from django.test import TestCase
from poke_api.models import Pokemon, UserProfile


class PokemonModelTest(TestCase):
    def setUp(self):
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
        self.assertEqual(str(self.pokemon), 'Pikachu')
