FROM dorowu/ubuntu-desktop-lxde-vnc

WORKDIR /sandbox
COPY . .
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 4EB27DB2A3B88B8B && \
    apt-get update && \
    apt-get install -y python3 python3-pip && \
    pip install --upgrade pip && \
    pip install --upgrade setuptools && \
    apt install dpkg && \
    dpkg -i ./DEBS/*.deb && \
    pip install -r requirements.txt

ENTRYPOINT [ "python3", "main.py" ]