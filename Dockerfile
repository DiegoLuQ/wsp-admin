# Usa una imagen de Python como base
FROM python:3.9-slim-buster

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos de la aplicación y los requisitos al contenedor
COPY ./app/requirements.txt ./app/requirements.txt

COPY ./app /app/
# Instala las dependencias de Python
RUN pip install --no-cache-dir --upgrade -r ./app/requirements.txt

# Instala las dependencias de Python y las bibliotecas requeridas por Chrome
RUN apt-get update && apt-get install -y wget \
    && wget -P ./ https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && mkdir -p /opt/google/chrome \
    && dpkg -x ./google-chrome-stable_current_amd64.deb /opt/google/chrome \
    && rm ./google-chrome-stable_current_amd64.deb \
    && apt-get install -y libglib2.0-0 libnss3 \
    && apt-get clean

# Agregar la ruta del ejecutable de Chrome al PATH
ENV PATH="/opt/google/chrome/opt/google/chrome:${PATH}"