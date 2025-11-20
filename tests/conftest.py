import pytest
import sys
import os
from unittest.mock import Mock, patch

# Agregar src al path para imports
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

@pytest.fixture(autouse=True)
def setup_test_environment():
    """Configuración automática para todas las pruebas"""
    # Configuración común para pruebas
    pass

@pytest.fixture
def sample_jugador_data():
    """Datos de ejemplo para jugador válido"""
    return {
        'nombre': 'Juan',
        'apellidos': 'Pérez López', 
        'curp': 'PELJ920101HDFRRN01',
        'categoria': 'Sub-12',
        'numero': 10,
        'pagado': 's',
        'equipo': 'Águilas'
    }