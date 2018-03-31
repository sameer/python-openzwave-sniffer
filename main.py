#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging

import time

import sys

import openzwave
from openzwave.network import ZWaveNetwork

from home_manager import HomeManager


class Config:
    DEVICE_PATH = "/dev/ttyACM0"  # Change to /dev/ttyUSB0 if on OS X
    OZW_LOG_LEVEL = "None"
    LOGGING_NAME = 'openzwave'
    DEFAULT_LOGGING_FORMATTER = "%(asctime)s %(levelname)s %(name)-10s[%(process)d] -- %(message)s"


def start():
    logging.basicConfig(level=logging.INFO, format=Config.DEFAULT_LOGGING_FORMATTER)
    logger = logging.getLogger(Config.LOGGING_NAME + '/' + __file__)
    logger.info("Launching with ZWave Stick at %s", Config.DEVICE_PATH)
    try:
        manager = HomeManager(Config.DEVICE_PATH, Config.OZW_LOG_LEVEL, logger)
    except openzwave.object.ZWaveException as e:
        logger.error('Unable to create ZWave Network: %s', e.value)
        return

    manager.connect_signals()
    manager.start()
    cur_state = manager.network.state
    cur_state_str = manager.network.state_str
    while True:
        time.sleep(0.25)
        if cur_state != manager.network.state:
            logger.info("%s ==> %s", cur_state_str, manager.network.state_str)
            cur_state = manager.network.state
            cur_state_str = manager.network.state_str
        if cur_state is ZWaveNetwork.STATE_STOPPED:
            logger.info("Stopped")
            break


if __name__ == "__main__":
    if len(sys.argv) > 1:
        Config.DEVICE_PATH = sys.argv[1]
    start()
