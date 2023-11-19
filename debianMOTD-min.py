import os

# Check if the script is run as root
if os.geteuid() != 0:
    print("Please run this script as root (using sudo).")
    exit(1)

# Update the package repository
os.system("sudo apt update")

# Install screenfetch and inxi
os.system("sudo apt install screenfetch inxi -y")

# Switch to superuser mode
os.system("sudo su -")

# Make all scripts in /etc/update-motd.d non-executable
os.system("chmod -x /etc/update-motd.d/*")

os.system('mv /etc/motd /etc/motd.bk')

# Create and edit the custom MOTD script
custom_motd_script = '''#!/bin/sh
echo "GENERAL SYSTEM INFORMATION"
echo
/usr/bin/screenfetch
echo
echo "SYSTEM DISK USAGE"
export TERM=xterm; inxi -D
echo
'''

with open('/etc/update-motd.d/01-custom', 'w') as f:
    f.write(custom_motd_script)

# Make the script executable
os.system("chmod +x /etc/update-motd.d/01-custom")

# Overwrite the MOTD with system information
os.system("uname -snrvm > /var/run/motd.dynamic")

# Disable the MOTD service
os.system("systemctl disable motd")

print("Setup complete. You may need to restart your session to see the changes.")
