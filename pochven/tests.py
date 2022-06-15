from django.contrib.auth.models import User
from django.test import TestCase

# Create your tests here.


class RegistrationTestCase(TestCase):

    def test__registration_success(self):

        data = {
            "username": "rsanchez",
            "email": "rsanchez@example.com",
            "password1": "SomeSecurePassword123",
            "password2": "SomeSecurePassword123",
        }

        response = self.client.post('/accounts/register/', data=data)


        try:
            user = User.objects.get(username="rsanchez")
        except User.DoesNotExist:
            self.fail("User should exist")

        self.assertEqual(user.email, "rsanchez@example.com")
        self.assertTrue(user.check_password("SomeSecurePassword123"))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/')
