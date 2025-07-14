"""
Tests mockeados para el API Import usando pytest y unittest.mock
Este archivo contiene tests que simulan las respuestas de la API para demostrar
el funcionamiento del framework sin depender de conexiones reales.
"""

import pytest
import json
from unittest.mock import Mock, patch
from api_test_challenge.pages.import_api import ImportAPI


@pytest.mark.mocked
class TestImportAPIMocked:
    """Clase de tests mockeados para ImportAPI"""

    @pytest.fixture
    def import_api(self):
        """Fixture que retorna instancia de ImportAPI"""
        return ImportAPI()

    def test_import_person_happy_path_mocked(self, import_api):
        """
        Test mockeado del happy path - importación exitosa
        """
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "status": "success",
            "message": "Person imported successfully",
            "personId": 111
        }
        mock_response.headers = {"Content-Type": "application/json"}
        
        # Act
        with patch.object(import_api.session, 'post', return_value=mock_response):
            response = import_api.import_person(111)
        
        # Assert
        assert response.status_code == 200
        assert response.json()["status"] == "success"
        assert response.json()["personId"] == 111

    @pytest.mark.parametrize("person_id,expected_status", [
        (111, 200),
        (222, 200),
        (333, 200),
        (444, 200)
    ])
    def test_import_person_with_valid_ids_mocked(self, import_api, person_id, expected_status):
        """
        Test mockeado con múltiples person_id válidos
        """
        # Arrange
        mock_response = Mock()
        mock_response.status_code = expected_status
        mock_response.json.return_value = {
            "status": "success",
            "message": "Person imported successfully",
            "personId": person_id
        }
        
        # Act
        with patch.object(import_api.session, 'post', return_value=mock_response):
            response = import_api.import_person(person_id)
        
        # Assert
        assert response.status_code == expected_status
        assert response.json()["personId"] == person_id

    def test_import_person_sad_path_invalid_id_mocked(self, import_api):
        """
        Test mockeado del sad path - ID inválido
        """
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {
            "status": "error",
            "message": "Invalid person ID",
            "error": "INVALID_PERSON_ID"
        }
        
        # Act
        with patch.object(import_api.session, 'post', return_value=mock_response):
            response = import_api.import_person(-1)
        
        # Assert
        assert response.status_code == 400
        assert response.json()["status"] == "error"
        assert "invalid" in response.json()["message"].lower()

    def test_import_person_sad_path_missing_auth_mocked(self, import_api):
        """
        Test mockeado del sad path - falta autenticación
        """
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.json.return_value = {
            "status": "error",
            "message": "Authentication required",
            "error": "UNAUTHORIZED"
        }
        
        # Act
        with patch.object(import_api.session, 'post', return_value=mock_response):
            response = import_api.import_person(111)
        
        # Assert
        assert response.status_code == 401
        assert response.json()["status"] == "error"
        assert "authentication" in response.json()["message"].lower()

    def test_import_person_sad_path_server_error_mocked(self, import_api):
        """
        Test mockeado del sad path - error del servidor
        """
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {
            "status": "error",
            "message": "Internal server error",
            "error": "SERVER_ERROR"
        }
        
        # Act
        with patch.object(import_api.session, 'post', return_value=mock_response):
            response = import_api.import_person(111)
        
        # Assert
        assert response.status_code == 500
        assert response.json()["status"] == "error"

    def test_import_person_response_time_mocked(self, import_api):
        """
        Test mockeado de tiempo de respuesta
        """
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "success", "personId": 111}
        mock_response.elapsed.total_seconds.return_value = 0.5
        
        # Act
        with patch.object(import_api.session, 'post', return_value=mock_response):
            response = import_api.import_person(111)
        
        # Assert
        assert response.status_code == 200
        # Validar que el tiempo de respuesta es aceptable (simulado)
        assert response.elapsed.total_seconds() < 2.0

    def test_import_person_invalid_payload_mocked(self, import_api):
        """
        Test mockeado con payload inválido
        """
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {
            "status": "error",
            "message": "Invalid payload format",
            "error": "BAD_REQUEST"
        }
        
        # Act
        with patch.object(import_api.session, 'post', return_value=mock_response):
            response = import_api.import_person_invalid_payload([])
        
        # Assert
        assert response.status_code == 400
        assert response.json()["status"] == "error"

    def test_import_person_headers_validation_mocked(self, import_api):
        """
        Test mockeado para validar headers de respuesta
        """
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {
            "Content-Type": "application/json",
            "X-API-Version": "1.0",
            "X-Rate-Limit": "1000"
        }
        mock_response.json.return_value = {"status": "success", "personId": 111}
        
        # Act
        with patch.object(import_api.session, 'post', return_value=mock_response):
            response = import_api.import_person(111)
        
        # Assert
        assert response.status_code == 200
        assert response.headers["Content-Type"] == "application/json"
        assert "X-API-Version" in response.headers 