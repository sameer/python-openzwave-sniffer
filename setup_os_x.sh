#!/bin/bash
brew install python3

pip3 install virtualenv
virtualenv --python=python3 venv
source venv/bin/activate
pip3 install python_openzwave
pip3 install cython wheel six
