import json
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
