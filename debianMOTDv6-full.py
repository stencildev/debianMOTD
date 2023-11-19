import os
import time

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

echo "SYSTEM LOAD"
uptime | awk -F 'average: ' '{print $2}'
echo

echo "DISK USAGE"
df -h / | awk 'NR==2 {print "Usage of /:", $5}'
echo

echo "MEMORY USAGE"
free -m | awk 'NR==2 {printf "Memory usage: %.1f%%\\n", ($3/$2)*100}'
echo

echo "SWAP USAGE"
free -m | awk 'NR==3 {printf "Swap usage: %.1f%%\\n", ($3/$2)*100}'
echo

echo "PROCESSES"
ps aux | wc -l | awk '{print "Processes:", $1}'
echo

echo "USERS LOGGED IN"
who | wc -l | awk '{print "Users logged in:", $1}'
echo

echo "NETWORK ADDRESSES"
for iface in $(ip -4 addr show | grep inet | awk '!/ lo:/ {print $NF}'); do
  ip -4 addr show $iface | awk '/inet / {print "IPv4 address for", $NF ":", $2}'
done
'''

with open('/etc/update-motd.d/01-custom', 'w') as f:
    f.write(custom_motd_script)

# Make the script executable
os.system("chmod +x /etc/update-motd.d/01-custom")

# Disable the MOTD service
os.system("systemctl disable motd")

print("Setup complete. You may need to restart your session to see the changes.")
