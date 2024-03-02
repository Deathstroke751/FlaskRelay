sudo supervisorctl stop relaybot
sudo supervisorctl remove relaybot
sudo rm -rf FlaskRelay/
git clone https://github.com/Deathstroke751/FlaskRelay
cd FlaskRelay/
sudo chmod +x start.sh
chmod +x start.sh
sudo supervisorctl update