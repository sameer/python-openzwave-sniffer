#!/bin/bash
die() {
	echo >&2 "$@"
	exit 1
}
[ "$#" -eq 1 ] || die "One argument required: absolute path of ZWave Stick port (i.e. /dev/ttyUSB0), you provided '$@'"
[ -f $1 ] || die "There is no ZWave Stick at '$1'!"
chmod 666 $1