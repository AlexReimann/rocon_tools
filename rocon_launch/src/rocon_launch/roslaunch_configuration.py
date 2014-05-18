#!/usr/bin/env python
#
# License: BSD
#   https://raw.github.com/robotics-in-concert/rocon_tools/license/LICENSE
#
##############################################################################
# Description
##############################################################################

"""
.. module:: roslaunch_configuration
   :platform: Unix
   :synopsis: Configuration for a single roslaunch


This module provides the context for a roslaunch configuration.

----

"""
##############################################################################
# Imports
##############################################################################

import os
import argparse
import subprocess
import signal
import sys
from time import sleep
import roslaunch
import tempfile
import rocon_python_utils
import rosgraph
import rocon_console.console as console
from urlparse import urlparse
import xml.etree.ElementTree as ElementTree

from .exceptions import InvalidRoconLauncher

##############################################################################
# Methods
##############################################################################


def _get_default_port():
    '''
    Helper method to determine the default port to use for roslaunch
    configurations. Uses the ros master uri port or 11311 otherwise.

    :returns: the default port
    :rtype: int
    '''
    ros_master_port = urlparse(os.environ["ROS_MASTER_URI"]).port
    return ros_master_port if ros_master_port is not None else 11311

##############################################################################
# Classes
##############################################################################


class RosLaunchConfiguration(object):
    __slots__ = [
                 'args',
                 'package',
                 'name',
                 'title',
                 'port',
                 'options',
                 'path'
                ]

    default_port = _get_default_port()

    def __init__(self,
                 name,
                 package=None,
                 port=None,
                 title=None,
                 args=[],
                 options=""):
        """
        :param str name: filename (must be absolute path if package is set to None)
        :param str package: name of the catkin package to find the launcher in (can be None)
        :param int port: port to launch on (defaults to ROS_MASTER_URI's or 11311 if None)
        :param str title: title to use for the launch window (provides a sensible default if None)
        :param str[] args: any args contained in the launcher
        :param str options: command line options to pass to roslaunch (string form, not list)

        :raises :exc:`.InvalidRoconLauncher`
        """
        self.args = args
        self.package = package
        self.name = name
        self.title = title or "RosLaunch Window"
        if self.package is None:
            # look for a standalone launcher
            if os.path.isfile(self.name):
                self.path = self.name
            else:
                raise InvalidRoconLauncher("roslaunch file does not exist [%s]" % self.name)
        else:
            # look for a catkin package launcher
            try:
                self.path = rocon_python_utils.ros.find_resource(self.package, self.name)
            except IOError as e:
                raise InvalidRoconLauncher("roslaunch file does not exist [%s/%s][%s]" % (self.package, self.name, str(e)))
        self.port = port or RosLaunchConfiguration.default_port
        self.options = options

    def append_option(self, option):
        """
        Appends a roslaunch command line option to the configuration.

        :param str option:
        """
        self.option = self.option + " " + option
