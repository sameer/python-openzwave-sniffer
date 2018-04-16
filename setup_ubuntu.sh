sudo apt-get update && sudo apt-get install --force-yes -y make python3 python3-pip libudev-dev g++ libyaml-dev
sudo pip3 install virtualenv
virtualenv --python=python3 venv
source venv/bin/activate
pip3 install python_openzwave
pip3 install cython wheel six
