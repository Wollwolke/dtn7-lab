#!/bin/bash

systemctl enable ssh
service ssh start

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

core-pygui
