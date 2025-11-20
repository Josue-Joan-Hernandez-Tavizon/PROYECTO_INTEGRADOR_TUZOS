import pytest
import sys
import os
from unittest.mock import Mock, patch, MagicMock

# Agregar src al path para imports
sys.path.append(os.path.join(os.path.dirname(__file__), '../../src'))

from registros.registro import registrarJugador, agregarHorario, registrarPartido, registrarTorneo, vaciarRegistros

class TestRegistro:
    
    @pytest.fixture
    def mock_db(self):
        """Fixture para simular la conexión a BD"""
        with patch('registros.registro.conexion') as mock_conn:
            mock_cursor = Mock()
            mock_conn.cursor.return_value = mock_cursor
            mock_conn.commit.return_value = None
            yield mock_conn, mock_cursor
    
    # PRUEBAS HAPPY PATH
    def test_registrar_jugador_valido(self, mock_db):
        """Test: Registrar jugador con datos válidos"""
        mock_conn, mock_cursor = mock_db
        mock_cursor.fetchone.return_value = None  # Simula equipo no existente
        
        # Datos válidos
        resultado = registrarJugador(
            nombre="Juan",
            apellidos="Pérez López",
            curp="PELJ920101HDFRRN01",
            categoria="Sub-12", 
            numero=10,
            pagado="s",
            equipo="Águilas"
        )
        
        # Verificar que se llamó a execute para insertar
        assert mock_cursor.execute.called
        assert "insertado correctamente" in resultado.lower()
    
    def test_agregar_horario_valido(self, mock_db):
        """Test: Agregar horario con datos válidos"""
        mock_conn, mock_cursor = mock_db
        mock_cursor.fetchone.return_value = None  # Simula horario no duplicado
        
        resultado = agregarHorario("Lunes", "Sub-12", "17:00-18:30")
        
        assert mock_cursor.execute.called
        assert "registrado" in resultado.lower()
    
    # PRUEBAS UNHAPPY PATH  
    def test_registrar_jugador_campos_vacios(self, mock_db):
        """Test: Error al registrar jugador con campos vacíos"""
        mock_conn, mock_cursor = mock_db
        
        resultado = registrarJugador(
            nombre="",  # Campo vacío
            apellidos="Pérez López",
            curp="PELJ920101HDFRRN01",
            categoria="Sub-12",
            numero=10,
            pagado="s",
            equipo="Águilas"
        )
        
        assert "vacío" in resultado.lower()
        assert not mock_cursor.execute.called
    
    def test_registrar_jugador_curp_invalida(self, mock_db):
        """Test: Error con CURP de longitud incorrecta"""
        mock_conn, mock_cursor = mock_db
        
        resultado = registrarJugador(
            nombre="Juan",
            apellidos="Pérez López",
            curp="CURPINVALIDA",  # CURP muy corta
            categoria="Sub-12",
            numero=10,
            pagado="s",
            equipo="Águilas"
        )
        
        assert "curp" in resultado.lower()
        assert not mock_cursor.execute.called
    
    # PRUEBAS DE FRONTERA
    def test_numero_jugador_frontera(self, mock_db):
        """Test: Números en los límites (1 y 99)"""
        mock_conn, mock_cursor = mock_db
        mock_cursor.fetchone.return_value = None
        
        # Frontera inferior
        resultado1 = registrarJugador(
            nombre="Ana", apellidos="García", curp="GARA950202MDFRRN02",
            categoria="Sub-12", numero=1, pagado="s", equipo="Tigres"
        )
        
        # Frontera superior  
        resultado2 = registrarJugador(
            nombre="Luis", apellidos="Martínez", curp="MALJ880303HDFRRN03", 
            categoria="Sub-12", numero=99, pagado="s", equipo="Leones"
        )
        
        assert "correctamente" in resultado1.lower()
        assert "correctamente" in resultado2.lower()
    
    def test_numero_jugador_fuera_frontera(self, mock_db):
        """Test: Números fuera de límites (0 y 100)"""
        mock_conn, mock_cursor = mock_db
        
        # Menor que mínimo
        resultado1 = registrarJugador(
            nombre="Ana", apellidos="García", curp="GARA950202MDFRRN02",
            categoria="Sub-12", numero=0, pagado="s", equipo="Tigres"
        )
        
        # Mayor que máximo
        resultado2 = registrarJugador(
            nombre="Luis", apellidos="Martínez", curp="MALJ880303HDFRRN03",
            categoria="Sub-12", numero=100, pagado="s", equipo="Leones"  
        )
        
        assert "inválido" in resultado1.lower() or "error" in resultado1.lower()
        assert "inválido" in resultado2.lower() or "error" in resultado2.lower()

if __name__ == "__main__":
    pytest.main([__file__, "-v"])