# 🚀 Framework de Automatización de API

[![CI](https://github.com/tu-usuario/tu-repo/workflows/API%20Automation%20Tests%20CI/badge.svg)](https://github.com/tu-usuario/tu-repo/actions)
[![Docker](https://img.shields.io/badge/docker-ready-blue)](https://hub.docker.com/)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/)
[![pytest](https://img.shields.io/badge/testing-pytest-green)](https://docs.pytest.org/)

## Descripción
Framework profesional de automatización de pruebas para APIs REST utilizando pytest, Docker y CI/CD. Implementa el patrón Page Object Model (POM) con cobertura completa de pruebas, reportes automáticos y pipeline de integración continua.

## Estructura del Proyecto
```
api_test_challenge/
├── tests/
│   ├── test_import.py      # Pruebas principales (happy path y sad path)
│   ├── test_import_2.py    # Pruebas avanzadas
│   └── __init__.py
├── pages/
│   ├── import_api.py       # Modelo POM para API testing
│   └── __init__.py
├── conftest.py             # Configuración y fixtures de pytest
└── __init__.py
requirements.txt            # Dependencias del proyecto
pytest.ini                  # Configuración de pytest
README.md                   # Este archivo
```

## Requisitos
- Python 3.8+
- pytest
- requests

## 🚀 Inicio Rápido

### Opción 1: Usando Docker (Recomendado)
```bash
# Ejecutar tests directamente
make docker-test

# O usando docker-compose
docker-compose up pytest-tests
```

### Opción 2: Instalación Local
```bash
# Instalar dependencias
make install

# Ejecutar tests
make test
```

## 📋 Comandos Disponibles

### Usando Makefile (Recomendado)
```bash
make help          # Ver todos los comandos disponibles
make test           # Ejecutar tests básicos
make test-coverage  # Ejecutar tests con cobertura
make test-html      # Generar reporte HTML
make docker-test    # Ejecutar en Docker
make lint           # Linting del código
make clean          # Limpiar archivos temporales
```

## 🧪 Ejecución de Pruebas

### Ejecutar todas las pruebas:
```bash
pytest
```

### Ejecutar solo el archivo principal de pruebas:
```bash
pytest api_test_challenge/tests/test_import.py
```

### Ejecutar con mayor verbosidad:
```bash
pytest -v
```

### Ejecutar con reporte HTML:
```bash
pytest --html=reports/report.html --self-contained-html
```

### Con cobertura de código:
```bash
pytest --cov=api_test_challenge --cov-report=html:reports/htmlcov
```

## 🐳 Docker

### Ejecutar tests en contenedor:
```bash
# Construir imagen
docker build -t api-automation-tests .

# Ejecutar tests
docker run --rm -v $(pwd)/reports:/app/reports api-automation-tests
```

### Desarrollo con Docker:
```bash
# Entorno interactivo
docker-compose up pytest-dev
```

## 🔄 CI/CD

Este proyecto incluye configuración completa de GitHub Actions que:

- ✅ Ejecuta tests en múltiples versiones de Python (3.9, 3.10, 3.11)
- ✅ Genera reportes HTML y de cobertura
- ✅ Ejecuta tests en Docker
- ✅ Escaneo de seguridad con Trivy
- ✅ Publica resultados automáticamente
- ✅ Ejecuta tests diariamente

### Ejecutar pruebas específicas:
```bash
# Solo happy path
pytest -k "happy_path"

# Solo sad path
pytest -k "sad_path"

# Excluir pruebas lentas
pytest -m "not slow"
```

## Características Implementadas

### ✅ Requisitos Cumplidos
- **Framework pytest**: Utilizado correctamente con fixtures y parametrización
- **Patrón POM**: Implementado en `pages/import_api.py` para separar la lógica de API
- **personId dinámico**: Parametrizado usando fixtures en `conftest.py`
- **Manejo de errores**: Implementado con try/catch y validaciones de respuesta
- **Código ejecutable**: Funciona directamente con `pytest test_import.py`

### 🚀 Funcionalidades Adicionales
- **Logging detallado**: Registro completo de requests y responses
- **Validación de estructura**: Verificación de headers y códigos de estado
- **Pruebas parametrizadas**: Múltiples scenarios con diferentes person_id
- **Validación de tiempo de respuesta**: Control de performance
- **Pruebas de autenticación**: Verificación de seguridad
- **Separación de responsabilidades**: Código limpio y mantenible

## Casos de Prueba Implementados

### Happy Path 🟢
- `test_import_person_happy_path`: Importación exitosa básica
- `test_import_person_with_different_valid_ids`: Pruebas parametrizadas con IDs válidos
- `test_import_person_response_structure`: Validación de estructura de respuesta

### Sad Path 🔴
- `test_import_person_sad_path_invalid_person_id`: ID inválido
- `test_import_person_sad_path_missing_person_id`: Payload sin personId
- `test_import_person_sad_path_empty_payload`: Payload vacío
- `test_import_person_sad_path_invalid_data_type`: Tipo de dato incorrecto
- `test_import_person_authentication_required`: Sin autenticación

### Pruebas Avanzadas 🔧
- `test_import_person_response_time`: Validación de performance
- `test_import_person_multiple_persons_payload`: Múltiples personas
- `test_import_person_database_validation`: Validación de DB (marcada como skip)

## Configuración de la API

### Endpoint
```
POST https://api.test.worldsys.ar/import
```

### Headers
```json
{
    "Content-Type": "application/json",
    "Authorization": "Bearer xxx"
}
```

### Payload de Ejemplo
```json
[
    {
        "personId": 111
    }
]
```

## Personalización

### Cambiar configuración de API
Modificar los parámetros en `pages/import_api.py`:
```python
api = ImportAPI(
    base_url="https://tu-api.com",
    auth_token="tu-token"
)
```

### Agregar nuevos person_id para pruebas
Modificar las fixtures en `conftest.py`:
```python
@pytest.fixture(params=[111, 222, 333, 444])  # Agregar más IDs
def valid_person_id(request):
    return request.param
```

## Validación de Base de Datos

Para habilitar la validación de base de datos, descomentar y configurar la prueba:
```python
# Query sugerida: SELECT DISTINCT * FROM Test.Worldsys WHERE personId = 111
```

## Reportes

El proyecto genera logs detallados y soporta reportes HTML para análisis de resultados.
