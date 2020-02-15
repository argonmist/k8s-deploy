#!/bin/bash

FILE=haproxy-keepalived/$1
if [ -d "$FILE" ]; then
    export LC_ALL=C
    sudo firewall-cmd --add-port=6443/tcp --permanent
    sudo firewall-cmd --reload
    sudo cp $FILE/keepalived.conf /etc/keepalived/keepalived.conf
    sudo cp haproxy-keepalived/check_haproxy.sh /etc/keepalived/check_haproxy.sh
    sudo cp /etc/haproxy/haproxy.cfg /etc/haproxy/haproxy.cfg.backup
    sudo cat haproxy-keepalived/haproxy.cfg >> /etc/haproxy/haproxy.cfg
    sudo keepalived -D -f /etc/keepalived/keepalived.conf
    time sleep 2
    sudo systemctl restart haproxy
    time sleep 2
    systemctl status haproxy
fi

