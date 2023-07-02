#!/bin/bash

# Update package lists
sudo apt update
sudo apt-get install libportaudio0 libportaudio2 libportaudiocpp0 portaudio19-dev
# Install required Python packages
pip install pyaudio
pip install picamera
pip install moviepy
pip install sounddevice
pip install soundfile
pip install ffmpeg
# LLVM_CONFIG=/usr/bin/llvm-config pip3 install llvmlite==0.31.0 numba==0.48.0 colorama==0.3.9 librosa==0.6.3
# Change directory to where the script is located
cd "$(dirname "$0")"

# Make the Python script executable
chmod +x main.py
# Add the script execution command to rc.local
sudo sed -i '$i python3 /home/bse23/Desktop/rasp-main/main.py &' /etc/rc.local

