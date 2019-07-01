#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
    Name: fbxmetrics.py
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
        Timeout for freebox discovery as parameter
        Loggin
        Raw output for counters
        Push gateway server address and port as arguments
        Metrics prefix as argument
"""
import os
import sys
import argparse
import ptvsd
from fbxerrors import FreeboxError
from fbx import Freebox

__version_info__ = ('0', '0', '1')
__version__ = '.'.join(__version_info__)
__date__ = "2019-06-30"
__author__ = "Denis Lambolez"
__contact__ = "denis.lambolez@gmail.com"
__license__ = "MIT"

APP_NAME = "FreeProbe"


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

    # Register app to freebox if requested and exit
    if args.register:
        try:
            freebox.register(APP_NAME, __version__)
        except FreeboxError as e:
            print(e.message)
            sys.exit(1)
    # Get metrics from freebox, push them to push_gatewayif requested and exit
    else:
        try:
            freebox.get_metrics()
        except FreeboxError as e:
            print(e.message)
            sys.exit(1)


if __name__ == "__main__":
    # Allow remote debug with ptvsd
    if os.getenv("PYTHON_DEBUG", default="false") == "true":
        ptvsd.enable_attach()
        ptvsd.wait_for_attach()
    main()
