from django.test import TestCase
from django.urls import reverse, resolve
from ..views import *

# resolve ----> The resolve() function can be used for resolving URL paths to the corresponding view functions. 
# It has the following signature: resolve (path, urlconf=None) path is the URL path you want to resolve.


class TestProductUrls(TestCase):

    def test_shop_categories_is_resolved(self):
        url = reverse('products:product_categories')
        self.assertEqual(resolve(url).func, shop_categories)

    def test_product_detail_view_is_resolved(self):
        url = reverse('products:product_detail', args=['random_product_for_slug'])
        self.assertEqual(resolve(url).func, product_detail_view)

    def test_add_to_wishlist_feature_is_resolved(self):
        url = reverse('products:add_to_wishlist', args=['random_product_for_slug'])
        self.assertEqual(resolve(url).func, add_to_wishlist)

    def test_removd_from_wishlist_feature_is_resolved(self):
        url = reverse('products:remove_from_wishlist', args=['random_product_for_slug'])
        self.assertEqual(resolve(url).func, remove_from_wishlist)
        
    def test_category_detail_view_is_resolved(self):
        url = reverse('products:category_detail', args=['random_slug_category'])
        self.assertEqual(resolve(url).func, products_or_category_detail)

    
    

    