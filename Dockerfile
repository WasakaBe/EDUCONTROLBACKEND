# Usa una imagen de Microsoft que ya contiene los controladores de SQL Server
FROM mcr.microsoft.com/azure-sql-edge:latest

# Instala Python y otras dependencias de sistema
RUN apt-get update && \
    apt-get install -y python3 python3-pip unixodbc-dev

# Instala las dependencias de Python
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Copia el código del backend
COPY . .

# Expone el puerto
EXPOSE 50023

# Comando para ejecutar la aplicación
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:50023"]
