#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
    Name: freeprobe.py
    Arguments:
        -r, --register: register freeprobe in Freebox (to allow FreeOS API connection) and exit
        -d, --dr-run: print performance counters to stdout without sendig them to Prometheus 
                      push-gateway
        -h, --help: print usage on stdout
        -V, --version : print script version on stdout
    Description:
        Connect to Freebox and retrieve various performance counters to push them to Prometheus
        push gateway 
    Requirements:
        The Prometheus "push-gateway" must be installed and configured (address and port)
        For security reason the script must be executed as root
    Todo:
        Loggin
        Raw output for counters
        Push gateway server address and port as arguments
        Metrics prefix as argument
"""
import os
import sys
import argparse
import ptvsd
import requests
import time
from requests import HTTPError
from zeroconf import Zeroconf, ServiceBrowser

__version_info__ = ('0', '0', '1')
__version__ = '.'.join(__version_info__)
__date__ = "2019-06-23"
__author__ = "Denis Lambolez"
__contact__ = "denis.lambolez@gmail.com"
__license__ = "MIT"

METRICS_PREFIXE = "freebox_"
PUSHGATEWAY_ADDRESS = "prometheus.catsnet.home"
PUSHGATEWAY_PORT = "9091"


class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class FreeboxError(Error):
    """Raised when unable to communicate with Freebox

    Attributes:
        message -- reason why we can't communicate
    """

    def __init__(self, message):
        """Constructor with message"""

        self.message = message


class Freebox(object):
    """Definition of the Freebox server

    Constants:
        _TYPE: private - string - The Freebox broadcasts the “_fbx-api._tcp” service
    Attributes:
        _mds_listener: private - MDNSListener - provide callback function for mDNS service browser  
    Properties:
        name: string, ro - Fully qualified name of the service
        addresse: string, ro - IP addresse of service
        port: integer, ro - port of the service
        server: string, ro, - name of the server
        type: string, ro - type of the service
        api_version: string, ro - The current API version on the Freebox
        device_type: string, ro - “FreeboxServerx,y” for the Freebox Server revision w,y
        api_base_url: string, ro - The API root path on the HTTP server
        uid: string, ro - The device unique id
        api_domain: string, ro - The domain to use in place of hardcoded Freebox ip
        https_available: string, ro - Tells if https has been configured on the Freebox
        https_port: string, ro - Port to use for remote https access to the Freebox Api
        box_model: string, ro - model of the Freebox
        box_model_name: string, ro - model name of the freebox
    Exceptions:
        FreeboxError - Don't find a Freebox on the local network
    """

    # From API docuemntation "https://dev.freebox.fr/sdk/os/" service name is “_fbx-api._tcp”
    # zeroconf requests to have ".local." at the end of service name
    _TYPE = "_fbx-api._tcp.local."

    class MDNSListener():
        """Callback class to get information of the available MDNS service

        Attributes:
            _info: private - composite - information on the Freebox and FreeOS API 
        """

        def __init__(self):
            """Constructor"""

            self._info = None

        def add_service(self, zeroconf, stype, name):
            """Callback when service is added. Get service info"""

            self._info = zeroconf.get_service_info(stype, name)

        @property
        def svc_info(self):
            return self._info

    def __init__(self):
        """Initialize the Freebox through mDNS discovery

        Exceptions:
            ConnectionError - Don't find a Freebox on the local network
        """

        self._mdns_listener = Freebox.MDNSListener()

        zeroconf = Zeroconf()
        # Launch the browser thread with the service type
        browser = ServiceBrowser(zeroconf, self._TYPE, self._mdns_listener)
        # Allow one second for the browser thread to find the Freebox
        time.sleep(5)
        # Cancel the browser thread and close zeroconf
        browser.cancel()
        zeroconf.close()

        if not self._mdns_listener.svc_info:
            raise FreeboxError(
                "Fatal: Unable to find a Freebox on the local network!")

    @property
    def name(self):
        if not self._mdns_listener.svc_info:
            return None
        else:
            return self._mdns_listener.svc_info

    @property
    def addresses(self):
        if not self._mdns_listener.svc_info:
            return None
        else:
            return self._mdns_listener.svc_info

    @property
    def port(self):
        if not self._mdns_listener.svc_info:
            return None
        else:
            return self._mdns_listener.svc_info

    @property
    def server(self):
        if not self._mdns_listener.svc_info:
            return None
        else:
            return self._mdns_listener.svc_info

    @property
    def api_version(self):
        if not self._mdns_listener.svc_info:
            return None
        else:
            return self._mdns_listener.svc_info

    @property
    def device_type(self):
        if not self._mdns_listener.svc_info:
            return None
        else:
            return self._mdns_listener.svc_info

    @property
    def api_base_url(self):
        if not self._mdns_listener.svc_info:
            return None
        else:
            return self._mdns_listener.svc_info

    @property
    def uid(self):
        if not self._mdns_listener.svc_info:
            return None
        else:
            return self._mdns_listener.svc_info

    @property
    def api_domain(self):
        if not self._mdns_listener.svc_info:
            return None
        else:
            return self._mdns_listener.svc_info

    @property
    def https_available(self):
        if not self._mdns_listener.svc_info:
            return None
        else:
            return self._mdns_listener.svc_info

    @property
    def https_port(self):
        if not self._mdns_listener.svc_info:
            return None
        else:
            return self._mdns_listener.svc_info

    @property
    def box_model(self):
        if not self._mdns_listener.svc_info:
            return None
        else:
            return self._mdns_listener.svc_info

    @property
    def box_model_name(self):
        if not self._mdns_listener.svc_info:
            return None
        else:
            return self._mdns_listener.svc_info


def main():
    """Script main function"""

    # Parse command line arguments
    parser = argparse.ArgumentParser(description="connect to Freebox and retrieve various "
                                     + "performance counters to push them to Prometheus")
    parser.add_argument("-r", "--register", action="store_true", help="register freeprobe in "
                        + "Freebox to allow FreeOS API connection")
    parser.add_argument("-d", "--dry-run", action="store_true", help="print performance counters "
                        + "to stdout without sendig them to Prometheus ")
    parser.add_argument("-V", "--version", action="version", version='%(prog)s ' + __version__
                        + ' - ' + __date__, help="show script current version")
    args = parser.parse_args()

    # Initialize Freebox
    try:
        freebox = Freebox()
    except FreeboxError as e:
        print(e.message)
        sys.exit(1)


if __name__ == "__main__":
    # Allow remote debug with ptvsd
    if os.getenv("PYTHON_DEBUG", default="false") == "true":
        ptvsd.enable_attach()
        ptvsd.wait_for_attach()
    main()
