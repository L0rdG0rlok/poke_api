from django.test import TestCase
from poke_api.models import UserProfile
from poke_api.serializers import UserProfileSerializer


class UserProfileSerializerTests(TestCase):
    def test_create_user_profile(self):
        data = {
            "email": "test@example.com",
            "username": "testuser",
            "password": "testpassword",
        }
        serializer = UserProfileSerializer(data=data)

        self.assertTrue(serializer.is_valid())
        user_profile = serializer.save()

        self.assertIsInstance(user_profile, UserProfile)
        self.assertEqual(user_profile.email, data["email"])
        self.assertEqual(user_profile.username, data["username"])
        self.assertTrue(user_profile.check_password(data["password"]))

    def test_update_user_profile(self):
        existing_user = UserProfile.objects.create_user(
            email="existing@example.com",
            username="existinguser",
            password="existingpassword",
        )
        data = {
            "email": "updated@example.com",
            "username": "updateduser",
            "password": "updatedpassword",
        }
        serializer = UserProfileSerializer(existing_user, data=data, partial=True)

        self.assertTrue(serializer.is_valid())
        updated_user_profile = serializer.save()

        self.assertEqual(updated_user_profile.email, data["email"])
        self.assertEqual(updated_user_profile.username, data["username"])
        self.assertTrue(updated_user_profile.check_password(data["password"]))

    def test_update_user_profile_without_password(self):
        existing_user = UserProfile.objects.create_user(
            email="existing@example.com",
            username="existinguser",
            password="existingpassword",
        )
        data = {"email": "updated@example.com", "username": "updateduser"}
        serializer = UserProfileSerializer(existing_user, data=data, partial=True)

        self.assertTrue(serializer.is_valid())
        updated_user_profile = serializer.save()

        self.assertEqual(updated_user_profile.email, data["email"])
        self.assertEqual(updated_user_profile.username, data["username"])
        self.assertTrue(updated_user_profile.check_password("existingpassword"))
