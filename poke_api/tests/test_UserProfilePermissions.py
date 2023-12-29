from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory
from poke_api.permissions import UpdateOwnProfile


class UpdateOwnProfilePermissionsTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            email="testuser@test.com", username="test_user", password="foo"
        )
        self.other_user = User.objects.create_user(
            email="testuser2@test.com", username="test_user2", password="foo"
        )

        self.permission = UpdateOwnProfile()
        self.factory = APIRequestFactory()

    def test_safe_methods_allowd(self):
        request = self.factory.get("api/profile/")
        request.user = self.user
        self.assertTrue(self.permission.has_object_permission(request, None, None))

    def test_edit_own_profile_allowed(self):
        # Test that user can edit their own profile
        request = self.factory.put("/api/user-profile/")
        request.user = self.user
        self.assertTrue(self.permission.has_object_permission(request, None, self.user))

    def test_edit_other_profile_not_allowed(self):
        # Test that user cannot edit another user's profile
        request = self.factory.put("/api/user-profile/")
        request.user = self.user
        self.assertFalse(
            self.permission.has_object_permission(request, None, self.other_user)
        )

    def test_unauthenticated_user_not_allowed(self):
        # Test that non-safe methods (PUT, POST, DELETE) require authentication
        request = self.factory.put("/api/user-profile/")
        request.user = None  # Unauthenticated user
        with self.assertRaises(AttributeError):
            self.permission.has_object_permission(request, None, None)
