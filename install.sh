#!/bin/bash

cwd=$(pwd)
version=$(lsb_release -rs )

# Wrong version warning
if [ "$version" != "20.04" ]
then
  printf "Warning! This installation script has only been tested on Ubuntu 20.04 LTS and will likely not work on your Ubuntu version.\n\n"
fi

doc=false
test=false

# Setting up test and doc parameters
while getopts ":dt" opt; do
  case $opt in
    d)
      printf "Installing with documentation dependencies.\n"
      doc=true
      ;;
    t)
      printf "Installing with testing dependencies.\n"
      test=true
      ;;
    \?)
      printf "Unknown option. Proceeding without installing documentation and testing dependencies.\n"
      ;;
  esac
done

sleep 3

# Update apt
sudo apt update

# Installing necessary packages
sudo apt install -y python3 python3-pip 


# BlockChain
# cd ~
# git clone --depth 1 https://github.com/WandeF/BlockChain.git
# cd BlockChain
# ./install.sh

# WEBGUI
# cd ~
# git clone --depth 1 https://github.com/WandeF/WebGUI.git
# cd WebGUI
# ./install.sh


sudo apt install -y python2

sudo apt  install curl
# Get python2 pip
curl https://bootstrap.pypa.io/pip/2.7/get-pip.py --output get-pip.py
sudo python2 get-pip.py -i http://mirrors.aliyun.com/pypi/simple/
rm get-pip.py

# CPPPO Correct Version 4.0.*
sudo pip install -i http://mirrors.aliyun.com/pypi/simple/ cpppo==4.0.*

# MiniCPS
cd ~
git clone --depth 1 https://github.com/afmurillo/minicps.git || git -C minicps pull
cd minicps
sudo python2 -m pip install -i http://mirrors.aliyun.com/pypi/simple/ .



# Installing other DHALSIM dependencies
sudo pip install -i http://mirrors.aliyun.com/pypi/simple/ pathlib==1.0.*
sudo pip install -i http://mirrors.aliyun.com/pypi/simple/ numpy==1.16.*
sudo pip install -i http://mirrors.aliyun.com/pypi/simple/ pathlib
sudo pip install -i http://mirrors.aliyun.com/pypi/simple/ networkx
sudo pip install -i http://mirrors.aliyun.com/pypi/simple/ pyyaml
sudo pip install -i http://mirrors.aliyun.com/pypi/simple/ jsonpickle
sudo pip install -i http://mirrors.aliyun.com/pypi/simple/ mininet
sudo python3 -m pip install -i http://mirrors.aliyun.com/pypi/simple/ pandas==1.3.4
sudo python3 -m pip install -i http://mirrors.aliyun.com/pypi/simple/ matplotlib==3.5.0
sudo python3 -m pip install -i http://mirrors.aliyun.com/pypi/simple/ testresources

# Mininet from source
cd ~
git clone https://github.com/mininet/mininet.git || git -C mininet pull
cd mininet
sudo PYTHON=python2 ./util/install.sh -fnv

# Installing testing pip dependencies
if [ "$test" = true ]
then
  sudo pip2 install -i http://mirrors.aliyun.com/pypi/simple/ netaddr==0.8.*
  sudo pip2 install -i http://mirrors.aliyun.com/pypi/simple/ flaky==3.7.*
  sudo pip2 install -i http://mirrors.aliyun.com/pypi/simple/ pytest==4.6.*
  sudo pip2 install -i http://mirrors.aliyun.com/pypi/simple/ pytest-timeout==1.4.*
  sudo pip2 install -i http://mirrors.aliyun.com/pypi/simple/ pytest-cov==2.12.*
  sudo pip2 install -i http://mirrors.aliyun.com/pypi/simple/ pytest-mock==3.6.*
fi

# Install netfilterqueue for Simple DoS attacks
sudo apt install -y python3-pip git libnfnetlink-dev libnetfilter-queue-dev
sudo python3 -m pip install -i http://mirrors.aliyun.com/pypi/simple/ -U git+https://github.com/kti/python-netfilterqueue

# Install DHALSIM
cd "${cwd}" || { printf "Failure: Could not find DHALSIM directory\n"; exit 1; }

# Install without doc and test
if [ "$test" = false ] && [ "$doc" = false ]
then
  sudo python3 -m pip install -i http://mirrors.aliyun.com/pypi/simple/ -e .

  printf "\nInstallation finished. You can now run DHALSIM by using \n\t<sudo dhalsim your_config.yaml>.\n"
  exit 0;
fi

# Install doc
if [ "$test" = false ]
then
  sudo python3 -m pip install -i http://mirrors.aliyun.com/pypi/simple/ -e .[doc]

  printf "\nInstallation finished. You can now run DHALSIM by using \n\t<sudo dhalsim your_config.yaml>.\n"
  exit 0;
fi

# Install test
if [ "$doc" = false ]
then
  sudo python3 -m pip install -i http://mirrors.aliyun.com/pypi/simple/ -e .[test]

  printf "\nInstallation finished. You can now run DHALSIM by using \n\t<sudo dhalsim your_config.yaml>.\n"
  exit 0;
fi

# Install test and doc
sudo python3 -m pip install -e .[test,doc]

printf "\nInstallation finished. You can now run DHALSIM by using \n\t<sudo dhalsim your_config.yaml>.\n"
exit 0;
