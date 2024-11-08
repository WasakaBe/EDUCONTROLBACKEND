# Usa una imagen base de Python
FROM python:3.9-slim

# Instala el controlador ODBC para SQL Server
RUN apt-get update && \
    apt-get install -y curl gnupg unixodbc-dev && \
    curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql18 && \
    apt-get clean

# Instala las dependencias de Python
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copia el código del backend
COPY . .

# Expone el puerto
EXPOSE 50023

# Comando para ejecutar la aplicación
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:50023"]
