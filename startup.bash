# shellcheck disable=SC2164

# SSH to the pi
# ssh pi@conference-sand-table-v2-pi.local

# BE SURE TO ACTIVATE THE Flask VENV!!!!!!
source ~packages/Flask/bin/activate

cd ~/projects/ConferenceSandTable/Server
export FLASK_APP=server
# Enable debug mode
export FLASK_ENV=development
flask run --host=0.0.0.0
# http://10.107.200.23:5000/
