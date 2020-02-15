#!/bin/bash

FILE=haproxy-keepalived.tar.gz
if test -f "/tmp/$FILE"; then
    mv /tmp/$FILE ./
    tar zxvf $FILE
fi

FILE=haproxy-keepalived/sources.list
if test -f "$FILE"; then
    export LC_ALL=C
    sudo mkdir /offlinePackage
    sudo cp /etc/apt/sources.list /etc/apt/sources.list.back
    sudo mv $FILE /etc/apt/sources.list
    sudo mv haproxy-keepalived/offlinePackage/* /offlinePackage
    sudo apt-get update --allow-insecure-repositories
    cat haproxy-keepalived/packages_list.txt | xargs sudo apt-get install -y --allow-unauthenticated
    rm -r haproxy-keepalived/offlinePackage
fi

