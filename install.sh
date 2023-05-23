#!/bin/bash

# Update package lists
sudo apt update
sudo apt-get install libportaudio0 libportaudio2 libportaudiocpp0 portaudio19-dev
# Install required Python packages
pip install pyaudio
pip install picamera
pip install moviepy

# Change directory to where the script is located
cd "$(dirname "$0")"

# Make the Python script executable
chmod +x main.py
chmod +x send_data.py
chmod +x sync_data.py
# Add the script execution command to rc.local
sudo sed -i '$i python3 /path/to/main.py &' /etc/rc.local
sudo sed -i '$i python3 /path/to/send_data.py &' /etc/rc.local
sudo sed -i '$i python3 /path/to/sync_data.py &' /etc/rc.local

# Reboot the Raspberry Pi
sudo reboot
# Exit the script
exit 0
