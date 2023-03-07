#!/bin/bash

SHARED="/tmp/shared"
EXPERIMENT=""

if [ -n "$1" ]; then
    SHARED=$(readlink -f $1)
    echo Using custom shared directory: $SHARED
else
    echo Using default shared directory: $SHARED
    mkdir -p $SHARED
fi

if [ -n "$2" ]; then
    if [ "$2" = "-i" ]; then
        INTERACTIVE="--entrypoint /bin/bash"
    else
        # do experiment
        INTERACTIVE="--entrypoint /shared/entrypoint.sh"
        EXPERIMENT=$2
    fi
else
    INTERACTIVE="--entrypoint /shared/entrypoint.sh"
fi

if ! lsmod | grep -q -e sch_netem -e ebtables; then
    echo "neither sch_netem nor ebables kernel modules are not loaded"
    echo "try running sudo modprobe -a sch_netem ebtables"
    sudo modprobe -a ebtables
fi

xhost +local:root
# docker run -it \
podman run -it --rm \
    --name clab \
    -p 2000:22 \
    -p 51051:50051 \
    -p 8765:8765 \
    --cap-add=NET_ADMIN \
    --cap-add=SYS_ADMIN \
    -e SSHKEY="$(ssh-add -L)" \
    -e DISPLAY \
    -v $SHARED:/shared \
    -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
    -v ~/Documents/mt/ros_ws/:/tmp/shared/ros_ws/ \
    -v ~/Documents/mt/clab/custom_services/:/tmp/shared/custom_services \
    -v ~/Documents/mt/bags:/shared/bags \
    --privileged \
    $INTERACTIVE \
    wollwolke/clab-ros \
    $EXPERIMENT
