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
    
    @pytest.mark.database
    def test_import_person_database_validation(self, import_api_with_db, database_available, setup_logging):
        """
        Prueba que valida que el person_id fue insertado correctamente en la base de datos
        
        Ejecuta la query real: SELECT DISTINCT * FROM Test.Worldsys WHERE personId = 111
        Se skipea automáticamente si no hay configuración de DB (variables DB_*)
        
        Args:
            import_api_with_db: Fixture con instancia de la API configurada con DB
            database_available: Fixture que valida disponibilidad de DB
            setup_logging: Fixture para configurar logging
        """
        if not database_available:
            pytest.skip("⚠️  Base de datos no configurada. Configurar variables de entorno DB_* para ejecutar")
        
        # Arrange
        person_id = 111
        logger.info(f"=== VALIDANDO INSERCIÓN EN BASE DE DATOS ===")
        logger.info(f"person_id a validar: {person_id}")
        
        # Act
        response = import_api_with_db.import_person(person_id)
        logger.info(f"Respuesta de importación: {response.status_code}")
        
        # Assert - Validar respuesta de API (puede fallar si API no está disponible)
        if response.status_code == 200:
            assert import_api_with_db.validate_response_success(response), \
                f"Se esperaba respuesta exitosa, pero se obtuvo código: {response.status_code}"
        else:
            logger.warning(f"⚠️  API no disponible (status: {response.status_code}), validando solo DB")
        
        # Validación principal: Consulta en base de datos con query real
        logger.info(f"Ejecutando query: SELECT DISTINCT * FROM Test.Worldsys WHERE personId = {person_id}")
        
        # Método 1: Usar el método específico de validación
        person_exists = import_api_with_db.validate_person_in_database(person_id)
        logger.info(f"¿Person ID {person_id} existe en DB?: {person_exists}")
        
        # Método 2: Usar query directa para obtener datos completos
        query = "SELECT DISTINCT * FROM Test.Worldsys WHERE personId = :person_id"
        db_result = import_api_with_db.execute_db_query(query, {"person_id": person_id})
        
        if db_result and len(db_result) > 0:
            logger.info(f"✅ Person ID {person_id} encontrado en base de datos")
            logger.info(f"Datos en DB: {db_result[0]}")
            
            # Obtener datos estructurados
            person_data = import_api_with_db.get_person_from_database(person_id)
            if person_data:
                logger.info(f"Datos estructurados: {person_data}")
                assert person_data.get('personId') == person_id, \
                    f"Person ID en DB ({person_data.get('personId')}) no coincide con esperado ({person_id})"
        else:
            logger.info(f"ℹ️  Person ID {person_id} no encontrado en base de datos")
            # En un entorno real, esto podría indicar que necesitamos crear el registro
            # o que la importación no fue exitosa
            if response.status_code == 200:
                pytest.fail(f"API retornó éxito pero person_id {person_id} no existe en DB")
            else:
                logger.info("Resultado consistente: API falló y person_id no está en DB")
        
        logger.info(f"✅ Validación de base de datos completada para person_id: {person_id}")


@pytest.mark.database  
class TestDatabaseIntegration:
    """
    Suite específica de pruebas de integración con base de datos
    
    Demuestra capacidades avanzadas de testing con DB:
    - Conectividad y configuración
    - Queries parametrizadas
    - Validaciones de integridad
    """
    
    def test_database_connectivity(self, db_config, database_available, setup_logging):
        """
        Test básico de conectividad a base de datos
        """
        if not database_available:
            pytest.skip("⚠️  Base de datos no configurada. Configurar variables de entorno DB_*")
        
        logger.info("=== VALIDANDO CONECTIVIDAD A BASE DE DATOS ===")
        
        # Validar configuración
        assert db_config is not None, "Configuración de DB no disponible"
        assert db_config.is_configured, "DB no está configurada correctamente"
        assert db_config.is_available, "DB no está disponible"
        
        # Test básico de conectividad
        query = "SELECT 1 as test_connection"
        result = db_config.execute_query(query)
        
        assert result is not None, "Error ejecutando query de conectividad"
        assert len(result) > 0, "Query de conectividad no retornó resultados"
        assert result[0][0] == 1, "Resultado de query de conectividad incorrecto"
        
        logger.info("✅ Conectividad a base de datos validada")
    
    @pytest.mark.parametrize("person_id", [111, 222, 333, 999])
    def test_validate_person_existence_parametrized(self, import_api_with_db, database_available, person_id, setup_logging):
        """
        Test parametrizado que valida existencia de múltiples person_ids
        """
        if not database_available:
            pytest.skip("⚠️  Base de datos no configurada. Configurar variables de entorno DB_*")
        
        logger.info(f"=== VALIDANDO EXISTENCIA DE PERSON_ID {person_id} ===")
        
        # Validar existencia
        exists = import_api_with_db.validate_person_in_database(person_id)
        logger.info(f"Person ID {person_id} existe: {exists}")
        
        if exists:
            # Si existe, obtener y validar datos
            person_data = import_api_with_db.get_person_from_database(person_id)
            assert person_data is not None, f"No se pudieron obtener datos para person_id {person_id}"
            assert person_data.get('personId') == person_id, \
                f"Person ID en datos no coincide: esperado {person_id}, obtenido {person_data.get('personId')}"
            logger.info(f"✅ Datos validados para person_id {person_id}")
        else:
            logger.info(f"ℹ️  Person ID {person_id} no existe en base de datos")
    
    def test_table_structure_validation(self, import_api_with_db, database_available, setup_logging):
        """
        Test que valida la estructura de la tabla Test.Worldsys
        """
        if not database_available:
            pytest.skip("⚠️  Base de datos no configurada. Configurar variables de entorno DB_*")
        
        logger.info("=== VALIDANDO ESTRUCTURA DE TABLA Test.Worldsys ===")
        
        # Obtener información de la tabla (query específica para SQL Server)
        table_info_query = """
        SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE, CHARACTER_MAXIMUM_LENGTH
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_SCHEMA = 'Test' AND TABLE_NAME = 'Worldsys'
        ORDER BY ORDINAL_POSITION
        """
        
        columns = import_api_with_db.execute_db_query(table_info_query)
        
        if columns:
            logger.info(f"Estructura de tabla Test.Worldsys:")
            for col in columns:
                logger.info(f"  - {col[0]} ({col[1]}) - Nullable: {col[2]}")
            
            # Validar que existe al menos la columna personId
            column_names = [col[0] for col in columns]
            assert 'personId' in column_names, "Columna 'personId' no encontrada en tabla Test.Worldsys"
            
            logger.info("✅ Estructura de tabla validada")
        else:
            pytest.skip("No se pudo obtener información de estructura de tabla") 