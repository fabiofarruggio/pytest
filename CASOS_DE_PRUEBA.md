# 📋 Documentación de Casos de Prueba

## 🎯 Resumen General

Este documento detalla cada uno de los 16 casos de prueba implementados en el framework de automatización de API, organizados por categorías y con descripción completa de cada escenario.

## 📊 Distribución de Casos de Prueba

- **Happy Path (Casos Exitosos)**: 3 casos
- **Sad Path (Casos de Error)**: 5 casos  
- **Pruebas Avanzadas**: 8 casos
- **Total**: 16 casos de prueba

---

## 🟢 HAPPY PATH - Casos Exitosos

### 1. `test_import_person_happy_path`
**Archivo:** `test_import.py`  
**Descripción:** Prueba básica de importación exitosa de una persona  
**Objetivo:** Validar el flujo principal de importación con un personId válido

**Configuración:**
- personId: 111 (valor fijo)
- Endpoint: POST /import
- Headers: Content-Type, Authorization

**Validaciones:**
- Código de respuesta: 200, 201 o 202
- Logging de request y response
- Manejo de errores de conexión

**Resultado esperado:** Importación exitosa

---

### 2. `test_import_person_with_different_valid_ids`
**Archivo:** `test_import.py`  
**Descripción:** Prueba parametrizada con múltiples personId válidos  
**Objetivo:** Validar que el sistema funciona con diferentes IDs válidos

**Configuración:**
- personId: 111, 222, 333 (parametrizado)
- Fixture: `valid_person_id`
- Ejecuta 3 veces (una por cada ID)

**Validaciones:**
- Código de respuesta exitoso para cada ID
- Estructura de respuesta JSON
- Logging detallado por cada ejecución

**Resultado esperado:** Todas las importaciones exitosas

---

### 3. `test_import_person_response_structure`
**Archivo:** `test_import_2.py`  
**Descripción:** Validación de estructura de respuesta en caso exitoso  
**Objetivo:** Verificar que la respuesta tiene la estructura correcta

**Configuración:**
- personId: 111
- Validación de headers HTTP
- Análisis de estructura de respuesta

**Validaciones:**
- Presencia de header Content-Type
- Código de respuesta válido
- Formato de respuesta correcto

**Resultado esperado:** Respuesta con estructura válida

---

## 🔴 SAD PATH - Casos de Error

### 4. `test_import_person_sad_path_invalid_person_id`
**Archivo:** `test_import.py`  
**Descripción:** Prueba con personId inválido  
**Objetivo:** Validar manejo de errores para IDs inválidos

**Configuración:**
- personId: -1 (valor inválido)
- Mismo endpoint y headers

**Validaciones:**
- Código de respuesta: 400 (Bad Request)
- Mensaje de error apropiado
- Logging de error manejado

**Resultado esperado:** Error 400 controlado

---

### 5. `test_import_person_sad_path_missing_person_id`
**Archivo:** `test_import.py`  
**Descripción:** Prueba con payload sin personId  
**Objetivo:** Validar manejo cuando falta el campo requerido

**Configuración:**
- Payload: [{}] (objeto vacío)
- Campo personId ausente

**Validaciones:**
- Código de respuesta: 400
- Validación de campo requerido
- Manejo de payload incompleto

**Resultado esperado:** Error por campo faltante

---

### 6. `test_import_person_sad_path_empty_payload`
**Archivo:** `test_import.py`  
**Descripción:** Prueba con payload completamente vacío  
**Objetivo:** Validar manejo de payload vacío

**Configuración:**
- Payload: [] (array vacío)
- Sin datos para procesar

**Validaciones:**
- Código de respuesta: 400
- Manejo de array vacío
- Error de validación de datos

**Resultado esperado:** Error por payload vacío

---

### 7. `test_import_person_sad_path_invalid_data_type`
**Archivo:** `test_import.py`  
**Descripción:** Prueba con tipo de dato incorrecto para personId  
**Objetivo:** Validar validación de tipos de datos

**Configuración:**
- Payload: [{"personId": "invalid_string"}]
- personId como string en lugar de entero

**Validaciones:**
- Código de respuesta: 400
- Validación de tipo de dato
- Error de conversión

**Resultado esperado:** Error por tipo de dato incorrecto

---

### 8. `test_import_person_with_parametrized_invalid_ids`
**Archivo:** `test_import_2.py`  
**Descripción:** Prueba parametrizada con múltiples IDs inválidos  
**Objetivo:** Validar diferentes tipos de IDs inválidos

**Configuración:**
- personId: 0, -1, 999999 (parametrizado)
- Fixture: `invalid_person_id`
- Ejecuta 3 veces

**Validaciones:**
- Códigos de respuesta: 400 o 404
- Manejo diferenciado por tipo de error
- Logging específico por caso

**Resultado esperado:** Errores apropiados según el ID

---

## 🔧 PRUEBAS AVANZADAS

### 9. `test_import_person_response_time`
**Archivo:** `test_import_2.py`  
**Descripción:** Validación de tiempo de respuesta  
**Objetivo:** Verificar performance de la API

**Configuración:**
- personId: 111
- Límite máximo: 5 segundos
- Medición de elapsed time

**Validaciones:**
- Tiempo de respuesta < 5 segundos
- Logging de tiempo exacto
- Performance monitoring

**Resultado esperado:** Respuesta dentro del tiempo límite

---

### 10. `test_import_person_authentication_required`
**Archivo:** `test_import_2.py`  
**Descripción:** Validación de autenticación requerida  
**Objetivo:** Verificar seguridad del endpoint

**Configuración:**
- Sin token de autenticación (token vacío)
- personId: 111
- Headers sin Authorization

**Validaciones:**
- Código de respuesta: 401 (Unauthorized)
- Mensaje de error de autenticación
- Seguridad del endpoint

**Resultado esperado:** Error de autorización

---

### 11. `test_import_person_multiple_persons_payload`
**Archivo:** `test_import_2.py`  
**Descripción:** Prueba con múltiples personas en un payload  
**Objetivo:** Validar procesamiento de lotes

**Configuración:**
- Payload: [{"personId": 111}, {"personId": 222}, {"personId": 333}]
- Múltiples objetos en array

**Validaciones:**
- Códigos de respuesta: 200, 201 o 400
- Procesamiento de lotes
- Manejo de múltiples registros

**Resultado esperado:** Procesamiento adecuado del lote

---

### 12. `test_import_person_database_validation` (SKIP)
**Archivo:** `test_import_2.py`  
**Descripción:** Validación de inserción en base de datos  
**Objetivo:** Verificar persistencia de datos

**Configuración:**
- personId: 111
- Query sugerida: `SELECT DISTINCT * FROM Test.Worldsys WHERE personId = 111`
- Marcado como skip por configuración de DB

**Validaciones:**
- Respuesta exitosa de API
- Verificación en base de datos
- Integridad de datos

**Resultado esperado:** Datos persistidos correctamente

---

## 📈 Casos Adicionales (Parametrizados)

### 13-15. Casos parametrizados de `valid_person_id`
**Descripción:** Ejecuciones múltiples del caso #2 con diferentes IDs válidos  
**Parámetros:** 111, 222, 333  
**Total de ejecuciones:** 3

### 16-18. Casos parametrizados de `invalid_person_id`
**Descripción:** Ejecuciones múltiples del caso #8 con diferentes IDs inválidos  
**Parámetros:** 0, -1, 999999  
**Total de ejecuciones:** 3

