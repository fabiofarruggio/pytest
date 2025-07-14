# 🗄️ Framework de Testing con Base de Datos

## 📋 Descripción

Este framework incluye capacidades avanzadas de testing con base de datos que demuestran:

- **Configuración parametrizable** via variables de entorno
- **Tests reales vs mockeados** según disponibilidad de DB
- **Soporte multi-DB** (SQL Server, PostgreSQL, MySQL)
- **Validaciones de integridad** API ↔ Base de datos
- **Manejo robusto de errores** y conectividad

## 🔧 Configuración de Base de Datos

### Variables de Entorno Requeridas

Para ejecutar tests reales de base de datos, configurar las siguientes variables:

```bash
# Configuración obligatoria
export DB_SERVER="tu-servidor.database.windows.net"
export DB_NAME="tu_base_datos"
export DB_USER="tu_usuario"
export DB_PASSWORD="tu_password"

# Configuración opcional
export DB_PORT="1433"                              # Puerto (por defecto 1433 para SQL Server)
export DB_DRIVER="ODBC Driver 17 for SQL Server"  # Driver ODBC
```

### Ejemplo de Configuración

#### SQL Server (Azure SQL Database)
```bash
export DB_SERVER="myserver.database.windows.net"
export DB_NAME="TestDatabase"
export DB_USER="testuser"
export DB_PASSWORD="MySecurePassword123!"
export DB_PORT="1433"
```

#### SQL Server (Local)
```bash
export DB_SERVER="localhost"
export DB_NAME="TestDB"
export DB_USER="sa"
export DB_PASSWORD="YourPassword123"
export DB_PORT="1433"
```

## 🏗️ Estructura del Framework

### Archivos Principales

```
api_test_challenge/
├── database_config.py           # Configuración y manejo de DB
├── conftest.py                  # Fixtures de DB para pytest
├── pages/import_api.py          # Métodos de validación DB en ImportAPI
└── tests/
    ├── test_import_2.py         # Tests de integración API + DB
    ├── test_database_mocked.py  # Tests mockeados de DB
    └── ...
```

### Componentes Clave

#### 1. `DatabaseConfig` (database_config.py)
```python
from api_test_challenge.database_config import db_config

# Verificar configuración
if db_config.is_configured:
    print("✅ Base de datos configurada")
    
    if db_config.is_available:
        print("✅ Base de datos disponible")
    else:
        print("⚠️  Base de datos no disponible")
else:
    print("❌ Base de datos no configurada")
```

#### 2. Fixtures de Pytest (conftest.py)
```python
# Fixtures disponibles
def test_example(db_config, database_available, import_api_with_db):
    if not database_available:
        pytest.skip("DB no configurada")
    
    # Usar import_api_with_db para tests con DB
    result = import_api_with_db.validate_person_in_database(111)
```

#### 3. Métodos de ImportAPI
```python
api = ImportAPI()

# Validar existencia en DB
exists = api.validate_person_in_database(111)

# Obtener datos completos
person_data = api.get_person_from_database(111)

# Ejecutar query personalizada
results = api.execute_db_query(
    "SELECT * FROM Test.Worldsys WHERE personId = :id",
    {"id": 111}
)
```

## 🧪 Comandos de Testing

### Tests de Base de Datos

```bash
# Tests mockeados de DB (siempre pasan - para demos)
make test-database-mocked

# Tests reales de DB (requieren configuración)
make test-database

# Suite completa (API + DB reales)
make test-full

# Todos los tests mockeados (API + DB)
make test-mocked-all
```

### Ejecución Directa con pytest

```bash
# Solo tests de DB con configuración real
pytest -v -m "database"

# Solo tests mockeados de DB
pytest -v -m "mocked_database"

# Tests reales (API + DB) con configuración
pytest -v -m "real_api or database"

# Todos los tests mockeados
pytest -v -m "mocked or mocked_database"
```

## 📊 Tipos de Tests

### 1. Tests Reales de Base de Datos
- Requieren configuración via variables `DB_*`
- Se conectan a base de datos real
- Ejecutan queries reales: `SELECT DISTINCT * FROM Test.Worldsys WHERE personId = ?`
- Se **skippean automáticamente** si no hay configuración

### 2. Tests Mockeados de Base de Datos
- **Siempre pasan** (perfectos para demos y CI)
- Simulan todas las operaciones de DB
- No requieren configuración real
- Demuestran capacidades del framework

### 3. Tests de Integración API + DB
- Validan consistencia entre API y base de datos
- Flujo completo: Import via API → Validar en DB
- Detectan inconsistencias de datos

## 🎯 Casos de Uso Demostrados

### Validación de Importación
```python
@pytest.mark.database
def test_import_and_validate_in_db(import_api_with_db, database_available):
    if not database_available:
        pytest.skip("DB no configurada")
    
    # 1. Importar via API
    response = import_api_with_db.import_person(111)
    
    # 2. Validar respuesta API
    assert response.status_code == 200
    
    # 3. Validar en base de datos
    exists = import_api_with_db.validate_person_in_database(111)
    assert exists is True
    
    # 4. Obtener y validar datos
    person_data = import_api_with_db.get_person_from_database(111)
    assert person_data["personId"] == 111
```

