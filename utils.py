from django.urls import reverse
from rest_framework.test import APIClient


def authenticate_jwt_client_creds(username, password):
    client = APIClient()
    data = {"username": username, "password": password}
    token_res = client.post(reverse("token_obtain_pair"), data, format="json")
    token = token_res.data.get("access")
    client.credentials(HTTP_AUTHORIZATION="Bearer " + str(token))

    return client