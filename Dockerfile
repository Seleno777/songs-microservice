# Imagen base oficial con Python
FROM python:3.12

# Evitar preguntas al instalar paquetes
ENV DEBIAN_FRONTEND=noninteractive

# Instalar dependencias del sistema para ODBC
RUN apt-get update && \
    apt-get install -y gnupg curl unixodbc-dev gcc g++ apt-transport-https && \
    curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql17 && \
    apt-get clean

# Crear directorio de trabajo
WORKDIR /app

# Copiar archivos
COPY . .

# Asegurar permisos de ejecución en el script de arranque
RUN chmod +x startup.sh

# Instalar dependencias de Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Exponer puerto para Azure
EXPOSE 8000

# Script de arranque
CMD ["bash", "startup.sh"]
