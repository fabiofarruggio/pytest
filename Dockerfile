# Usar Python 3.11 slim como base
FROM python:3.11-slim

# Establecer variables de entorno
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Establecer directorio de trabajo
WORKDIR /app

# Copiar requirements primero para aprovechar cache de Docker
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código del proyecto
COPY . .

# Crear directorio para reportes
RUN mkdir -p /app/reports

# Comando por defecto para ejecutar tests
CMD ["pytest", "-v", "--html=reports/report.html", "--self-contained-html", "--junitxml=reports/junit.xml"] 