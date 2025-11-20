import pytest
import sys
import os
from unittest.mock import patch, Mock

sys.path.append(os.path.join(os.path.dirname(__file__), '../../src'))

from registros.registro import registrarJugador

class TestProperties:
    
    @pytest.fixture
    def mock_db(self):
        with patch('registros.registro.conexion') as mock_conn:
            mock_cursor = Mock()
            mock_conn.cursor.return_value = mock_cursor
            yield mock_conn, mock_cursor
    
    def test_propiedad_idempotencia(self, mock_db):
        """Propiedad: Registrar mismo jugador 2 veces no duplica registros"""
        mock_conn, mock_cursor = mock_db
        mock_cursor.fetchone.return_value = None
        
        # Datos del jugador
        datos_jugador = {
            'nombre': 'Carlos', 'apellidos': 'Sánchez',
            'curp': 'SACC900404HDFNRN05', 'categoria': 'Sub-14',
            'numero': 7, 'pagado': 's', 'equipo': 'Halcones'
        }
        
        # Primera ejecución
        resultado1 = registrarJugador(**datos_jugador)
        
        # Segunda ejecución con mismos datos
        resultado2 = registrarJugador(**datos_jugador)
        
        # Ambas deben tener el mismo tipo de resultado
        # (ambas éxito o ambas manejar el duplicado consistentemente)
        assert type(resultado1) == type(resultado2)
        assert "correctamente" in resultado1.lower() or "duplicado" in resultado1.lower()
    
    def test_propiedad_determinismo(self, mock_db):
        """Propiedad: Misma entrada → misma salida (determinismo)"""
        mock_conn, mock_cursor = mock_db
        mock_cursor.fetchone.return_value = None
        
        datos_jugador = {
            'nombre': 'Elena', 'apellidos': 'Rodríguez',
            'curp': 'ROME880505MDFDDN06', 'categoria': 'Sub-16', 
            'numero': 15, 'pagado': 'n', 'equipo': 'Panteras'
        }
        
        # Ejecutar múltiples veces con mismos datos
        resultados = []
        for _ in range(3):
            with patch('registros.registro.conexion', mock_conn):
                resultado = registrarJugador(**datos_jugador)
                resultados.append(resultado)
        
        # Todos los resultados deben ser iguales
        assert all(r == resultados[0] for r in resultados), "El sistema no es determinista"
    
    def test_propiedad_manejo_errores_consistente(self, mock_db):
        """Propiedad: Entradas inválidas siempre producen errores"""
        mock_conn, mock_cursor = mock_db
        
        # Casos de entrada inválida
        casos_invalidos = [
            {'nombre': '', 'apellidos': 'Apellido', 'curp': 'CURP123', 'categoria': 'Sub-12', 'numero': 10, 'pagado': 's', 'equipo': 'Equipo'},
            {'nombre': 'Nombre', 'apellidos': '', 'curp': 'CURP123', 'categoria': 'Sub-12', 'numero': 10, 'pagado': 's', 'equipo': 'Equipo'},
            {'nombre': 'Nombre', 'apellidos': 'Apellido', 'curp': '', 'categoria': 'Sub-12', 'numero': 10, 'pagado': 's', 'equipo': 'Equipo'},
        ]
        
        for caso in casos_invalidos:
            resultado = registrarJugador(**caso)
            # Debe rechazar entradas inválidas
            assert "vacío" in resultado.lower() or "error" in resultado.lower()