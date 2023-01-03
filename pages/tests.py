from django.test import TestCase
from django.urls import reverse, resolve
from .views import HomePageView


class TestPagesUrls(TestCase):
    def test_home_page_is_resolved(self):
        url = reverse('homepage')
        self.assertEqual(HomePageView.as_view().__name__, resolve(url).func.__name__)

