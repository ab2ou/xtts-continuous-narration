#!/bin/bash
# Update and install system dependencies
apt-get update && apt-get install -y ffmpeg espeak-ng python3.10 python3.10-dev python3.10-distutils

# Install pip and upgrade core tools
curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10
python3.10 -m pip install --upgrade pip setuptools wheel

# Install all requirements from the requirements.txt file
python3.10 -m pip install -r requirements.txt
