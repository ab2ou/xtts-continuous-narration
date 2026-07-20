#!/bin/bash
apt-get update && apt-get install -y ffmpeg espeak-ng
pip install --upgrade pip
pip install -r requirements.txt
