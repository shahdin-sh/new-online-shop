from django.test import TestCase
from django.urls import reverse, resolve
from ..views import cart_detail_view

# resolve ----> The resolve() function can be used for resolving URL paths to the corresponding view functions. 
# It has the following signature: resolve (path, urlconf=None) path is the URL path you want to resolve.


class TestProductUrls(TestCase):

    def test_cart_detail_view_is_resolved(self):
        url = reverse('cart:cart_detail_view')
        self.assertEqual(resolve(url).func, cart_detail_view)

    