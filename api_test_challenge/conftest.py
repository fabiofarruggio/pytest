import pytest
from api_test_challenge.pages.import_api import ImportAPI

@pytest.fixture
def import_api():
    """
    Fixture profesional que proporciona una instancia de ImportAPI
    
    Configurada con parámetros por defecto para entorno de testing.
    Permite reutilización y consistencia en todas las pruebas.
    
    Returns:
        ImportAPI: Instancia configurada de la API
    """
    return ImportAPI()

@pytest.fixture(params=[111, 222, 333])
def valid_person_id(request):
    """
    Fixture parametrizada que proporciona diferentes person_id válidos
    
    Returns:
        int: ID de persona válido
    """
    return request.param

@pytest.fixture(params=[0, -1, 999999])
def invalid_person_id(request):
    """
    Fixture parametrizada que proporciona diferentes person_id inválidos
    
    Returns:
        int: ID de persona inválido
    """
    return request.param

@pytest.fixture
def setup_logging():
    """
    Fixture para configurar logging durante las pruebas
    """
    import logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__) 