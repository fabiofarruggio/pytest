import requests
import json
import logging
from typing import Dict, Any, Optional

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ImportAPI:
    """
    Clase que implementa el patrón Page Object Model para API testing profesional
    Maneja las interacciones con endpoints de importación con arquitectura escalable
    
    Esta clase encapsula toda la lógica de comunicación con la API,
    proporcionando métodos reutilizables y mantenibles para testing automatizado.
    """
    
    def __init__(self, base_url: str = "https://api.test.worldsys.ar", auth_token: str = "xxx"):
        """
        Inicializa la clase con la URL base y token de autenticación
        
        Args:
            base_url (str): URL base de la API
            auth_token (str): Token de autenticación Bearer
        """
        self.base_url = base_url
        self.auth_token = auth_token
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {auth_token}"
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def import_person(self, person_id: int) -> requests.Response:
        """
        Realiza la importación de una persona mediante la API
        
        Args:
            person_id (int): ID de la persona a importar
            
        Returns:
            requests.Response: Respuesta de la API
        """
        url = f"{self.base_url}/import"
        payload = [{"personId": person_id}]
        
        logger.info(f"Enviando request POST a: {url}")
        logger.info(f"Payload: {json.dumps(payload, indent=2)}")
        
        try:
            response = self.session.post(url, json=payload)
            logger.info(f"Código de respuesta: {response.status_code}")
            logger.info(f"Respuesta: {response.text}")
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"Error en la request: {str(e)}")
            raise
    
    def import_person_invalid_payload(self, payload: Any) -> requests.Response:
        """
        Realiza una request con payload inválido para testing de sad path
        
        Args:
            payload (Any): Payload inválido para enviar
            
        Returns:
            requests.Response: Respuesta de la API
        """
        url = f"{self.base_url}/import"
        
        logger.info(f"Enviando request POST con payload inválido a: {url}")
        logger.info(f"Payload inválido: {payload}")
        
        try:
            response = self.session.post(url, json=payload)
            logger.info(f"Código de respuesta: {response.status_code}")
            logger.info(f"Respuesta: {response.text}")
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"Error en la request: {str(e)}")
            raise
    
    def validate_response_success(self, response: requests.Response) -> bool:
        """
        Valida que la respuesta sea exitosa
        
        Args:
            response (requests.Response): Respuesta de la API
            
        Returns:
            bool: True si la respuesta es exitosa
        """
        is_success = response.status_code in [200, 201, 202]
        logger.info(f"Validación de respuesta exitosa: {is_success}")
        return is_success
    
    def validate_response_error(self, response: requests.Response, expected_status: int = 400) -> bool:
        """
        Valida que la respuesta contenga un error esperado
        
        Args:
            response (requests.Response): Respuesta de la API
            expected_status (int): Código de estado esperado
            
        Returns:
            bool: True si la respuesta contiene el error esperado
        """
        is_error = response.status_code == expected_status
        logger.info(f"Validación de error esperado ({expected_status}): {is_error}")
        return is_error
    
    def get_response_data(self, response: requests.Response) -> Optional[Dict[str, Any]]:
        """
        Extrae los datos de la respuesta JSON
        
        Args:
            response (requests.Response): Respuesta de la API
            
        Returns:
            Optional[Dict[str, Any]]: Datos de la respuesta o None si no es JSON válido
        """
        try:
            return response.json()
        except (json.JSONDecodeError, ValueError):
            logger.warning("La respuesta no contiene JSON válido")
            return None 