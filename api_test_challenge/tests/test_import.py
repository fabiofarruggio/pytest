import pytest
import logging
from api_test_challenge.pages.import_api import ImportAPI

# Configurar logger para las pruebas
logger = logging.getLogger(__name__)

@pytest.mark.real_api
class TestImportAPI:
    """
    Suite de pruebas profesional para el endpoint de importación
    
    Implementa estrategias de testing completas incluyendo:
    - Happy Path: Casos de éxito
    - Sad Path: Manejo de errores
    - Edge Cases: Casos límite
    - Data-driven testing: Pruebas parametrizadas
    """
    
    def test_import_person_happy_path(self, import_api: ImportAPI, setup_logging):
        """
        Prueba del happy path: importación exitosa de una persona
        
        Args:
            import_api (ImportAPI): Fixture con instancia de la API
            setup_logging: Fixture para configurar logging
        """
        # Arrange
        person_id = 111
        logger.info(f"=== INICIANDO PRUEBA HAPPY PATH ===")
        logger.info(f"Probando importación de persona con ID: {person_id}")
        
        # Act
        response = import_api.import_person(person_id)
        
        # Assert
        assert import_api.validate_response_success(response), \
            f"Se esperaba respuesta exitosa, pero se obtuvo código: {response.status_code}"
        
        logger.info("✅ Prueba happy path completada exitosamente")
    
    def test_import_person_with_different_valid_ids(self, import_api: ImportAPI, valid_person_id, setup_logging):
        """
        Prueba parametrizada con diferentes person_id válidos
        
        Args:
            import_api (ImportAPI): Fixture con instancia de la API
            valid_person_id (int): Fixture parametrizada con IDs válidos
            setup_logging: Fixture para configurar logging
        """
        # Arrange
        logger.info(f"=== PRUEBA PARAMETRIZADA HAPPY PATH ===")
        logger.info(f"Probando importación con person_id: {valid_person_id}")
        
        # Act
        response = import_api.import_person(valid_person_id)
        
        # Assert
        assert import_api.validate_response_success(response), \
            f"Se esperaba respuesta exitosa para person_id {valid_person_id}, pero se obtuvo código: {response.status_code}"
        
        # Validaciones adicionales
        response_data = import_api.get_response_data(response)
        if response_data:
            logger.info(f"Datos de respuesta: {response_data}")
        
        logger.info(f"✅ Prueba exitosa para person_id: {valid_person_id}")
    
    def test_import_person_sad_path_invalid_person_id(self, import_api: ImportAPI, setup_logging):
        """
        Prueba del sad path: person_id inválido
        
        Args:
            import_api (ImportAPI): Fixture con instancia de la API
            setup_logging: Fixture para configurar logging
        """
        # Arrange
        invalid_person_id = -1
        logger.info(f"=== INICIANDO PRUEBA SAD PATH - PERSON ID INVÁLIDO ===")
        logger.info(f"Probando con person_id inválido: {invalid_person_id}")
        
        # Act
        response = import_api.import_person(invalid_person_id)
        
        # Assert
        assert import_api.validate_response_error(response, 400), \
            f"Se esperaba error 400 para person_id inválido, pero se obtuvo código: {response.status_code}"
        
        logger.info("✅ Prueba sad path completada - error manejado correctamente")
    
    def test_import_person_sad_path_missing_person_id(self, import_api: ImportAPI, setup_logging):
        """
        Prueba del sad path: payload sin person_id
        
        Args:
            import_api (ImportAPI): Fixture con instancia de la API
            setup_logging: Fixture para configurar logging
        """
        # Arrange
        invalid_payload = [{}]  # Payload sin personId
        logger.info(f"=== INICIANDO PRUEBA SAD PATH - PERSON ID FALTANTE ===")
        logger.info(f"Probando con payload sin personId: {invalid_payload}")
        
        # Act
        response = import_api.import_person_invalid_payload(invalid_payload)
        
        # Assert
        assert import_api.validate_response_error(response, 400), \
            f"Se esperaba error 400 para payload sin personId, pero se obtuvo código: {response.status_code}"
        
        logger.info("✅ Prueba sad path completada - error de payload faltante manejado correctamente")
    
    def test_import_person_sad_path_empty_payload(self, import_api: ImportAPI, setup_logging):
        """
        Prueba del sad path: payload vacío
        
        Args:
            import_api (ImportAPI): Fixture con instancia de la API
            setup_logging: Fixture para configurar logging
        """
        # Arrange
        empty_payload = []
        logger.info(f"=== INICIANDO PRUEBA SAD PATH - PAYLOAD VACÍO ===")
        logger.info(f"Probando con payload vacío: {empty_payload}")
        
        # Act
        response = import_api.import_person_invalid_payload(empty_payload)
        
        # Assert
        assert import_api.validate_response_error(response, 400), \
            f"Se esperaba error 400 para payload vacío, pero se obtuvo código: {response.status_code}"
        
        logger.info("✅ Prueba sad path completada - error de payload vacío manejado correctamente")
    
    def test_import_person_sad_path_invalid_data_type(self, import_api: ImportAPI, setup_logging):
        """
        Prueba del sad path: person_id con tipo de dato inválido
        
        Args:
            import_api (ImportAPI): Fixture con instancia de la API
            setup_logging: Fixture para configurar logging
        """
        # Arrange
        invalid_payload = [{"personId": "invalid_string"}]
        logger.info(f"=== INICIANDO PRUEBA SAD PATH - TIPO DE DATO INVÁLIDO ===")
        logger.info(f"Probando con personId como string: {invalid_payload}")
        
        # Act
        response = import_api.import_person_invalid_payload(invalid_payload)
        
        # Assert
        assert import_api.validate_response_error(response, 400), \
            f"Se esperaba error 400 para tipo de dato inválido, pero se obtuvo código: {response.status_code}"
        
        logger.info("✅ Prueba sad path completada - error de tipo de dato inválido manejado correctamente") 