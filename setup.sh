#!/bin/bash

echo ""

pip install -r requirements.txt 
pip3 uninstall -y -r uninstall.txt 
python3 bot.py