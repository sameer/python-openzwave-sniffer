#!/bin/bash
die() {
	echo >&2 "$@"
	exit 1
}
[[ -f venv/bin/activate ]] || die "You have not set up the virtual environment yet, run setup_your_os.sh first!"
source venv/bin/activate
python3 main.py $@
