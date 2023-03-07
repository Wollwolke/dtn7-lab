#!/bin/bash

systemctl enable ssh
service ssh start

# copy mounted services into container
DIR="/tmp/shared/custom_services"
if [ -d "$DIR" ]; then  
  cp $DIR/* /root/.core/myservices
fi

# update custom core service only on first startup
ALREADY_STARTED="/tmp/already_started"
if [ ! -e $ALREADY_STARTED ]; then
    touch $ALREADY_STARTED
    /update-custom-services.sh
fi

#service core-daemon start
if test -e "/tmp/pycore.1"; then
    rm -r /tmp/pycore.1
fi


core-daemon > /var/log/core-daemon.log 2>&1 &

iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE

if [ ! -z "$SSHKEY" ]; then
    echo "Adding ssh key: $SSHKEY"
    mkdir /root/.ssh
    chmod 755 ~/.ssh
    echo $SSHKEY > /root/.ssh/authorized_keys
    chmod 644 /root/.ssh/authorized_keys
fi

echo "source /opt/ros/humble/install/setup.bash" >> ~/.bashrc

if [ -n "$1" ]; then
    if [ -f "$1" ]; then
        echo "$1 exists."
        sleep 1
        time core-experiment $1 2>&1 | tee /shared/experiment.log
        exit 0
    fi
fi

echo "$1"

core-pygui



