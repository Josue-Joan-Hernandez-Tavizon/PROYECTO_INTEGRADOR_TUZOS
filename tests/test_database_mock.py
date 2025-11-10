import sys
import os
# Agregar el directorio raíz del proyecto al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from unittest.mock import MagicMock, patch
from src.models.database import Database

class TestDatabase(unittest.TestCase):
    @patch('mysql.connector.connect')
    def test_connection_success(self, mock_connect):
        """Prueba de conexión exitosa a la base de datos"""
        # Configurar mock
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        
        # Ejecutar
        db = Database()
        
        # Verificar
        mock_connect.assert_called_once()
        self.assertIsNotNone(db.connection)


    @patch('mysql.connector.connect')
    def test_fetch_all(self, mock_connect):
        """Prueba del método fetch_all"""
        # Configurar mock
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        # Simular datos de retorno
        expected_data = [('user1',), ('user2',)]
        mock_cursor.fetchall.return_value = expected_data
        
        # Ejecutar
        db = Database()
        result = db.fetch_all("SELECT * FROM users")
        
        # Verificar
        self.assertEqual(result, expected_data)
        mock_cursor.execute.assert_called_with("SELECT * FROM users", ())
        mock_cursor.close.assert_called_once()

    @patch('mysql.connector.connect')
    def test_execute_query(self, mock_connect):
        """Prueba del método execute_query"""
        # Configurar mock
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        # Ejecutar
        db = Database()
        success = db.execute_query("INSERT INTO users VALUES (%s)", ('user1',))
        
        # Verificar
        self.assertTrue(success)
        mock_cursor.execute.assert_called_with("INSERT INTO users VALUES (%s)", ('user1',))
        mock_conn.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
