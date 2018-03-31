# OpenZWave Sensor Sniffer in Python 3

This program initializes the ZWave Network, logging any and all value refreshes received to the file output.csv -- this includes sensor readings and other updates.


## Set-up

### Ubuntu (also Windows Subsystem for Linux with Ubuntu)

* ./setup_ubuntu.sh
* ./allow_port_access_forever_ubuntu.sh

### OS X

* ./setup_os_x.sh

## Running

* ./run.sh <optional port name, defaults to /dev/ttyACM0 for Linux>

## Stopping
* Just do ctrl+C once, it will stop itself.

## FAQ

### What should the port name be?

** Assume # to be the port number of the ZWave Stick. **

#### Windows Subsystem for Linux with Ubuntu
It should be COM# in Windows and /dev/ttyS# in Ubuntu. You can try figure out what # is by opening Device Manager and looking at the USB devices list, then trying each with `./run.sh /dev/ttyS#` until it works. If you get an error message that permission is denied, run `./allow_port_access_once.sh /dev/tty/S#`.

#### OS X
It should be /dev/ttyUSB#, you can also try each one until you get it right.

### Any other Linux system
It should be /dev/ttyACM#, you may need permission to read/write to the port. In that case, run `./allow_port_access_once.sh /dev/ttyACM#` or use the indefinite version.

### Is it relatively safe to delete all the files that seem to be generated (i.e. pyozw.sqlite) when I run the sniffer?

Yes, just make sure you stop the sniffer first.
