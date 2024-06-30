from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
import json
from .models import ProductModel

class CreateProductTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('create_product')
        self.valid_payload = {'name': 'Test Product', 'price': 100, 'retailer_name': 'Test Retailer'}
        self.invalid_payload = {'name': '', 'price': 100, 'retailer_name': 'Test Retailer'}

    def test_create_valid_product(self):
        response = self.client.post(
        self.url, data=json.dumps(self.valid_payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('msg', response.json())

    def test_create_invalid_product(self):
        response = self.client.post(
        self.url, data=json.dumps(self.invalid_payload),content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('msg', response.json())



from django.test import TestCase, Client

class SearchProductsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('search_product', kwargs={'name': 'Test'})
        ProductModel.objects.create(name='Test Product', price=100, retailer_name='Test Retailer')
        ProductModel.objects.create(name='Another Product', price=200, retailer_name='Another Retailer')

    def test_search_existing_product(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.json()), 0)

    def test_search_non_existing_product(self):
        url = reverse('search_product', kwargs={'name': 'NonExistent'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('msg', response.json())
