import csv
import signal
import datetime
import sys
import time
from openzwave.command import ZWaveNodeSensor
from openzwave.network import ZWaveNetwork
from openzwave.option import ZWaveOption
from pydispatch import dispatcher


def ozw_debug(logger, network):
    logger.info("------------------------------------------------------------")
    logger.info("Use openzwave library : {}".format(network.controller.ozw_library_version))
    logger.info("Use python library : {}".format(network.controller.python_library_version))
    logger.info("Use ZWave library : {}".format(network.controller.library_description))
    logger.info("Network home id : {}".format(network.home_id_str))
    logger.info("Controller node id : {}".format(network.controller.node.node_id))
    logger.info("Controller node version : {}".format(network.controller.node.version))
    logger.info("Nodes in network : {}".format(network.nodes_count))
    logger.info("------------------------------------------------------------")


def value_refresh_to_influxdb_json(node, val):
    return {
        "measurement": "value_refresh",
        "tags": {
            'id_on_network': val.id_on_network,
            'home_id': node.home_id,
            'node_id': node.node_id,
            'value_id': val.value_id,
            'manufacturer_id': node.manufacturer_id,
            'product_id': node.product_id,
            'label': str(val.label),
            'genre': str(val.genre),
        },
        "time": time.asctime(time.localtime()),
        "fields": {
            'label': str(val.label),
            'data': str(val.data_as_string),
            'units': str(val.units),
            'max': str(val.max),
            'min': str(val.min),
        }
    }


def value_refresh_to_csv(node, val):
    return [
        datetime.datetime.now(),
        val.id_on_network,  # A sort of sensor UUID
        node.home_id,       # The home id, a hexadecimal string
        node.node_id,       # The node id, a number from 1 to n where n is the number of nodes on the network
        val.value_id,       # The value id, a string that identifies the 
        node.manufacturer_id, # Manufacturer identifier, useful for knowing which sensor the value is from
        node.product_id,    # Product identifier, useful for knowing which sensor the value is from
        val.data_as_string, # Data read, converted to a string
        val.units,          # Units of the data, can be empty
        val.label,          # What kind of data it is
        val.min,            # Minimum possible value
        val.max,            # Maximum possible value
    ]


class HomeManager(object):
    def __init__(self, device_path, ozw_log_level, logger):
        self.logger = logger

        options = ZWaveOption(device_path,
                              config_path="./venv/lib/python3.%d/site-packages/python_openzwave/ozw_config" % sys.version_info[1],
                              user_path=".", cmd_line="")
        options.set_log_file("OZW.log")
        options.set_append_log_file(False)
        options.set_save_log_level(ozw_log_level)
        options.set_console_output(False)
        options.set_logging(True)
        options.lock()
        self.options = options
        self.network = ZWaveNetwork(options, log=None, autostart=False)
        self.csvfile = open('output.csv', 'a')
        self.writer = csv.writer(self.csvfile)
        self.stopping = False

    def start(self):
        self.logger.info("Starting network...")
        self.network.start()

    def stop_signal(self, signum, frame):
        self.stop()

    def stop(self):
        if self.stopping:
            return
        else:
            self.stopping = True
        self.logger.info("Stopping network...")
        self.network.stop()
        self.csvfile.close()
        self.logger.info("Stopped")

    def connect_signals(self):
        dispatcher.connect(self.signal_network_ready, self.network.SIGNAL_NETWORK_READY)
        signal.signal(signal.SIGINT, self.stop_signal)

    # Note -- the name of the network parameter must not change!
    def signal_network_ready(self, network):
        if self.network is not network:
            return
        else:
            del network
        ozw_debug(self.logger, self.network)
        self.logger.info("Network is ready!")
        dispatcher.connect(self.signal_node_update, self.network.SIGNAL_NODE)
        dispatcher.connect(self.signal_value_refreshed, self.network.SIGNAL_VALUE)

    # Note -- the names of the network/node/value parameters must not change!
    def signal_value_refreshed(self, network, node, value):
        if self.network is not network:
            return
        else:
            del network
        self.logger.info("Received value refresh %s: %s", value.id_on_network, value)
        self.writer.writerow(value_refresh_to_csv(node, value))
        self.csvfile.flush()

    # Note -- the names of the network/node parameters must not change!
    def signal_node_update(self, network, node):
        return

    @staticmethod
    def is_sensor(node):
        return isinstance(node, ZWaveNodeSensor) and not len(node.get_sensors()) is 0
