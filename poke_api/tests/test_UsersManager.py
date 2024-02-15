from django.test import TestCase
from django.contrib.auth import get_user_model


class UsersManagerTest(TestCase):
    def test_create_user(self):
        # Get the user model and create user
        User = get_user_model()
        user = User.objects.create_user(
            email="test@user.com", password="foo", username="test"
        )

        # Assert that user attributes are set correctly
        self.assertEqual(user.email, "test@user.com")
        self.assertEqual(user.username, "test")
        self.assertTrue(user.check_password("foo"))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertEqual(str(user), user.email)

        # Test that creating a user with no email raises a ValueError
        with self.assertRaises(ValueError):
            User.objects.create_user(email=None, password="foo", username="test")

    def test_create_superuser(self):
        # Get the user model and create superuser
        User = get_user_model()
        user = User.objects.create_superuser(
            email="superuser@test.com", username="superuser", password="foo"
        )

        # Assert that user attributes are set correctly
        self.assertEqual(user.email, "superuser@test.com")
        self.assertEqual(user.username, "superuser")
        self.assertTrue(user.check_password("foo"))
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

        # Test that creating a superuser with no email raises a ValueError
        with self.assertRaises(ValueError):
            User.objects.create_user(email=None, password="foo", username="test")
