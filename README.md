# Monitoring Plugin: Radius

### Description
For usage with nagios compatible monitoring systems (nagios, icinga, icinga2 etc.).
Check if authentication with given credentials on a radius server is working (and if its fast enough)

### Usage
usage: check_radius [-h] -s RADIUS_SERVER -u USERNAME -p PASSWORD -S
                    SHARED_SECRET [-n NAS_IDENTIFIER] [-c SECONDS]
                    [-t SECONDS] [-w SECONDS] [-r RETRIES] [-v]

arguments:
  -h, --help         show this help message and exit
  -s RADIUS_SERVER   radius server to check
  -u USERNAME        username to use for authentication
  -p PASSWORD        password to use for authentication
  -S SHARED_SECRET   shared secret between client and server
  -n NAS_IDENTIFIER  NAS identifier to use for authentication
  -c SECONDS         threshold for critical in SECONDS
  -t SECONDS         SECONDS to wait for an answer
  -w SECONDS         threshold for warning in SECONDS
  -r RETRIES         number of times to retry connection to radius
  -v                 verbose output


### Example
```
./check_radius -s radius.example.org -u testuser -p testpassword -S secret
OK - access granted | elapsed=0.02
```

### Build
```
./build.sh
```

### Install
* Copy check_radius to all your servers
* create a service/exec in your monitoring engine to execute the remote check
