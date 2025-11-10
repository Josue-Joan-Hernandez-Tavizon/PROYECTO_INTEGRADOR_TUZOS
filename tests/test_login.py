import sys
import os
# Agregar el directorio raíz del proyecto al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from src.controllers.auth_controller import validar_credenciales
from unittest.mock import patch

def test_login_exitoso():
    """Prueba de login con credenciales correctas (Simulado)"""
    with patch('src.controllers.auth_controller.Database') as MockDB:
        # Configurar mock para devolver un usuario
        mock_instance = MockDB.return_value
        mock_instance.fetch_all.return_value = [('1', 'admin', '123')]
        
        assert validar_credenciales("admin", "123") == True

def test_login_fallido():
    """Prueba de login con credenciales incorrectas (Simulado)"""
    with patch('src.controllers.auth_controller.Database') as MockDB:
        # Configurar mock para devolver lista vacía
        mock_instance = MockDB.return_value
        mock_instance.fetch_all.return_value = []
        
        assert validar_credenciales("admin", "456") == False

def test_usuario_inexistente():
    """Prueba con usuario que no existe"""
    with patch('src.controllers.auth_controller.Database') as MockDB:
        mock_instance = MockDB.return_value
        mock_instance.fetch_all.return_value = []
        
        assert validar_credenciales("usuario_inexistente", "123") == False