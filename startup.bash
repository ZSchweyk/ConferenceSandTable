# SSH to the pi
# shellcheck disable=SC2164
cd ~/projects/ConferenceSandTable/Server
export FLASK_APP=server
flask run --host=0.0.0.0
# http://10.107.200.23:5000/
