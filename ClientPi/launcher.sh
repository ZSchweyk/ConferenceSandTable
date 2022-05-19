cd $(dirname $(readlink -f "$0"))

export PYTHONPATH="/home/pi/.local/lib/python3.7/site-packages"

cd /home/pi/projects/ConferenceSandTable/ClientPi
python3 main.py

