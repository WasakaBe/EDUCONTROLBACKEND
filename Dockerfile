# Usa una imagen base de Python
FROM python:3.9-slim

# Actualiza el sistema e instala los paquetes necesarios
RUN apt-get update && \
    apt-get install -y curl gnupg && \
    curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql17 unixodbc-dev

# Establece el directorio de trabajo
WORKDIR /app

# Crear un entorno virtual para aislar las dependencias
RUN python -m venv /opt/venv

# Activa el entorno virtual e instala dependencias
ENV PATH="/opt/venv/bin:$PATH"
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copia el código de la aplicación al contenedor
COPY . .

# Expone el puerto en el que se ejecutará la aplicación Flask
EXPOSE 50023

# Comando para ejecutar la aplicación con Gunicorn
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:50023"]
