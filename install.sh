set -xe
python3 -m venv ./venv/
. ./venv/bin/activate
pip install python-rtmidi --install-option="--no-jack"
pip install -r requirements.txt
