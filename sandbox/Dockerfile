FROM dorowu/ubuntu-desktop-lxde-vnc

WORKDIR /sandbox
COPY . .
RUN sudo apt install dpkg
RUN sudo apt -y install gnome-screenshot
RUN sudo dpkg -i ./DEBS/*.deb