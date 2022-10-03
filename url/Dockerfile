FROM tensorflow/tensorflow:2.8.2

RUN pip install pandas

WORKDIR /url
COPY . .
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    pip install --upgrade pip && \
    pip install --upgrade setuptools && \
    pip install -r requirements.txt

ENTRYPOINT [ "python3", "main.py" ]