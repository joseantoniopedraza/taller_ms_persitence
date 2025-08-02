from django.test import TestCase
from django.urls import reverse
from .models import Clients, Interests, Clients_Interests
import json


class ClientsListViewTest(TestCase):
    def setUp(self):
        # Crear cliente y su interés
        self.client_obj = Clients.objects.create(name="Juan", email="juan@example.com")
        self.interest = Interests.objects.create(name="Programación")
        Clients_Interests.objects.create(client=self.client_obj, interest=self.interest)

    def test_clients_list_returns_data(self):
        response = self.client.get("/clients/")  # Asegúrate de que esta URL esté en tu urls.py
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], "Juan")
        self.assertIn("Programación", data[0]['interests'])


class InterestsListViewTest(TestCase):
    def setUp(self):
        Interests.objects.create(name="Django")
        Interests.objects.create(name="Python")

    def test_interests_list_returns_all(self):
        response = self.client.get("/clients/interests/")  # Asegúrate de que esta URL esté en tu urls.py
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['name'], "Django")


class CreateClientWithInterestsTest(TestCase):
    def test_create_client_success(self):
        payload = {
            "name": "Ana",
            "email": "ana@example.com",
            "interests": ["IA", "Ciencia de Datos"]
        }

        response = self.client.post(
            "/clients/create/",  # Asegúrate de que esta URL esté en tu urls.py
            data=json.dumps(payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 201)
        self.assertTrue(Clients.objects.filter(name="Ana").exists())
        ana = Clients.objects.get(name="Ana")
        self.assertEqual(ana.clients_interests_set.count(), 2)

    def test_create_client_missing_fields(self):
        payload = {
            "email": "sin_nombre@example.com"
        }

        response = self.client.post(
            "/clients/create/",
            data=json.dumps(payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("Faltan campos obligatorios", response.json()['error'])

    def test_create_client_invalid_json(self):
        response = self.client.post(
            "/clients/create/",
            data="esto no es json",
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("Formato JSON inválido", response.json()['error'])
