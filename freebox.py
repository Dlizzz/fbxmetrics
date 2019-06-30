#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Define the Freebox

Name: freebox.py
Classes:
    Freebox: freebox object
"""

import os
import sys
import time
import requests
import platform
import json
from requests import HTTPError
from zeroconf import Zeroconf, ServiceBrowser
from freeerrors import FreeboxError


METRICS_PREFIXE = "freebox_"
PUSHGATEWAY_ADDRESS = "prometheus.catsnet.home"
PUSHGATEWAY_PORT = "9091"


class Freebox(object):
    """Definition of the Freebox server

    Constants:
        _TYPE: private - string - The Freebox broadcasts the “_fbx-api._tcp” service
    Attributes:
        _mds_listener: private - MDNSListener - provide callback function for mDNS service browser
        _properties: private - dict - All properties of the Freebox
            name: string - Fully qualified name of the service
            addresse: string - IP addresse of service
            port: integer - port of the service
            server: string - name of the server
            type: string - type of the service
            api_version: string - The current API version on the Freebox
            device_type: string - “FreeboxServerx,y” for the Freebox Server revision w,y
            api_base_url: string - The API root path on the HTTP server
            uid: string - The device unique id
            api_domain: string - The domain to use in place of hardcoded Freebox ip
            https_available: string - Tells if https has been configured on the Freebox
            https_port: string - Port to use for remote https access to the Freebox Api
            box_model: string - model of the Freebox
            box_model_name: string - model name of the freebox
    Properties:
        properties: dict, ro - provide access to Freebox properties
    Methods:
        _full_api_url: private - return a full url for the given api url
        register: register app to the freebox
        get_metrics: get metrics from the freebox
        push_metrics: push metrics to the prometheus push gateway
        print_metrics: print metrics to stdout 
    Exceptions:
        FreeboxError - Don't find a Freebox on the local network
    """

    # From API docuemntation "https://dev.freebox.fr/sdk/os/" service name is “_fbx-api._tcp”
    # zeroconf requests to have ".local." at the end of service name
    _TYPE = "_fbx-api._tcp.local."

    class MDNSListener():
        """Callback class to get information of the available MDNS service

        Attributes:
            _freebox: private - Freebox - Access to Freebox parent instance 
        """

        def __init__(self, freebox):
            """Constructor

            Arguments:
                freebox: Freebox - Freebox to discover  
            """

            self._freebox = freebox

        def add_service(self, zeroconf, stype, name):
            """Callback when service is added. Get service info"""

            info = zeroconf.get_service_info(stype, name)

            # Store freebox properties in Freebox parent instance
            if info is not None:
                self._freebox.properties["name"] = info.name
                self._freebox.properties["type"] = info.type
                self._freebox.properties["server"] = info.server
                self._freebox.properties["port"] = info.port
                self._freebox.properties["address"] = (
                    str(info.address[0])
                    + "." + str(info.address[1])
                    + "." + str(info.address[2])
                    + "." + str(info.address[3])
                )
                for key, value in info.properties.items():
                    self._freebox.properties[key.decode()] = value.decode()

    def __init__(self):
        """Initialize the Freebox through mDNS discovery

        Exceptions:
            ConnectionError - Don't find a Freebox on the local network
        """

        self._mdns_listener = Freebox.MDNSListener(self)
        self._properties = {}

        zeroconf = Zeroconf()
        # Launch the browser thread with the service type
        browser = ServiceBrowser(zeroconf, self._TYPE, self._mdns_listener)
        # Allow one second for the browser thread to find the Freebox
        time.sleep(2)
        # Cancel the browser thread and close zeroconf
        browser.cancel()
        zeroconf.close()

        if not self._properties:
            raise FreeboxError(
                "Fatal: Unable to find a Freebox on the local network!")

    def _full_api_url(self, api_url):
        """Provide fully qualified url for the given api url

        Arguments:
            api_url: string - the api url
        Return:
            string - the fully qualified https url
        """

        url = (
            "https://"
            + self.properties["api_domain"]
#            + ":" + str(self.properties["port"])
            + self.properties["api_base_url"]
            + "v" + self.properties["api_version"].split(".")[0]
            + api_url
        )
        return url

    def register(self, app_name, app_version):
        """Register the app to the freebox and store the recieved token in secured file

        Arguments:
            app_name: string - name of the application for registration
            app_version: string - version of the application for registration
        Exceptions:
            ConnectionError - Can't connect to the freebox
        """

        # Post request for authorization
        url = self._full_api_url("/login/authorize/")
        data = {
            "app_id": "fr.freebox." + app_name.lower(),
            "app_name": app_name,
            "app_version": app_version,
            "device_name": platform.node()
        }
        ssl_dir = os.path.dirname(os.path.realpath(sys.argv[0])) + "/ssl"
        r = requests.post(url, json.dumps(data))
        return 

    def get_metrics(self):
        pass

    def push_metrics(self):
        pass

    def print_metrics(self):
        pass

    @property
    def properties(self):
        return self._properties
