#!/usr/bin/env python3
"""
Ejemplo de uso del framework de automatización de API
Este archivo demuestra cómo usar la clase ImportAPI directamente
en un entorno profesional
"""

import sys
import os

# Asegurar que el módulo esté en el path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from api_test_challenge.pages.import_api import ImportAPI

def main():
    """
    Función principal que demuestra el uso de la API
    """
    print("=== EJEMPLO DE USO DE LA API DE IMPORTACIÓN ===")
    
    # Crear instancia de la API
    api = ImportAPI()
    
    # Ejemplo 1: Happy Path
    print("\n1. Probando Happy Path...")
    try:
        response = api.import_person(111)
        is_success = api.validate_response_success(response)
        print(f"   ✅ Éxito: {is_success}")
        print(f"   Código de respuesta: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Ejemplo 2: Sad Path
    print("\n2. Probando Sad Path...")
    try:
        response = api.import_person(-1)
        is_error = api.validate_response_error(response, 400)
        print(f"   ✅ Error esperado: {is_error}")
        print(f"   Código de respuesta: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error inesperado: {e}")
    
    # Ejemplo 3: Payload inválido
    print("\n3. Probando payload inválido...")
    try:
        response = api.import_person_invalid_payload([])
        is_error = api.validate_response_error(response, 400)
        print(f"   ✅ Error esperado para payload vacío: {is_error}")
        print(f"   Código de respuesta: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error inesperado: {e}")
    
    print("\n=== EJEMPLO COMPLETADO ===")

if __name__ == "__main__":
    main() 