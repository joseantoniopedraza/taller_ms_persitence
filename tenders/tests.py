from django.test import TestCase
from .models import Tenders
from .views import create_tender
import json


class TendersListViewTest(TestCase):
    def setUp(self):
        Tenders.objects.create(
            title="Licitación 1",
            description="Primera licitación de prueba",
            code="LIC001"
        )

    def test_tenders_list_returns_all(self):
        response = self.client.get("/tenders/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['code'], "LIC001")


class CreateTenderFunctionTest(TestCase):
    def test_create_tender_success(self):
        payload = {
            "payload": {
                "title": "Nueva Licitación",
                "description": "Descripción de prueba",
                "code": "LIC123"
            }
        }

        json_data = json.dumps(payload)
        response = create_tender(json_data)

        self.assertEqual(response.status_code, 201)
        self.assertTrue(Tenders.objects.filter(code="LIC123").exists())

    def test_create_tender_missing_fields(self):
        payload = {
            "payload": {
                "title": "Sin código"
                # Falta description y code
            }
        }

        json_data = json.dumps(payload)
        response = create_tender(json_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Todos los campos son obligatorios", json.loads(response.content)['error'])

    def test_create_tender_duplicate_code(self):
        Tenders.objects.create(
            title="Existente",
            description="Ya existe",
            code="LIC999"
        )

        payload = {
            "payload": {
                "title": "Duplicada",
                "description": "Intento duplicado",
                "code": "LIC999"
            }
        }

        json_data = json.dumps(payload)
        response = create_tender(json_data)
        self.assertEqual(response.status_code, 409)
        self.assertIn("Ya existe una licitación con ese código", json.loads(response.content)['error'])

    def test_create_tender_invalid_json(self):
        invalid_json = "esto no es json"
        response = create_tender(invalid_json)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Formato JSON inválido", json.loads(response.content)['error'])
