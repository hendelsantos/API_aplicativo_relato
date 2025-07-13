"""
Testes básicos para verificar se as APIs estão funcionando
Execute com: python manage.py test
"""

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from authentication.models import User
from parts.models import PartCategory, Part
from locations.models import Location


class AuthenticationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            employee_id='TEST001',
            shift='morning'
        )
    
    def test_login(self):
        """Testa login JWT"""
        response = self.client.post('/api/auth/login/', {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
    
    def test_profile(self):
        """Testa acesso ao perfil"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/auth/profile/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')


class PartsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            employee_id='TEST001',
            shift='morning'
        )
        self.client.force_authenticate(user=self.user)
        
        self.category = PartCategory.objects.create(
            name='Teste',
            description='Categoria de teste'
        )
        
        self.part = Part.objects.create(
            code='TEST001',
            name='Peça de Teste',
            category=self.category,
            minimum_stock=10,
            current_stock=20
        )
    
    def test_list_parts(self):
        """Testa listagem de peças"""
        response = self.client.get('/api/parts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_scan_qr_code(self):
        """Testa escaneamento de QR code"""
        response = self.client.post('/api/parts/scan-qr/', {
            'qr_data': f'PART:{self.part.code}:{self.part.name}'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['part']['code'], 'TEST001')


class LocationsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            employee_id='TEST001',
            shift='morning'
        )
        self.client.force_authenticate(user=self.user)
        
        self.location = Location.objects.create(
            name='Local de Teste',
            code='LOC001',
            location_type='plant'
        )
    
    def test_list_locations(self):
        """Testa listagem de locais"""
        response = self.client.get('/api/locations/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_location_tree(self):
        """Testa árvore de locais"""
        response = self.client.get('/api/locations/tree/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['tree']), 1)


print("Execute os testes com: python manage.py test")
