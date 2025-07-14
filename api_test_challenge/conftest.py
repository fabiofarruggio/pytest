import pytest
from api_test_challenge.pages.import_api import ImportAPI

@pytest.fixture
def import_api():
    """
    Fixture que proporciona una instancia de ImportAPI
    
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


# Fixtures para base de datos
@pytest.fixture(scope="session")
def db_config():
    """
    Fixture que proporciona la configuración de base de datos
    
    Returns:
        DatabaseConfig: Instancia de configuración de DB
    """
    try:
        from api_test_challenge.database_config import db_config
        return db_config
    except ImportError:
        return None


@pytest.fixture(scope="session")
def database_available(db_config):
    """
    Fixture que verifica si la base de datos está disponible
    
    Returns:
        bool: True si la DB está configurada y disponible
    """
    if db_config is None:
        return False
    return db_config.is_available


@pytest.fixture
def import_api_with_db(import_api, db_config):
    """
    Fixture que proporciona ImportAPI con configuración de base de datos
    
    Returns:
        ImportAPI: Instancia con DB configurada
    """
    import_api.db_config = db_config
    return import_api 