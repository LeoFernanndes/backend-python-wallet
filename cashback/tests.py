import datetime
import json
from django.core.management import call_command
from django.test import TestCase
from rest_framework import status

from utils import authenticate_jwt_client_creds


class TestCreateCashback(TestCase):
    @classmethod
    def setUpClass(cls):
        call_command("loaddata", "product_types")
        call_command("loaddata", "customers")
        call_command("loaddata", "users")
        pass

    def setUp(self):
        self.base_url = "/api/cashbacks/"


    def test_create_cashback_201(self):
        payload = {
            "customer": {
                "name": "Fulano",
                "document": "79336512404"
            },
            "products": [
                {
                    "type": "A",
                    "value": 50,
                    "qty": 1
                },
                {
                    "type": "B",
                    "value": 25,
                    "qty": 2
                }
            ],
            "sold_at": "2021-09-19 21:12:31",
            "total": 100
        }

        expected_result = {
            'id': 1,
            'customer': {
                'id': 1,
                'name': 'Fulano',
                'document': '79336512404'
            },
            'products': [
                {'id': 1, 'type': 'A', 'value': 50.0, 'qty': 1},
                {'id': 2, 'type': 'B', 'value': 25.0, 'qty': 2}
            ],
            'sold_at': '2021-09-19T21:12:31Z',
            'total': 100.0,
            # 'created_at': '2021-09-25T13:28:23.672Z',
            'message': 'Cashback criado com sucesso!',
            # 'returned_id': 13,
            'cashback': 3.0,
            'document': "79336512404"
        }

        client = authenticate_jwt_client_creds("user", "password")
        response = client.post(self.base_url, payload, format="json")
        response_content = json.loads(response.content)
        response_content.pop('returned_id')
        response_content.pop('created_at')
        self.assertEqual(response_content, expected_result)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_cashback_inconsistent_customer_400(self):
        payload = {
            "customer": {
                "name": "Inconsistent Name",
                "document": "79336512404"
            },
            "products": [
                {
                    "type": "A",
                    "value": 50,
                    "qty": 1
                },
                {
                    "type": "B",
                    "value": 25,
                    "qty": 2
                }
            ],
            "sold_at": "2021-09-19 21:12:31",
            "total": 100
        }

        expected_result = {'non_field_errors': ['Customer data does not match document.']}

        client = authenticate_jwt_client_creds("user", "password")
        response = client.post(self.base_url, payload, format="json")
        response_content = json.loads(response.content)
        self.assertEqual(response_content, expected_result)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_cashback_invalid_document_400(self):
        payload = {
            "customer": {
                "name": "Nome",
                "document": "79336512404"
            },
            "products": [
                {
                    "type": "A",
                    "value": 50,
                    "qty": 1
                },
                {
                    "type": "B",
                    "value": 25,
                    "qty": 2
                }
            ],
            "sold_at": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=1),
            "total": 100
        }

        expected_result = {'sold_at': ['This field must not represent a future datetime.']}

        client = authenticate_jwt_client_creds("user", "password")
        response = client.post(self.base_url, payload, format="json")
        response_content = json.loads(response.content)
        self.assertEqual(response_content, expected_result)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_cashback_future_sale_date_400(self):
        payload = {
            "customer": {
                "name": "Nome",
                "document": "12345678912"
            },
            "products": [
                {
                    "type": "A",
                    "value": 50,
                    "qty": 1
                },
                {
                    "type": "B",
                    "value": 25,
                    "qty": 2
                }
            ],
            "sold_at": "2021-09-19 21:12:31",
            "total": 100
        }

        expected_result = {'customer': {'document': ['Invalid document.']}}

        client = authenticate_jwt_client_creds("user", "password")
        response = client.post(self.base_url, payload, format="json")
        response_content = json.loads(response.content)
        self.assertEqual(response_content, expected_result)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_create_cashback_empty_products_list_400(self):
        payload = {
            "customer": {
                "name": "Nome",
                "document": "79336512404"
            },
            "products": [

            ],
            "sold_at": "2021-09-19 21:12:31",
            "total": 100
            }

        expected_result = {'products': ['This field must not be an empty list.']}

        client = authenticate_jwt_client_creds("user", "password")
        response = client.post(self.base_url, payload, format="json")
        self.assertEqual(json.loads(response.content), expected_result)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_create_cashback_missing_data_400(self):
        payload = {

        }

        expected_result = {'customer': ['This field is required.'], 'products': ['This field is required.'],
                           'sold_at': ['This field is required.'], 'total': ['This field is required.']}

        client = authenticate_jwt_client_creds("user", "password")
        response = client.post(self.base_url, payload, format="json")
        self.assertEqual(json.loads(response.content), expected_result)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_create_cashback_incorrect_total_sum_400(self):
        payload = {
            "customer": {
                "name": "Nome",
                "document": "79336512404"
            },
            "products": [
                {
                    "type": "A",
                    "value": 50,
                    "qty": 1
                },
                {
                    "type": "B",
                    "value": 25,
                    "qty": 1
                }
            ],
            "sold_at": "2021-09-19 21:12:31",
            "total": 100
        }

        expected_result = {'non_field_errors': ['Inconsistent value sum.']}

        client = authenticate_jwt_client_creds("user", "password")
        response = client.post(self.base_url, payload, format="json")
        self.assertEqual(json.loads(response.content), expected_result)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_create_cashback_negative_values(self):
        payload = {
            "customer": {
                "name": "Nome",
                "document": "79336512404"
            },
            "products": [
                {
                    "type": "A",
                    "value": 50,
                    "qty": 1
                },
                {
                    "type": "B",
                    "value": 25,
                    "qty": 1
                }
            ],
            "sold_at": "2021-09-19 21:12:31",
            "total": -1
        }

        expected_result = {'total': ['This field must not be a negative sum.']}

        client = authenticate_jwt_client_creds("user", "password")
        response = client.post(self.base_url, payload, format="json")
        self.assertEqual(json.loads(response.content), expected_result)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @classmethod
    def tearDownClass(cls):
        pass
