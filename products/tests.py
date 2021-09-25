import json

from django.core.management import call_command
from django.test import TestCase
from rest_framework import status


class TestCreateProductType(TestCase):

    def setUp(self):
        self.base_url = "/api/product-types/"

    def test_create_product_type_201(self):
        payload = {
            "type": "Z",
            "cashback_percent": 0.05
        }

        expected_result = {
            'id': 5,
            'cashback_percent': 0.05,
            'type': 'Z'
        }

        response = self.client.post(self.base_url, payload, content_type='application/json')
        self.assertEqual(json.loads(response.content), expected_result)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_create_product_type_negative_cashback_400(self):
        payload = {
            "type": "Z",
            "cashback_percent": -0.05
        }

        expected_result = {
            'cashback_percent': ['This field must not be a negative value.']
        }

        response = self.client.post(self.base_url, payload, content_type='application/json')
        self.assertEqual(json.loads(response.content), expected_result)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestCreateProduct(TestCase):
    @classmethod
    def setUpClass(cls):
        call_command("loaddata", "product_types")
        pass

    def setUp(self):
        self.base_url = "/api/products/"

    def test_create_product_type_201(self):
        payload = {
            "type": "A",
            "qty": 1,
            'value': 10
        }

        expected_result = {
            "id": 1,
            "type": "A",
            "qty": 1,
            'value': 10
        }

        response = self.client.post(self.base_url, payload, content_type='application/json')
        self.assertEqual(json.loads(response.content), expected_result)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_product_unexistent_type_400(self):
        payload = {
                "type": "Z",
                "qty": 1,
                'value': 10
            }

        expected_result = {
                'type': ['Type does not exist.']
            }

        response = self.client.post(self.base_url, payload, content_type='application/json')
        self.assertEqual(json.loads(response.content), expected_result)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @classmethod
    def tearDownClass(cls):
        pass
