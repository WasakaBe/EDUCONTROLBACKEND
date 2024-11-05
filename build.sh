#!/usr/bin/env bash
set -x

# Instalar el driver ODBC 17 para SQL Server
apt-get update && apt-get install -y curl apt-transport-https
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
curl https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/prod.list > /etc/apt/sources.list.d/mssql-release.list
apt-get update
ACCEPT_EULA=Y apt-get install -y msodbcsql17

# Paquetes adicionales
apt-get install -y unixodbc-dev
