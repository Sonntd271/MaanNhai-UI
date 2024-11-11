#!/bin/bash

REPOSITORY_NAME="MaanNhai-UI"
REPOSITORY_URL="https://github.com/kchammanard/MaanNhai-UI.git"

# Install system dependencies
python3 --version
if [ $? -ne 0 ]; then
    # Install python if not on host
    sudo apt install -y python3
fi

sudo apt-get update
sudo apt install -y python3-pip python3.12-venv && sudo apt-get update

# Clone into repo
git clone $REPOSITORY_URL
cd $REPOSITORY_NAME

# Set up a virtual environment
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt

# Run app
python3 app.py