### Query Personalizada
```python
@pytest.mark.database
def test_custom_database_query(import_api_with_db, database_available):
    if not database_available:
        pytest.skip("DB no configurada")
    
    # Query con parámetros
    query = """
    SELECT personId, firstName, lastName 
    FROM Test.Worldsys 
    WHERE personId IN (:id1, :id2, :id3)
    ORDER BY personId
    """
    
    results = import_api_with_db.execute_db_query(query, {
        "id1": 111,
        "id2": 222, 
        "id3": 333
    })
    
    assert results is not None
    assert len(results) > 0
```

### Validación de Estructura de Tabla
```python
@pytest.mark.database
def test_table_structure(import_api_with_db, database_available):
    if not database_available:
        pytest.skip("DB no configurada")
    
    # Obtener estructura de tabla
    structure_query = """
    SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE
    FROM INFORMATION_SCHEMA.COLUMNS 
    WHERE TABLE_SCHEMA = 'Test' AND TABLE_NAME = 'Worldsys'
    """
    
    columns = import_api_with_db.execute_db_query(structure_query)
    column_names = [col[0] for col in columns]
    
    assert 'personId' in column_names
```

## 🛡️ Manejo de Errores

### Configuración No Disponible
```python
# El framework detecta automáticamente:
if not db_config.is_configured:
    pytest.skip("⚠️  Variables de entorno DB_* no configuradas")
    
# O para métodos específicos:
if not api.validate_person_in_database(111):
    # Retorna False si DB no está configurada
```

### Conexión Fallida
```python
# Test de conectividad
try:
    result = db_config.execute_query("SELECT 1")
    print("✅ Conectividad exitosa")
except Exception as e:
    print(f"❌ Error de conectividad: {e}")
```

### Queries Inválidas
```python
# Manejo de errores SQL
try:
    result = api.execute_db_query("SELECT * FROM NonExistentTable")
except Exception as e:
    print(f"❌ Error en query: {e}")
    # El framework maneja gracefully y retorna None
```

## 📈 Resultados Esperados

### Con Configuración de DB ✅
```bash
$ make test-database

=== TESTS DE BASE DE DATOS ===
✅ test_database_connectivity - PASSED
✅ test_validate_person_exists_in_database - PASSED  
✅ test_get_person_data_success - PASSED
✅ test_table_structure_validation - PASSED

4 passed, 0 skipped
```

### Sin Configuración de DB ⚠️
```bash
$ make test-database

=== TESTS DE BASE DE DATOS ===
⚠️  test_database_connectivity - SKIPPED (DB no configurada)
⚠️  test_validate_person_exists_in_database - SKIPPED (DB no configurada)
⚠️  test_get_person_data_success - SKIPPED (DB no configurada)
⚠️  test_table_structure_validation - SKIPPED (DB no configurada)

0 passed, 4 skipped
```

### Tests Mockeados (Siempre) ✅
```bash
$ make test-database-mocked

=== TESTS MOCKEADOS DE BASE DE DATOS ===
✅ test_database_connectivity_success - PASSED
✅ test_validate_person_exists_success - PASSED
✅ test_get_person_data_success - PASSED
✅ test_complex_database_query - PASSED

8 passed, 0 skipped
```

## 🔐 Dependencias

### Paquetes Requeridos
```txt
# Base de datos (incluidas en requirements.txt)
SQLAlchemy==2.0.21    # ORM y engine de DB
pyodbc==4.0.39        # Driver ODBC para SQL Server
pymssql==2.2.8        # Driver alternativo para SQL Server
```

### Instalación
```bash
# Instalar todas las dependencias
make install

# O manualmente
pip install -r requirements.txt
```

## 🎪 Demo y Presentación

Para **demostraciones** y **portfolios profesionales**:

1. **Usar tests mockeados** que siempre pasan:
   ```bash
   make test-mocked-all
   ```

2. **Mostrar configuración** de variables de entorno

3. **Ejecutar con DB real** si está disponible:
   ```bash
   # Configurar variables
   export DB_SERVER="..."
   export DB_NAME="..."
   export DB_USER="..."
   export DB_PASSWORD="..."
   
   # Ejecutar tests reales
   make test-database
   ```

4. **Demostrar skip automático** cuando no hay configuración

## 🏆 Valor Técnico Demostrado

Este framework demuestra conocimientos en:

- **✅ Arquitectura de testing enterprise-grade**
- **✅ Configuración parametrizable y flexible**
- **✅ Manejo robusto de dependencias externas**
- **✅ Tests duales (reales vs mockeados)**
- **✅ Integración API ↔ Base de datos**
- **✅ Validaciones de integridad de datos**
- **✅ Manejo profesional de errores**
- **✅ Documentación técnica completa**
- **✅ Soporte multi-base de datos**
- **✅ CI/CD ready con skip automático** 