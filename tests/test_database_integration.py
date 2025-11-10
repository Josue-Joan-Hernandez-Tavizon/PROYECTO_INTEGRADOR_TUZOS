import sys
import os
# Agregar el directorio raíz del proyecto al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from src.models.database import Database

class TestDatabaseIntegration:
    """Tests de integración para la base de datos"""
    
    def test_database_connection(self):
        """Verifica que la conexión a la base de datos se establezca correctamente"""
        db = Database()
        assert db.connection is not None
        db.close()
    
    def test_fetch_all_usuarios(self):
        """Verifica que se puedan obtener datos de la tabla usuarios"""
        db = Database()
        query = "SELECT * FROM usuarios LIMIT 1"
        result = db.fetch_all(query)
        # Verificar que devuelva una lista (puede estar vacía o con datos)
        assert isinstance(result, list)
        db.close()
    
    def test_execute_query_safe(self):
        """Prueba una query SELECT segura para no modificar datos"""
        db = Database()
        # Usamos una query SELECT que no modifica datos
        query = "SELECT COUNT(*) FROM usuarios"
        result = db.fetch_all(query)
        assert isinstance(result, list)
        assert len(result) > 0
        db.close()
    
    def test_connection_properties(self):
        """Verifica las propiedades de la conexión"""
        db = Database()
        if db.connection:
            # Verificar que la conexión esté activa
            assert db.connection.is_connected()
        db.close()

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
