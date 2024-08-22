#!/bin/bash

# Set variables
INSTALL_DIR="/etc/bell/chat"
SCRIPT_NAME="terminal_chat.py"
SCRIPT_URL="https://raw.githubusercontent.com/bellnetwork/Bell-Let-s-Talk/main/terminal_chat.py"
DESKTOP_FILE="$HOME/.local/share/applications/bell_lets_talk.desktop"
DESKTOP_FILE_NAME="bell_lets_talk.desktop"

# Create installation directory
echo "Creating installation directory at $INSTALL_DIR..."
sudo mkdir -p $INSTALL_DIR

# Download the Python script
echo "Downloading $SCRIPT_NAME..."
sudo curl -o $INSTALL_DIR/$SCRIPT_NAME $SCRIPT_URL

# Make the Python script executable
echo "Making $SCRIPT_NAME executable..."
sudo chmod +x $INSTALL_DIR/$SCRIPT_NAME

# Create the .desktop file
echo "Creating .desktop launcher..."
mkdir -p ~/.local/share/applications
cat << EOF > $DESKTOP_FILE
[Desktop Entry]
Name=Bell Let's Talk Terminal
Comment=Launch the Bell Let's Talk chat application
Exec=gnome-terminal -- /usr/bin/python3 $INSTALL_DIR/$SCRIPT_NAME
Icon=utilities-terminal
Terminal=false
Type=Application
Categories=Utility;Application;
EOF

# Make the .desktop file executable
chmod +x $DESKTOP_FILE

# Final message
echo "Installation complete! You can launch the application by searching for 'The Ultimative Bell Let's Talk Terminal' in your application menu or by double-clicking the .desktop launcher."
