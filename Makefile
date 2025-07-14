# Variables
PYTHON := python3
PIP := pip3
DOCKER_IMAGE := api-automation-tests
DOCKER_CONTAINER := api-automation-container

# Colores para output
RED := \033[0;31m
GREEN := \033[0;32m
YELLOW := \033[1;33m
BLUE := \033[0;34m
NC := \033[0m # No Color

.PHONY: help install test test-verbose test-html test-coverage clean docker-build docker-run docker-test lint format setup-dev

# Ayuda por defecto
help:
	@echo "$(BLUE)API Automation Testing Framework$(NC)"
	@echo "$(YELLOW)Comandos disponibles:$(NC)"
	@echo "  $(GREEN)install$(NC)      - Instalar dependencias"
	@echo "  $(GREEN)test$(NC)         - Ejecutar tests básicos"
	@echo "  $(GREEN)test-mocked$(NC)  - Ejecutar solo tests mockeados (sin conexión real)"
	@echo "  $(GREEN)test-real$(NC)    - Ejecutar solo tests con API real"
	@echo "  $(GREEN)test-verbose$(NC) - Ejecutar tests con output detallado"
	@echo "  $(GREEN)test-html$(NC)    - Ejecutar tests y generar reporte HTML"
	@echo "  $(GREEN)test-coverage$(NC)- Ejecutar tests con cobertura"
	@echo "  $(GREEN)test-database$(NC) - Ejecutar tests de base de datos (requiere DB_*)"
	@echo "  $(GREEN)test-database-mocked$(NC) - Ejecutar tests mockeados de DB"
	@echo "  $(GREEN)test-full$(NC)    - Ejecutar suite completa (API + DB reales)"
	@echo "  $(GREEN)test-mocked-all$(NC) - Ejecutar todos los tests mockeados"
	@echo "  $(GREEN)lint$(NC)         - Ejecutar linting"
	@echo "  $(GREEN)format$(NC)       - Formatear código"
	@echo "  $(GREEN)clean$(NC)        - Limpiar archivos temporales"
	@echo "  $(GREEN)docker-build$(NC) - Construir imagen Docker"
	@echo "  $(GREEN)docker-run$(NC)   - Ejecutar tests en Docker"
	@echo "  $(GREEN)docker-test$(NC)  - Construir imagen y ejecutar tests"
	@echo "  $(GREEN)setup-dev$(NC)    - Configurar entorno de desarrollo"

# Instalar dependencias
install:
	@echo "$(YELLOW)Instalando dependencias...$(NC)"
	$(PIP) install -r requirements.txt
	$(PIP) install pytest-cov pytest-html pytest-xdist flake8 black isort

# Ejecutar tests básicos
test:
	@echo "$(YELLOW)Ejecutando tests...$(NC)"
	$(PYTHON) -m pytest -v

# Ejecutar solo tests mockeados (no requieren conexión real)
test-mocked:
	@echo "$(YELLOW)Ejecutando solo tests mockeados...$(NC)"
	$(PYTHON) -m pytest -v -m "mocked"

# Ejecutar solo tests con API real (requieren conexión)
test-real:
	@echo "$(YELLOW)Ejecutando tests con API real...$(NC)"
	$(PYTHON) -m pytest -v -m "real_api" --tb=short

# Ejecutar tests con output detallado
test-verbose:
	@echo "$(YELLOW)Ejecutando tests con output detallado...$(NC)"
	$(PYTHON) -m pytest -v -s --tb=short

# Ejecutar solo tests de base de datos (requieren configuración DB_*)
test-database:
	@echo "$(YELLOW)Ejecutando tests de base de datos...$(NC)"
	@echo "$(BLUE)Nota: Requiere variables de entorno DB_SERVER, DB_NAME, DB_USER, DB_PASSWORD$(NC)"
	$(PYTHON) -m pytest -v -m "database" --tb=short

# Ejecutar solo tests mockeados de base de datos
test-database-mocked:
	@echo "$(YELLOW)Ejecutando tests mockeados de base de datos...$(NC)"
	$(PYTHON) -m pytest -v -m "mocked_database"

# Ejecutar todos los tests (API + DB) con configuración real
test-full:
	@echo "$(YELLOW)Ejecutando suite completa de tests...$(NC)"
	@echo "$(BLUE)Incluye: API real + Base de datos real$(NC)"
	$(PYTHON) -m pytest -v -m "real_api or database" --tb=short

# Ejecutar todos los tests mockeados (para demos/CI)
test-mocked-all:
	@echo "$(YELLOW)Ejecutando todos los tests mockeados...$(NC)"
	@echo "$(BLUE)Incluye: API mockeada + Base de datos mockeada$(NC)"
	$(PYTHON) -m pytest -v -m "mocked or mocked_database"

# Ejecutar tests y generar reporte HTML
test-html:
	@echo "$(YELLOW)Ejecutando tests y generando reporte HTML...$(NC)"
	mkdir -p reports
	$(PYTHON) -m pytest -v \
		--html=reports/report.html \
		--self-contained-html \
		--junitxml=reports/junit.xml

# Ejecutar tests con cobertura
test-coverage:
	@echo "$(YELLOW)Ejecutando tests con cobertura...$(NC)"
	mkdir -p reports
	$(PYTHON) -m pytest -v \
		--cov=api_test_challenge \
		--cov-report=html:reports/htmlcov \
		--cov-report=xml:reports/coverage.xml \
		--cov-report=term-missing \
		--html=reports/report.html \
		--self-contained-html

# Linting
lint:
	@echo "$(YELLOW)Ejecutando linting...$(NC)"
	flake8 api_test_challenge/ --max-line-length=127
	@echo "$(GREEN)Linting completado$(NC)"

# Formatear código
format:
	@echo "$(YELLOW)Formateando código...$(NC)"
	black api_test_challenge/
	isort api_test_challenge/
	@echo "$(GREEN)Formateo completado$(NC)"

# Limpiar archivos temporales
clean:
	@echo "$(YELLOW)Limpiando archivos temporales...$(NC)"
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf reports/
	@echo "$(GREEN)Limpieza completada$(NC)"

# Construir imagen Docker
docker-build:
	@echo "$(YELLOW)Construyendo imagen Docker...$(NC)"
	docker build -t $(DOCKER_IMAGE) .
	@echo "$(GREEN)Imagen Docker construida: $(DOCKER_IMAGE)$(NC)"

# Ejecutar tests en Docker
docker-run:
	@echo "$(YELLOW)Ejecutando tests en Docker...$(NC)"
	mkdir -p reports
	docker run --rm \
		-v $(PWD)/reports:/app/reports \
		$(DOCKER_IMAGE)

# Construir y ejecutar tests en Docker
docker-test: docker-build docker-run

# Ejecutar con docker-compose
compose-test:
	@echo "$(YELLOW)Ejecutando tests con docker-compose...$(NC)"
	docker-compose up --build pytest-tests

# Configurar entorno de desarrollo
setup-dev: install
	@echo "$(YELLOW)Configurando entorno de desarrollo...$(NC)"
	$(PIP) install pre-commit
	pre-commit install
	@echo "$(GREEN)Entorno de desarrollo configurado$(NC)"

# Ejecutar todos los checks (CI local)
ci-check: lint test-coverage
	@echo "$(GREEN)Todos los checks de CI completados$(NC)" 