#!/bin/bash

REPOSITORY_NAME="MaanNhai-UI"
REPOSITORY_URL="https://github.com/kchammanard/MaanNhai-UI.git"

cd
if [ ! -d "$REPOSITORY_NAME" ]; then
    git clone "$REPOSITORY_URL"
fi

cd "$REPOSITORY_NAME"
python3 -u device.py &> device.log &
