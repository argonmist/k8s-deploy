#!/bin/bash

FILE=deploy-node.tar.gz
if test -f "/tmp/$FILE"; then
    mv /tmp/$FILE ./
    tar zxvf $FILE
fi


FILE=deploy-node/sources.list
if test -f "$FILE"; then
    export LC_ALL=C
    sudo mkdir /offlinePackage
    sudo cp /etc/apt/sources.list /etc/apt/sources.list.back
    sudo mv $FILE /etc/apt/sources.list
    sudo mv deploy-node/offlinePackage/* /offlinePackage
    sudo apt-get update --allow-insecure-repositories
    cat deploy-node/packages_list.txt | xargs sudo apt-get install -y --allow-unauthenticated
    rm -r deploy-node/offlinePackage
    rm -r deploy-node/packages_list.txt
    sudo firewall-cmd --permanent --add-port=6443/tcp
    sudo firewall-cmd --permanent --add-port=2380/tcp
    sudo firewall-cmd --permanent --add-port=10251/tcp
    sudo firewall-cmd --permanent --add-port=10252/tcp
    sudo firewall-cmd --permanent --add-port=10250/tcp
    sudo firewall-cmd --permanent --add-port=10255/tcp
    sudo firewall-cmd --permanent --add-port=30000-32767/tcp
    sudo firewall-cmd --permanent --add-port=179/tcp
    sudo firewall-cmd --permanent --add-port=2379/tcp
    sudo firewall-cmd --permanent --add-port=5473/tcp
    sudo firewall-cmd --permanent --add-port=4789/udp
    sudo firewall-cmd --permanent --add-port=6783/tcp
    sudo firewall-cmd --permanent --add-port=443/tcp
    sudo firewall-cmd --permanent --add-port=53/tcp
    sudo firewall-cmd --permanent --add-port=8081/tcp
    sudo firewall-cmd --reload
fi

FILE=deploy-node/requirements.txt
if test -f "$FILE"; then
    export LC_ALL=C
    pip3 install --no-index --find-links=deploy-node/pip-package -r $FILE
    rm $FILE
    rm -r deploy-node/pip-package
fi

FILE=deploy-node/Docker_images
if [ -d "$FILE" ]; then
    cd $FILE
    directory=`pwd`
    ls | grep tar > files.txt
    c=0
    printf "START \n"
    input="$directory/files.txt"
    while IFS= read -r line
    do
         c=$((c+1))
         printf "$c) $line \n"
         sudo docker load -i $line
         printf "$c) Successfully created the Docker image $line  \n \n"
    done < "$input"
    cd ../
    rm -r Docker_images
fi
