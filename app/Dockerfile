FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

# RUN adduser --disabled-password --gecos "" app

WORKDIR /app
COPY . .

RUN mkdir -p /var/public && \
    mkdir -p /var/public/attached && \
    mkdir -p /var/public/converted && \
    chmod -R 771 /var/public && \
    pip install -r requirements.txt

# USER app