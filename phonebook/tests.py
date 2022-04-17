from django.http import response
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

# Create your tests here.
class IndexTestCase(TestCase):
    """
    test  index view
    """

    def setUp(self):
        return super().setUp()

    def test_login_require(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.url)
        response = self.client.get(reverse("index"), follow=True)
        self.assertContains(response, "Login")

    def test_create_form(self):
        user = get_user_model().objects.create(username="testuser")
        self.client.force_login(user=user)
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "First name")
        self.client.logout()


class CreatProfileViewTestCase(TestCase):
    """
    test  index view
    """

    def setUp(self):
        return super().setUp()

    def test_login_require(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.url)
        response = self.client.get(reverse("index"), follow=True)
        self.assertContains(response, "Login")

    def test_tru_stause(self):
        user = get_user_model().objects.create(username="testuser")
        self.client.force_login(user)
        response = self.client.post(
            reverse("create_profile"),
            data={"first_name": "hamzeh", "last_name": "mahmoudi", "phone_number": "09165572957"},
        )
        self.assertEqual(response.status_code, 201)


class SearchViewTestCase(TestCase):
    """
    test  index view
    """

    def setUp(self):
        return super().setUp()

    def test_login_require(self):
        response = self.client.get(reverse("search"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.url)
        response = self.client.get(reverse("search"), follow=True)
        self.assertContains(response, "Login")

    def test_search_form(self):
        user = get_user_model().objects.create(username="testuser")
        self.client.force_login(user=user)
        response = self.client.get(reverse("search"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "phone number")
        self.client.logout()


class EditTestCase(TestCase):
    """
    test  edit view
    """

    def setUp(self):
        return super().setUp()

    def test_login_require(self):
        response = self.client.get(reverse("editprofile", args=[2]))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.url)
        response = self.client.get(reverse("editprofile", args=[1]), follow=True)
        self.assertContains(response, "Login")


class FindViewTestCase(TestCase):
    """
    test find view
    """

    def setUp(self):
        return super().setUp()

    def test_login_require(self):
        response = self.client.get(reverse("find"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.url)
        response = self.client.get(reverse("find"), follow=True)
        self.assertContains(response, "Login")
