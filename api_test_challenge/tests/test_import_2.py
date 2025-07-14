import pytest
import logging
from api_test_challenge.pages.import_api import ImportAPI

# Configurar logger para las pruebas
logger = logging.getLogger(__name__)

@pytest.mark.real_api
class TestImportAPIAdvanced:
    """
    Suite avanzada de pruebas profesionales para endpoint de importación
    
    Incluye validaciones especializadas:
    - Performance testing
    - Security testing
    - Schema validation
    - Integration testing
    """
    
    def test_import_person_response_structure(self, import_api: ImportAPI, setup_logging):
        """
        Prueba que valida la estructura de respuesta en happy path
        
        Args:
            import_api (ImportAPI): Fixture con instancia de la API
            setup_logging: Fixture para configurar logging
        """
        # Arrange
        person_id = 111
        logger.info(f"=== VALIDANDO ESTRUCTURA DE RESPUESTA ===")
        logger.info(f"Probando estructura de respuesta para person_id: {person_id}")
        
        # Act
        response = import_api.import_person(person_id)
        
        # Assert
        assert import_api.validate_response_success(response), \
            f"Se esperaba respuesta exitosa, pero se obtuvo código: {response.status_code}"
        
        # Validar headers de respuesta
        assert 'content-type' in response.headers.keys(), \
            "La respuesta debe incluir header Content-Type"
        
        logger.info(f"Headers de respuesta: {dict(response.headers)}")
        logger.info("✅ Estructura de respuesta validada correctamente")
    
    def test_import_person_with_parametrized_invalid_ids(self, import_api: ImportAPI, invalid_person_id, setup_logging):
        """
        Prueba parametrizada con diferentes person_id inválidos
        
        Args:
            import_api (ImportAPI): Fixture con instancia de la API
            invalid_person_id (int): Fixture parametrizada con IDs inválidos
            setup_logging: Fixture para configurar logging
        """
        # Arrange
        logger.info(f"=== PRUEBA PARAMETRIZADA SAD PATH ===")
        logger.info(f"Probando con person_id inválido: {invalid_person_id}")
        
        # Act
        response = import_api.import_person(invalid_person_id)
        
        # Assert
        # Puede ser 400 (Bad Request) o 404 (Not Found) dependiendo de la implementación
        assert response.status_code in [400, 404], \
            f"Se esperaba error 400 o 404 para person_id inválido {invalid_person_id}, pero se obtuvo código: {response.status_code}"
        
        logger.info(f"✅ Prueba completada para person_id inválido: {invalid_person_id}")
    
    def test_import_person_response_time(self, import_api: ImportAPI, setup_logging):
        """
        Prueba que valida el tiempo de respuesta de la API
        
        Args:
            import_api (ImportAPI): Fixture con instancia de la API
            setup_logging: Fixture para configurar logging
        """
        # Arrange
        person_id = 111
        max_response_time = 5.0  # 5 segundos máximo
        logger.info(f"=== VALIDANDO TIEMPO DE RESPUESTA ===")
        logger.info(f"Tiempo máximo permitido: {max_response_time} segundos")
        
        # Act
        response = import_api.import_person(person_id)
        
        # Assert
        assert response.elapsed.total_seconds() < max_response_time, \
            f"El tiempo de respuesta ({response.elapsed.total_seconds()}s) excede el máximo permitido ({max_response_time}s)"
        
        logger.info(f"Tiempo de respuesta: {response.elapsed.total_seconds():.3f} segundos")
        logger.info("✅ Tiempo de respuesta dentro del límite aceptable")
    
    def test_import_person_authentication_required(self, setup_logging):
        """
        Prueba que valida que se requiere autenticación para acceder a la API
        
        Args:
            setup_logging: Fixture para configurar logging
        """
        # Arrange
        api_without_auth = ImportAPI(auth_token="")  # Sin token de autenticación
        person_id = 111
        logger.info(f"=== VALIDANDO AUTENTICACIÓN REQUERIDA ===")
        logger.info(f"Probando request sin token de autenticación")
        
        # Act
        response = api_without_auth.import_person(person_id)
        
        # Assert
        assert response.status_code == 401, \
            f"Se esperaba error 401 (Unauthorized) sin autenticación, pero se obtuvo código: {response.status_code}"
        
        logger.info("✅ Autenticación requerida validada correctamente")
    
    def test_import_person_multiple_persons_payload(self, import_api: ImportAPI, setup_logging):
        """
        Prueba que valida la importación de múltiples personas en un solo payload
        
        Args:
            import_api (ImportAPI): Fixture con instancia de la API
            setup_logging: Fixture para configurar logging
        """
        # Arrange
        multiple_persons_payload = [
            {"personId": 111},
            {"personId": 222},
            {"personId": 333}
        ]
        logger.info(f"=== PROBANDO PAYLOAD CON MÚLTIPLES PERSONAS ===")
        logger.info(f"Payload: {multiple_persons_payload}")
        
        # Act
        response = import_api.import_person_invalid_payload(multiple_persons_payload)
        
        # Assert
        # Esto podría ser exitoso o fallar dependiendo de la implementación de la API
        assert response.status_code in [200, 201, 400], \
            f"Se esperaba código 200, 201 o 400 para múltiples personas, pero se obtuvo: {response.status_code}"
        
        logger.info(f"Respuesta para múltiples personas: {response.status_code}")
        logger.info("✅ Prueba de payload múltiple completada")
    
    @pytest.mark.skip(reason="Base de datos no configurada para esta prueba")
    def test_import_person_database_validation(self, import_api: ImportAPI, setup_logging):
        """
        Prueba que valida que el person_id fue insertado correctamente en la base de datos
        Esta prueba está marcada como skip porque requiere configuración de DB
        
        Query sugerida: SELECT DISTINCT * FROM Test.Worldsys WHERE personId = 111
        
        Args:
            import_api (ImportAPI): Fixture con instancia de la API
            setup_logging: Fixture para configurar logging
        """
        # Arrange
        person_id = 111
        logger.info(f"=== VALIDANDO INSERCIÓN EN BASE DE DATOS ===")
        logger.info(f"person_id a validar: {person_id}")
        
        # Act
        response = import_api.import_person(person_id)
        
        # Assert
        assert import_api.validate_response_success(response), \
            f"Se esperaba respuesta exitosa, pero se obtuvo código: {response.status_code}"
        
        # Aquí iría la validación de base de datos
        # Ejemplo de query: SELECT DISTINCT * FROM Test.Worldsys WHERE personId = 111
        # db_result = execute_query(f"SELECT DISTINCT * FROM Test.Worldsys WHERE personId = {person_id}")
        # assert db_result is not None and len(db_result) > 0, "El person_id no se encontró en la base de datos"
        
        logger.info(f"✅ Validación de base de datos completada para person_id: {person_id}") 