import pytest
import logging
from unittest.mock import Mock, patch, MagicMock
from api_test_challenge.pages.import_api import ImportAPI

# Configurar logger para las pruebas
logger = logging.getLogger(__name__)


@pytest.mark.mocked_database
class TestDatabaseMocked:
    """
    Suite de pruebas mockeadas para funcionalidad de base de datos
    
    Estos tests siempre pasan y demuestran capacidades del framework:
    - Conectividad a base de datos
    - Validación de existencia de registros
    - Queries parametrizadas
    - Manejo de errores de DB
    """
    
    @patch('api_test_challenge.database_config.db_config')
    def test_database_connectivity_success(self, mock_db_config, import_api, setup_logging):
        """
        Test mockeado que simula conectividad exitosa a base de datos
        """
        logger.info("=== TEST MOCKEADO: CONECTIVIDAD DB EXITOSA ===")
        
        # Arrange - Configurar mocks
        mock_db_config.is_configured = True
        mock_db_config.is_available = True
        mock_db_config.execute_query.return_value = [(1,)]
        
        # Asignar mock a la instancia de ImportAPI
        import_api.db_config = mock_db_config
        
        # Act
        result = import_api.execute_db_query("SELECT 1")
        
        # Assert
        assert result is not None, "Query de conectividad falló"
        assert len(result) > 0, "Query no retornó resultados"
        assert result[0][0] == 1, "Resultado incorrecto"
        
        # Verificar que se llamó el método correcto
        mock_db_config.execute_query.assert_called_once_with("SELECT 1", None)
        
        logger.info("✅ Conectividad mockeada validada exitosamente")
    
    @patch('api_test_challenge.database_config.db_config')
    def test_validate_person_exists_success(self, mock_db_config, import_api, setup_logging):
        """
        Test mockeado que simula validación exitosa de existencia de persona
        """
        logger.info("=== TEST MOCKEADO: VALIDACIÓN EXISTENCIA PERSONA ===")
        
        # Arrange
        person_id = 111
        mock_db_config.is_configured = True
        mock_db_config.is_available = True
        mock_db_config.validate_person_exists.return_value = True
        
        import_api.db_config = mock_db_config
        
        # Act
        exists = import_api.validate_person_in_database(person_id)
        
        # Assert
        assert exists is True, f"Person ID {person_id} debería existir en DB mockeada"
        mock_db_config.validate_person_exists.assert_called_once_with(person_id)
        
        logger.info(f"✅ Person ID {person_id} validado exitosamente en DB mockeada")
    
    @patch('api_test_challenge.database_config.db_config')
    def test_get_person_data_success(self, mock_db_config, import_api, setup_logging):
        """
        Test mockeado que simula obtención exitosa de datos de persona
        """
        logger.info("=== TEST MOCKEADO: OBTENER DATOS DE PERSONA ===")
        
        # Arrange
        person_id = 111
        expected_data = {
            "personId": person_id,
            "firstName": "John",
            "lastName": "Doe",
            "email": "john.doe@example.com",
            "created_at": "2024-01-15 10:30:00"
        }
        
        mock_db_config.is_configured = True
        mock_db_config.is_available = True
        mock_db_config.get_person_data.return_value = expected_data
        
        import_api.db_config = mock_db_config
        
        # Act
        person_data = import_api.get_person_from_database(person_id)
        
        # Assert
        assert person_data is not None, "No se obtuvieron datos de la persona"
        assert person_data["personId"] == person_id, "Person ID no coincide"
        assert person_data["firstName"] == "John", "Nombre no coincide"
        assert person_data["email"] == "john.doe@example.com", "Email no coincide"
        
        mock_db_config.get_person_data.assert_called_once_with(person_id)
        
        logger.info(f"✅ Datos de person_id {person_id} obtenidos exitosamente")
        logger.info(f"Datos: {person_data}")
    
    @pytest.mark.parametrize("person_id,expected_exists", [
        (111, True),
        (222, True),
        (333, True),
        (999, False),
        (0, False),
        (-1, False)
    ])
    @patch('api_test_challenge.database_config.db_config')
    def test_validate_multiple_persons_parametrized(self, mock_db_config, import_api, person_id, expected_exists, setup_logging):
        """
        Test mockeado parametrizado que valida múltiples person_ids
        """
        logger.info(f"=== TEST MOCKEADO PARAMETRIZADO: PERSON_ID {person_id} ===")
        
        # Arrange
        mock_db_config.is_configured = True
        mock_db_config.is_available = True
        mock_db_config.validate_person_exists.return_value = expected_exists
        
        if expected_exists:
            mock_db_config.get_person_data.return_value = {
                "personId": person_id,
                "firstName": f"User{person_id}",
                "lastName": "Test",
                "email": f"user{person_id}@test.com"
            }
        else:
            mock_db_config.get_person_data.return_value = None
        
        import_api.db_config = mock_db_config
        
        # Act
        exists = import_api.validate_person_in_database(person_id)
        
        # Assert
        assert exists == expected_exists, \
            f"Resultado de existencia para person_id {person_id} no coincide. Esperado: {expected_exists}, Obtenido: {exists}"
        
        if expected_exists:
            person_data = import_api.get_person_from_database(person_id)
            assert person_data is not None, f"Datos de person_id {person_id} deberían estar disponibles"
            assert person_data["personId"] == person_id, "Person ID en datos no coincide"
        
        logger.info(f"✅ Person ID {person_id} - Existe: {exists}")
    
    @patch('api_test_challenge.database_config.db_config')
    def test_database_error_handling(self, mock_db_config, import_api, setup_logging):
        """
        Test mockeado que simula manejo de errores de base de datos
        """
        logger.info("=== TEST MOCKEADO: MANEJO DE ERRORES DB ===")
        
        # Arrange - Simular error de DB
        mock_db_config.is_configured = True
        mock_db_config.is_available = False  # DB no disponible
        
        import_api.db_config = mock_db_config
        
        # Act
        exists = import_api.validate_person_in_database(111)
        person_data = import_api.get_person_from_database(111)
        query_result = import_api.execute_db_query("SELECT * FROM Test.Worldsys")
        
        # Assert - Todos deberían manejar gracefully la DB no disponible
        assert exists is False, "Validación debería retornar False cuando DB no está disponible"
        assert person_data is None, "Datos deberían ser None cuando DB no está disponible"
        assert query_result is None, "Query debería retornar None cuando DB no está disponible"
        
        logger.info("✅ Manejo de errores DB validado correctamente")
    
    @patch('api_test_challenge.database_config.db_config')
    def test_database_not_configured(self, mock_db_config, import_api, setup_logging):
        """
        Test mockeado que simula DB no configurada (sin variables de entorno)
        """
        logger.info("=== TEST MOCKEADO: DB NO CONFIGURADA ===")
        
        # Arrange - Simular DB no configurada
        mock_db_config.is_configured = False
        mock_db_config.is_available = False
        
        import_api.db_config = mock_db_config
        
        # Act
        exists = import_api.validate_person_in_database(111)
        person_data = import_api.get_person_from_database(111)
        
        # Assert
        assert exists is False, "Validación debería retornar False cuando DB no está configurada"
        assert person_data is None, "Datos deberían ser None cuando DB no está configurada"
        
        logger.info("✅ Comportamiento con DB no configurada validado")
    
    @patch('api_test_challenge.database_config.db_config')
    def test_complex_database_query(self, mock_db_config, import_api, setup_logging):
        """
        Test mockeado que simula query compleja con joins y aggregaciones
        """
        logger.info("=== TEST MOCKEADO: QUERY COMPLEJA ===")
        
        # Arrange
        complex_query = """
        SELECT 
            p.personId,
            p.firstName,
            p.lastName,
            COUNT(o.orderId) as total_orders,
            MAX(o.order_date) as last_order_date
        FROM Test.Worldsys p
        LEFT JOIN Orders o ON p.personId = o.personId
        WHERE p.personId IN (:person_ids)
        GROUP BY p.personId, p.firstName, p.lastName
        HAVING COUNT(o.orderId) > 0
        ORDER BY total_orders DESC
        """
        
        expected_results = [
            (111, "John", "Doe", 5, "2024-01-15"),
            (222, "Jane", "Smith", 3, "2024-01-10"),
            (333, "Bob", "Johnson", 1, "2024-01-05")
        ]
        
        mock_db_config.is_configured = True
        mock_db_config.is_available = True
        mock_db_config.execute_query.return_value = expected_results
        
        import_api.db_config = mock_db_config
        
        # Act
        params = {"person_ids": [111, 222, 333]}
        results = import_api.execute_db_query(complex_query, params)
        
        # Assert
        assert results is not None, "Query compleja no retornó resultados"
        assert len(results) == 3, "Número de resultados incorrecto"
        
        # Validar estructura de resultados
        for i, row in enumerate(results):
            expected_row = expected_results[i]
            assert row[0] == expected_row[0], f"Person ID incorrecto en fila {i}"
            assert row[3] >= 1, f"Total orders debería ser >= 1 en fila {i}"
        
        # Verificar que la query se ejecutó con parámetros correctos
        mock_db_config.execute_query.assert_called_once_with(complex_query, params)
        
        logger.info("✅ Query compleja ejecutada exitosamente")
        logger.info(f"Resultados: {results}")


