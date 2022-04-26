# BE SURE TO ACTIVATE THE Flask VENV!!!!!!
source packages/Flask/bin/activate  # just run the activate file on Windows

cd projects/ConferenceSandTable/Server
export FLASK_APP=server  # use set FLASK_APP=server on Windows
# Enable debug mode
export FLASK_ENV=development  # use set FLASK_ENV=development on Windows
flask run --host=0.0.0.0
# http://10.107.200.23:5000/