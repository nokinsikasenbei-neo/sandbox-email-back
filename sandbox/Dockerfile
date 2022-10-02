FROM dorowu/ubuntu-desktop-lxde-vnc

WORKDIR /sandbox
COPY . .
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 4EB27DB2A3B88B8B
RUN apt-get update
RUN apt-get install -y python3 python3-pip
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN apt install dpkg
RUN dpkg -i ./DEBS/*.deb
RUN pip install -r requirements.txt