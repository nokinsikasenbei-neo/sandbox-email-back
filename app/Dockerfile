FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

RUN adduser --disabled-password --gecos "" app

WORKDIR /app
COPY . .

RUN chown -R root:app .
RUN pip install -r requirements.txt

USER app