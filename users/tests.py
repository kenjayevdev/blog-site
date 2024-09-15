from django.contrib.auth.middleware import get_user
from django.urls import reverse

from users.models import CustomUser
from django.test import TestCase

class RegistrationTestCase(TestCase):
    def test_user_account_is_created(self):
        self.client.post(
            reverse("users:register"),
            data={"username": "jas",
                    "first_name": "jasurbek",
                    "last_name": "kenjayev",
                    "email": "jasur@gmail.com",
                    "password": "22121944"
            }
        )

        user = CustomUser.objects.get(username="jas")

        self.assertEquals(user.first_name, "jasurbek")
        self.assertEquals(user.last_name, "kenjayev")
        self.assertEquals(user.email, "jasur@gmail.com")
        self.assertNotEqual(user.password, "22121944")
        self.assertTrue(user.check_password("22121944"))

    def test_requered_fields(self):
        response = self.client.post(
            reverse("users:register"),
            data={
                "first_name": "jasurbek",
                "email": "jasur@gmail.com"
            }
        )

        user_count = CustomUser.objects.count()

        self.assertEqual(user_count, 0)
        self.assertFormError(response, "form", "username", "This field is required.")
        self.assertFormError(response, "form", "password", "This field is required.")

    def test_invalid_email(self):
        response = self.client.post(
            reverse("users:register"),
            data={"username": "jas",
                  "first_name": "jasurbek",
                  "last_name": "kenjayev",
                  "email": "jasur-email",
                  "password": "22121944"
            }
        )

        user_count = CustomUser.objects.count()

        self.assertEqual(user_count, 0)
        self.assertFormError(response, "form", "email", "Enter a valid email address.")

    def test_unique_username(self):
        user = CustomUser.objects.create(username="jas", first_name="jasurbek")
        user.set_password("22121944")
        user.save()

        response = self.client.post(
            reverse("users:register"),
            data={"username": "jas",
                  "first_name": "jasurbek",
                  "last_name": "kenjayev",
                  "email": "jasur@gmail.com",
                  "password": "22121944"
            }
        )

        user_count = CustomUser.objects.count()
        self.assertEqual(user_count, 1)
        self.assertFormError(response, "form", "username", "A user with that username already exists.")


class LoginTestCase(TestCase):
    def setUp(self):
        self.db_user = CustomUser.objects.create(username="jas", first_name="jasurbek")
        self.db_user.set_password("22121944")
        self.db_user.save()

    def test_successful_login(self):
        self.client.post(
            reverse("users:login"),
            data={
                "username": "jas",
                "password": "22121944"
            }
        )

        user = get_user(self.client)
        self.assertTrue(user.is_authenticated)

    def test_wrong_credentials(self):
        self.client.post(
            reverse("users:login"),
            data={
                "username": "jasurr",
                "password": "22121944"
            }
        )

        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

    def test_logout(self):
        self.client.login(username="jas", password="22121948")

        self.client.get(reverse("users:logout"))

        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

class ProfileTestCase(TestCase):
    def test_login_required(self):
        response = self.client.get(reverse("users:profile"))

        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, reverse("users:login") + "?next=/users/profile/")

    def test_profile_details(self):
        user = CustomUser.objects.create(
            username="wolf", first_name="jasur", last_name="kenjayev", email="wolf@gmail.com"
        )

        user.set_password("22121948")
        user.save()

        self.client.login(username="wolf", password="22121948")

        response = self.client.get(reverse("users:profile"))

        self.assertEquals(response.status_code, 200)
        self.assertContains(response, user.username)
        self.assertContains(response, user.first_name)
        self.assertContains(response, user.last_name)
        self.assertContains(response, user.email)

    def test_update_profile(self):
        user = CustomUser.objects.create(
            username="wolf", first_name="jasur", last_name="kenjayev", email="wolf@gmail.com"
        )

        user.set_password("22121948")
        user.save()

        self.client.login(username="wolf", password="22121948")

        response = self.client.post(
            reverse("users:profile-edit"),
            data={
                "username": "wolf",
                "first_name": "jasur",
                "last_name": "alendar",
                "email": "alendar@gmail.com"

            }
        )

        user = CustomUser.objects.get(pk=user.pk)

        self.assertEquals(user.last_name, "alendar")
        self.assertEquals(user.email, "alendar@gmail.com")
        self.assertEquals(response.url, reverse("users:profile"))