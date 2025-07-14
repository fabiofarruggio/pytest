# Usar Python 3.11 slim como base
FROM python:3.11-slim

# Establecer variables de entorno
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Crear usuario no-root para seguridad
RUN groupadd -r testuser && useradd -r -g testuser testuser

# Establecer directorio de trabajo
WORKDIR /app

# Copiar requirements primero para aprovechar cache de Docker
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código del proyecto
COPY . .

# Cambiar propiedad de archivos al usuario no-root
RUN chown -R testuser:testuser /app

# Cambiar a usuario no-root
USER testuser

# Crear directorio para reportes en /tmp (siempre escribible)
RUN mkdir -p /tmp/reports

# Comando por defecto para ejecutar tests
CMD ["pytest", "-v", "--html=/tmp/reports/report.html", "--self-contained-html", "--junitxml=/tmp/reports/junit.xml"] 