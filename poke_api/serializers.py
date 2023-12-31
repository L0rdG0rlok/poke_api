from rest_framework import serializers
from poke_api import models


class PokemonSerializer(serializers.ModelSerializer):
    """Serializes a Pokemon object"""

    class Meta:
        model = models.Pokemon
        fields = "__all__"
        read_only_fields = [
            "owner",
        ]

    def create(self, validated_data):
        """Assign the owner to the user making the request"""
        validated_data["owner"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        user = self.context["request"].user
        pokemon_count = user.pokemon.count()
        if pokemon_count >= 5:
            raise serializers.ValidationError(
                {"error": "Users can have a maximum of 5 Pokemon"}
            )

        return data


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializes a user profile object"""

    class Meta:
        model = models.UserProfile
        fields = ["id", "email", "username", "pokemon", "password"]
        pokemon = PokemonSerializer(many=True, read_only=True)
        depth = 1
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        """Create and return new user"""
        user = models.UserProfile.objects.create_user(**validated_data)

        return user

    def update(self, instance, validated_data):
        """Handle updating user account"""
        if "password" in validated_data:
            password = validated_data.pop("password")
            instance.set_password(password)

        return super().update(instance, validated_data)