@pytest.mark.mocked_database
class TestDatabaseIntegrationMocked:
    """
    Suite mockeada para tests de integración API + Base de datos
    
    Simula el flujo completo:
    1. Llamada a API de importación
    2. Validación en base de datos
    3. Verificación de consistencia
    """
    
    @patch('api_test_challenge.database_config.db_config')
    @patch('requests.post')
    def test_end_to_end_import_and_db_validation(self, mock_post, mock_db_config, import_api, setup_logging):
        """
        Test end-to-end mockeado: API + DB integration
        """
        logger.info("=== TEST E2E MOCKEADO: API + DB ===")
        
        # Arrange - Mock API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"success": True, "personId": 111}
        mock_response.elapsed.total_seconds.return_value = 0.5
        mock_post.return_value = mock_response
        
        # Mock DB responses
        mock_db_config.is_configured = True
        mock_db_config.is_available = True
        mock_db_config.validate_person_exists.return_value = True
        mock_db_config.get_person_data.return_value = {
            "personId": 111,
            "firstName": "Test",
            "lastName": "User",
            "email": "test@example.com",
            "created_at": "2024-01-15 10:30:00"
        }
        
        import_api.db_config = mock_db_config
        
        # Act
        person_id = 111
        
        # 1. Importar vía API
        api_response = import_api.import_person(person_id)
        
        # 2. Validar en DB
        db_exists = import_api.validate_person_in_database(person_id)
        person_data = import_api.get_person_from_database(person_id)
        
        # Assert
        # Validar API
        assert import_api.validate_response_success(api_response), "Importación API falló"
        assert api_response.json()["personId"] == person_id, "Person ID en respuesta API no coincide"
        
        # Validar DB
        assert db_exists is True, "Person ID no encontrado en DB después de importación"
        assert person_data is not None, "No se pudieron obtener datos de DB"
        assert person_data["personId"] == person_id, "Person ID en DB no coincide"
        
        # Verificar llamadas a mocks
        mock_post.assert_called_once()
        mock_db_config.validate_person_exists.assert_called_once_with(person_id)
        mock_db_config.get_person_data.assert_called_once_with(person_id)
        
        logger.info("✅ Flujo E2E API + DB completado exitosamente")
        logger.info(f"API Response: {api_response.json()}")
        logger.info(f"DB Data: {person_data}")
    
    @patch('api_test_challenge.database_config.db_config')
    @patch('requests.post')
    def test_api_success_but_db_inconsistency(self, mock_post, mock_db_config, import_api, setup_logging):
        """
        Test que simula API exitosa pero inconsistencia en DB (caso edge)
        """
        logger.info("=== TEST MOCKEADO: INCONSISTENCIA API vs DB ===")
        
        # Arrange - API exitosa
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"success": True, "personId": 111}
        mock_post.return_value = mock_response
        
        # DB indica que no existe (inconsistencia)
        mock_db_config.is_configured = True
        mock_db_config.is_available = True
        mock_db_config.validate_person_exists.return_value = False
        mock_db_config.get_person_data.return_value = None
        
        import_api.db_config = mock_db_config
        
        # Act
        person_id = 111
        api_response = import_api.import_person(person_id)
        db_exists = import_api.validate_person_in_database(person_id)
        
        # Assert
        assert import_api.validate_response_success(api_response), "API debería ser exitosa"
        assert db_exists is False, "DB debería indicar que no existe"
        
        # Esta situación requiere logging especial para investigación
        logger.warning("⚠️  INCONSISTENCIA DETECTADA: API exitosa pero person_id no encontrado en DB")
        logger.warning(f"API Status: {api_response.status_code}")
        logger.warning(f"DB Exists: {db_exists}")
        
        logger.info("✅ Detección de inconsistencia API vs DB validada")
    
    @patch('api_test_challenge.database_config.db_config')
    def test_bulk_person_validation(self, mock_db_config, import_api, setup_logging):
        """
        Test mockeado para validación masiva de personas en DB
        """
        logger.info("=== TEST MOCKEADO: VALIDACIÓN MASIVA ===")
        
        # Arrange
        person_ids = [111, 222, 333, 444, 555]
        existing_ids = [111, 222, 333]  # Solo algunos existen
        
        def mock_validate_person_exists(person_id):
            return person_id in existing_ids
        
        def mock_get_person_data(person_id):
            if person_id in existing_ids:
                return {
                    "personId": person_id,
                    "firstName": f"User{person_id}",
                    "lastName": "Test"
                }
            return None
        
        mock_db_config.is_configured = True
        mock_db_config.is_available = True
        mock_db_config.validate_person_exists.side_effect = mock_validate_person_exists
        mock_db_config.get_person_data.side_effect = mock_get_person_data
        
        import_api.db_config = mock_db_config
        
        # Act
        results = {}
        for person_id in person_ids:
            exists = import_api.validate_person_in_database(person_id)
            data = import_api.get_person_from_database(person_id) if exists else None
            results[person_id] = {"exists": exists, "data": data}
        
        # Assert
        assert len(results) == len(person_ids), "Número de resultados incorrecto"
        
        # Validar existentes
        for person_id in existing_ids:
            assert results[person_id]["exists"] is True, f"Person ID {person_id} debería existir"
            assert results[person_id]["data"] is not None, f"Data de person_id {person_id} debería estar disponible"
        
        # Validar no existentes
        non_existing = [444, 555]
        for person_id in non_existing:
            assert results[person_id]["exists"] is False, f"Person ID {person_id} no debería existir"
            assert results[person_id]["data"] is None, f"Data de person_id {person_id} debería ser None"
        
        logger.info("✅ Validación masiva completada")
        logger.info(f"Existentes: {existing_ids}")
        logger.info(f"No existentes: {non_existing}") 