import sys
import os
# Agregar el directorio raíz del proyecto al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from unittest.mock import patch, MagicMock
from src.controllers.auth_controller import validar_credenciales

class TestAuthController(unittest.TestCase):
    @patch('src.controllers.auth_controller.Database')
    def test_validar_credenciales_exito(self, MockDatabase):
        """Prueba de validación con credenciales correctas"""
        # Configurar mock
        mock_db_instance = MockDatabase.return_value
        # Simular búsqueda de usuario
        mock_db_instance.fetch_all.return_value = [('id', 'admin', 'password')]
        
        # Ejecutar
        resultado = validar_credenciales('admin', 'password')
        
        # Verificar
        self.assertTrue(resultado)
        mock_db_instance.fetch_all.assert_called_once()

    @patch('src.controllers.auth_controller.Database')
    def test_validar_credenciales_fallo(self, MockDatabase):
        """Prueba de validación con credenciales incorrectas"""
        # Configurar mock
        mock_db_instance = MockDatabase.return_value
        # Simular usuario no encontrado
        mock_db_instance.fetch_all.return_value = []
        
        # Ejecutar
        resultado = validar_credenciales('admin', 'wrong_pass')
        
        # Verificar
        self.assertFalse(resultado)

    @patch('src.controllers.auth_controller.Database')
    def test_validar_credenciales_error(self, MockDatabase):
        """Prueba de validación cuando ocurre un error de base de datos"""
        # Configurar mock para lanzar excepción
        mock_db_instance = MockDatabase.return_value
        mock_db_instance.fetch_all.side_effect = Exception("DB Error")
        
        # Ejecutar
        resultado = validar_credenciales('admin', 'pass')
        
        # Verificar
        self.assertFalse(resultado)
