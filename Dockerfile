FROM python:3.9-slim

# Instala solo el driver ODBC y sus dependencias
RUN apt-get update && \
    apt-get install -y curl gnupg apt-transport-https ca-certificates && \
    curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql17 unixodbc-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Variables de entorno para ODBC
ENV LD_LIBRARY_PATH=/opt/microsoft/msodbcsql17/lib64:$LD_LIBRARY_PATH

# Instala las dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código del backend
COPY . .

# Expone el puerto
EXPOSE 50023

# Comando para ejecutar la aplicación
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:50023"]
