
from django.test import TestCase
from django.urls import reverse
from core.models import Url
from core.forms import UrlForm, PinForm

# Create your tests here
class UrlFormTestCase(TestCase):
    def test_valid_form(self):
        form_data = {
            "url": "https://www.example.com",
            "hashed_url": "xEBop_6suJ",
        }
        form = UrlForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

# test-case : invaid hashed Url
    def test_invalid_hashedUrl(self):
        form_data = {
            "url": "",
            "hashed_url": "custom-hash",
        }
        form = UrlForm(data=form_data)
        self.assertFalse(form.is_valid())

# test-case : invalid form
    def test_invalid_form(self):
        form_data = {
            "url": "",
            "hashed_url": "xEBop_6suJ",
        }
        form = UrlForm(data=form_data)
        self.assertFalse(form.is_valid())

class PinFormTestCase(TestCase):
    def test_valid_form(self):
        form_data = {
            "pin": "123456",
        }
        form = PinForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form_data = {
            "pin": "",
        }
        form = PinForm(data=form_data)
        self.assertFalse(form.is_valid())

class HomeViewTestCase(TestCase):
    def test_get_request(self):
        response = self.client.get(reverse("home_page"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")
    
    def test_post_request_invalid_form(self):
        form_data = {
            "url": "",
            "hashed_url": "custom-hash",
        }
        response = self.client.post(reverse("home_page"), data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")
        self.assertFormError(response, "form", "url", "This field is required.")

    # def test_post_request_valid_form(self):
    #     form_data = {
    #         "url": "https://www.example.com",
    #         "hashed_url": "custom-hash",
    #     }
    #     response = self.client.post(reverse("home_page"), data=form_data)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, "home.html")

    #     obj = Url.objects.get(url="https://www.example.com", hashed_url="custom-hash")
    #     self.assertEqual(response.context["short_url"], obj.get_full_short_url())


class RedirectViewTestCase(TestCase):
    def setUp(self):
        self.url = Url.objects.create(url="https://www.example.com", hashed_url="xEBop_6suJ")

    # def test_valid_hashed_url(self):
    #     response = self.client.get(reverse("redirect_url", args=[self.url.hashed_url]))
    #     self.assertRedirects(response, self.url.url, status_code=302, target_status_code=200)

    def test_invalid_hashed_url(self):
        response = self.client.get(reverse("redirect_url", args=["invalid-hash"]))
        self.assertEqual(response.status_code, 404)


class RetrieveViewTestCase(TestCase):
    def test_get_request(self):
        response = self.client.get(reverse("retrieve_url"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "retrieve.html")

    def test_post_request_valid_form(self):
        url = Url.objects.create(url="https://www.example.com", hashed_url="xEBop_6suJ")
        form_data = {
            "pin": url.pin,
        }
        response = self.client.post(reverse("retrieve_url"), data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "retrieve.html")
        self.assertEqual(response.context["url"], url)

    def test_post_request_invalid_form(self):
        form_data = {
            "pin": "123456",
        }
        response = self.client.post(reverse("retrieve_url"), data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "retrieve.html")
        self.assertFormError(response, "form", "pin", "Invalid PIN")

class URLListViewTestCase(TestCase):
    def test_get_request(self):
        response = self.client.get(reverse("url_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "url_list.html")
        

class EditViewTestCase(TestCase):
    def setUp(self):
        self.url = Url.objects.create(url="https://www.example.com", hashed_url="xEBop_6suJ")

    def test_get_request(self):
        response = self.client.get(reverse("edit_url", args=[self.url.hashed_url]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "edit.html")
        self.assertContains(response, self.url.url)

    def test_post_request_valid_form(self):
        form_data = {
            "url": "https://www.updated-example.com",
        }
        response = self.client.post(reverse("edit_url", args=[self.url.hashed_url]), data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("home_page"))

        updated_url = Url.objects.get(pk=self.url.pk)
        self.assertEqual(updated_url.url, "https://www.updated-example.com")

    def test_post_request_invalid_form(self):
        form_data = {
            "url": "",
        }
        response = self.client.post(reverse("edit_url", args=[self.url.hashed_url]), data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "edit.html")
        self.assertFormError(response, "form", "url", "This field is required.")

