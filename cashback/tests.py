import json
from django.test import TestCase
from rest_framework import status


class TestCreateCashback(TestCase):

    def setUp(self):
        self.base_url = "/api/cashbacks/"

    def test_create_cashback_201(self):
        payload = {
            "customer": {
                "name": "Nome",
                "document": "12345678912"
            },
            "products": [
                {
                    "type": "Tipo 1",
                    "value": 50,
                    "qty": 1
                },
                {
                    "type": "Tipo 2",
                    "value": 25,
                    "qty": 2
                }
            ],
            "sold_at": "2021-09-19 21:12:31",
            "total": 100
        }

        expected_result = {
            "id": 1,
            "customer": {
                "id": 1,
                "name": "Nome",
                "document": "12345678912"
            },
            "products": [
                {
                    "id": 1,
                    "type": "Tipo 1",
                    "value": 50.0,
                    "qty": 1
                },
                {
                    "id": 2,
                    "type": "Tipo 2",
                    "value": 25.0,
                    "qty": 2
                }
            ],
            "sold_at": "2021-09-19T21:12:31Z",
            "total": 100
        }

        response = self.client.post(self.base_url, payload, content_type='application/json')
        self.assertEqual(json.loads(response.content), expected_result)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_cashback_empty_products_list_400(self):
        payload = {
            "customer": {
                "name": "Nome",
                "document": "12345678912"
            },
            "products": [

            ],
            "sold_at": "2021-09-19 21:12:31",
            "total": 100
            }

        expected_result = {'products': ['This field must not be an empty list.']}

        response = self.client.post(self.base_url, payload, content_type='application/json')
        self.assertEqual(json.loads(response.content), expected_result)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_create_cashback_missing_data_400(self):
        payload = {

        }

        expected_result = {'customer': ['This field is required.'], 'products': ['This field is required.'],
                           'sold_at': ['This field is required.'], 'total': ['This field is required.']}

        response = self.client.post(self.base_url, payload, content_type='application/json')
        self.assertEqual(json.loads(response.content), expected_result)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_cashback_incorrect_total_sum_400(self):
        payload = {
            "customer": {
                "name": "Nome",
                "document": "12345678912"
            },
            "products": [
                {
                    "type": "Tipo 1",
                    "value": 50,
                    "qty": 1
                },
                {
                    "type": "Tipo 2",
                    "value": 25,
                    "qty": 1
                }
            ],
            "sold_at": "2021-09-19 21:12:31",
            "total": 100
        }

        expected_result = {'non_field_errors': ['Inconsistent value sum.']}

        response = self.client.post(self.base_url, payload, content_type='application/json')
        self.assertEqual(json.loads(response.content), expected_result)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_cashback_negative_values(self):
        payload = {
            "customer": {
                "name": "Nome",
                "document": "12345678912"
            },
            "products": [
                {
                    "type": "Tipo 1",
                    "value": 50,
                    "qty": 1
                },
                {
                    "type": "Tipo 2",
                    "value": 25,
                    "qty": 1
                }
            ],
            "sold_at": "2021-09-19 21:12:31",
            "total": -1
        }

        expected_result = {'total': ['This field must not be a negative sum.']}

        response = self.client.post(self.base_url, payload, content_type='application/json')
        self.assertEqual(json.loads(response.content), expected_result)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
