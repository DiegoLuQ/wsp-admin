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
    # && apt-get install -y libglib2.0-0 libnss3 libdbus-1-3 \
    && apt-get update && apt-get install -y \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libatspi2.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libgtk-3-0 \
#    libgtk-4-1 \
    libnspr4 \
    libnss3 \
    libwayland-client0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxkbcommon0 \
    libxrandr2 \
    xdg-utils \
    libu2f-udev \
    libvulkan1 \
    && apt-get clean

# Agregar la ruta del ejecutable de Chrome al PATH
ENV PATH="/opt/google/chrome/opt/google/chrome:${PATH}"