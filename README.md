# fbxmetrics
Connect to Freebox and retrieve various performance counters to push them to Prometheus push gateway

## Arguments
    -r, --register: register freeprobe in Freebox (allow FreeOS API connection) and exit
    -d, --dr-run: print performance counters to stdout without sendig them to Prometheus push-gateway
    -h, --help: print usage on stdout
    -V, --version : print script version on stdout
       
## Requirements
    The Prometheus "push-gateway" must be installed and configured (address and port)
    For security reason the script must be executed as root

## Todo
    1. Raw output for counters
    2. Push gateway server address and port as arguments
    3. Metrics prefix as argument

## Dependencies
* Python libraries
  * requests -- The only Non-GMO HTTP library for Python, safe for human consumption. Used for all 
  API calls
  * zeroconf -- This is fork of pyzeroconf, Multicast DNS Service Discovery for Python, originally 
  by Paul Scott-Murphy. Used for Freebox discovery
