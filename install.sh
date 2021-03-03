set -xe
sudo apt-get install libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0
python3 -m venv ./venv/
. ./venv/bin/activate
pip install python-rtmidi --install-option="--no-jack"
pip install -r requirements.txt
