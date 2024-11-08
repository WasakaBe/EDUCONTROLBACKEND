FROM python:3.9-slim

RUN pip install --upgrade pip setuptools
RUN apt-get update && \
    apt-get install -y curl gnupg unixodbc-dev build-essential && \
    curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql18 unixodbc-dev

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 50023
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:50023"]
