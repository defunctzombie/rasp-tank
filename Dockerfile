FROM ros:noetic-ros-core

RUN apt update
RUN apt install ros-noetic-rosbridge-suite -y
RUN apt install make g++ -y
RUN apt install python3-rpi.gpio -y

COPY build.sh /
COPY entrypoint.sh /

WORKDIR /workspace
COPY ./workspace /workspace

RUN "/build.sh"

# disable the evils of pycache litter everywhere
ENV PYTHONDONTWRITEBYTECODE 1

ENTRYPOINT ["/entrypoint.sh"]
CMD ["roslaunch", "launch", "rasptank.launch"]