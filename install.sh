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

sudo apt install -y python2

# BlockChain
cd ~
git clone --depth 1 https://github.com/WandeF/BlockChain.git
cd BlockChain
./install.sh

# WEBGUI
cd ~
git clone --depth 1 https://github.com/WandeF/WebGUI.git
cd WebGUI
./install.sh


# Get python2 pip
curl https://bootstrap.pypa.io/pip/2.7/get-pip.py --output get-pip.py
sudo python2 get-pip.py -i https://pypi.tuna.tsinghua.edu.cn/simple
rm get-pip.py

# CPPPO Correct Version 4.0.*
sudo pip install -i https://pypi.tuna.tsinghua.edu.cn/simple cpppo==4.0.*

# MiniCPS
cd ~
git clone --depth 1 https://github.com/afmurillo/minicps.git || git -C minicps pull
cd minicps
sudo python2 -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple .



# Installing other DHALSIM dependencies
sudo pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pathlib==1.0.*
sudo pip install -i https://pypi.tuna.tsinghua.edu.cn/simple numpy==1.16.*
sudo python3 -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pandas==1.3.4
sudo python3 -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple matplotlib==3.5.0
sudo python3 -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple testresources

# Mininet from source
cd ~
git clone https://github.com/mininet/mininet.git || git -C mininet pull
cd mininet
sudo PYTHON=python2 ./util/install.sh -fnv

# Installing testing pip dependencies
if [ "$test" = true ]
then
  sudo pip2 install -i https://pypi.tuna.tsinghua.edu.cn/simple netaddr==0.8.*
  sudo pip2 install -i https://pypi.tuna.tsinghua.edu.cn/simple flaky==3.7.*
  sudo pip2 install -i https://pypi.tuna.tsinghua.edu.cn/simple pytest==4.6.*
  sudo pip2 install -i https://pypi.tuna.tsinghua.edu.cn/simple pytest-timeout==1.4.*
  sudo pip2 install -i https://pypi.tuna.tsinghua.edu.cn/simple pytest-cov==2.12.*
  sudo pip2 install -i https://pypi.tuna.tsinghua.edu.cn/simple pytest-mock==3.6.*
fi

# Install netfilterqueue for Simple DoS attacks
sudo apt install -y python3-pip git libnfnetlink-dev libnetfilter-queue-dev
sudo python3 -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -U git+https://github.com/kti/python-netfilterqueue

# Install DHALSIM
cd "${cwd}" || { printf "Failure: Could not find DHALSIM directory\n"; exit 1; }

# Install without doc and test
if [ "$test" = false ] && [ "$doc" = false ]
then
  sudo python3 -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -e .

  printf "\nInstallation finished. You can now run DHALSIM by using \n\t<sudo dhalsim your_config.yaml>.\n"
  exit 0;
fi

# Install doc
if [ "$test" = false ]
then
  sudo python3 -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -e .[doc]

  printf "\nInstallation finished. You can now run DHALSIM by using \n\t<sudo dhalsim your_config.yaml>.\n"
  exit 0;
fi

# Install test
if [ "$doc" = false ]
then
  sudo python3 -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -e .[test]

  printf "\nInstallation finished. You can now run DHALSIM by using \n\t<sudo dhalsim your_config.yaml>.\n"
  exit 0;
fi

# Install test and doc
sudo python3 -m pip install -e .[test,doc]

printf "\nInstallation finished. You can now run DHALSIM by using \n\t<sudo dhalsim your_config.yaml>.\n"
exit 0;
