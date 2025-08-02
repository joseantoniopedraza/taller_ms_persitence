from django.test import TestCase
from django.urls import reverse
from django.http import JsonResponse
from .models import Tenders
import json


class TendersListViewTest(TestCase):
    def setUp(self):
        Tenders.objects.create(
            title="Licitación 1",
            description="Primera licitación de prueba",
            code="LIC001"
        )
        Tenders.objects.create(
            title="Licitación 2",
            description="Segunda licitación de prueba",
            code="LIC002"
        )

    def test_tenders_list_returns_all(self):
        response = self.client.get("/tenders/")  # Ajusta si usas otra ruta
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['code'], "LIC001")
        self.assertEqual(data[1]['code'], "LIC002")


class CreateTenderViewTest(TestCase):
    def test_create_tender_success(self):
        payload = {
            "title": "Nueva Licitación",
            "description": "Licitación de prueba",
            "code": "LIC100"
        }

        response = self.client.post(
            "/tenders/create/",  # Ajusta la URL si es diferente
            data=json.dumps(payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 201)
        self.assertTrue(Tenders.objects.filter(code="LIC100").exists())

    def test_create_tender_missing_fields(self):
        payload = {
            "title": "Sin descripción ni código"
        }

        response = self.client.post(
            "/tenders/create/",
            data=json.dumps(payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("Todos los campos son obligatorios", response.json()['error'])

    def test_create_tender_duplicate_code(self):
        Tenders.objects.create(
            title="Existente",
            description="Ya existe",
            code="LIC999"
        )

        payload = {
            "title": "Duplicada",
            "description": "Intento duplicado",
            "code": "LIC999"
        }

        response = self.client.post(
            "/tenders/create/",
            data=json.dumps(payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 409)
        self.assertIn("Ya existe una licitación con ese código", response.json()['error'])

    def test_create_tender_invalid_json(self):
        response = self.client.post(
            "/tenders/create/",
            data="esto no es json válido",
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("Formato JSON inválido", response.json()['error'])

    def test_create_tender_wrong_method(self):
        response = self.client.get("/tenders/create/")
        self.assertEqual(response.status_code, 405)
        self.assertIn("Método no permitido", response.json()['error'])
