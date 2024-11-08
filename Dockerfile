# Usa una imagen base de Python
FROM python:3.9

# Instala dependencias de sistema
RUN apt-get update && \
    apt-get install -y curl apt-transport-https gnupg && \
    curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql18 unixodbc-dev && \
    apt-get clean -y

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos de la aplicación
COPY . .

# Instala las dependencias de Python
RUN pip install -r requirements.txt

# Expone el puerto de la aplicación Flask
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
