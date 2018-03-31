# OpenZWave Sensor Sniffer in Python 3

This program initializes the ZWave Network, logging any and all value refreshes received to the file output.csv -- this includes sensor readings and other updates.


## Set-up

### Ubuntu

> ./setup_ubuntu.sh
> ./allow_port_access_forever_ubuntu.sh

### OS X

> ./setup_os_x.sh

## Running

> ./run.sh <optional port name, defaults to /dev/ttyACM0 for Linux>

## Stopping
Just do ctrl+C once, it will stop itself.

## FAQ

### What should the port name be?

** Assume # to be the port number of the ZWave Stick. **

On Windows, COM#, you can figure out what this number is by opening Device Manager and looking at the USB devices list

On OS X, it should be /dev/ttyUSB#, you can try each one until you get it right

On Linux, it should be /dev/ttyACM#, you may need permission to read/write to the port. In that case, run `./allow_port_access_once.sh /dev/ttyACM#`.

### Is it relatively safe to delete all the files that seem to be generated (i.e. pyozw.sqlite) when I run the sniffer?

Yes, just make sure you stop the sniffer first.
