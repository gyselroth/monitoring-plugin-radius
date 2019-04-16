#!/bin/python
import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/dependencies')
import pkg_resources
import time
from pyrad.client import Client, Timeout
from pyrad.dictionary import Dictionary
import pyrad.packet
from argparse import ArgumentParser

CRITICAL = 10
WARNING = 5
TIMEOUT = 5
RETRIES = 3
NASID = 'localhost'

def ok(message, elapsed):
  print('OK - ' + message + ' | elapsed=' + str(elapsed))
  exit(0)

def warning(message, elapsed):
  print('WARNING - ' + message + ' | elapsed=' + str(elapsed))
  exit(1)

def critical(message, elapsed):
  print('CRITICAL - ' + message + ' | elapsed=' + str(elapsed))
  exit(2)

def unknown(message, elapsed):
  print('UNKNOWN - ' + message + ' | elapsed=' + str(elapsed))
  exit(3)

def verboseOut(verbose, message):
  if verbose:
    print(message)

def elapsed(start):
  return time.time() - start

def main(argv):
  # Parse arguments
  parser = ArgumentParser()
  parser.add_argument('-s', dest='radius_server', required=True, help='radius server to check', metavar='RADIUS_SERVER')
  parser.add_argument('-u', dest='username', required=True, help='username to use for authentication', metavar='USERNAME')
  parser.add_argument('-p', dest='password', required=True, help='password to use for authentication', metavar='PASSWORD')
  parser.add_argument('-S', dest='shared_secret', required=True, help='shared secret between client and server', metavar='SHARED_SECRET')
  parser.add_argument('-n', dest='nasId', default=NASID, help='NAS identifier to use for authentication', metavar='NAS_IDENTIFIER')
  parser.add_argument('-c', dest='criticalThreshold', type=int, default=CRITICAL, help='threshold for critical in SECONDS', metavar='SECONDS')
  parser.add_argument('-t', dest='timeout', type=int, default=TIMEOUT, help='SECONDS to wait for an answer', metavar='SECONDS')
  parser.add_argument('-w', dest='warningThreshold', type=int, default=WARNING, help='threshold for warning in SECONDS', metavar='SECONDS')
  parser.add_argument('-r', dest='retries', type=int, default=RETRIES, help='number of times to retry connection to radius', metavar='RETRIES')
  parser.add_argument('-v', dest='verbose', default=False, help='verbose output', action='store_true')
  args = parser.parse_args()

  srv = Client(
    server=args.radius_server, secret=args.shared_secret.encode(),
    dict=Dictionary(pkg_resources.resource_stream('dependencies', 'dictionary')),
  )
  srv.timeout = args.timeout
  srv.retries = args.retries

  # create request
  request = srv.CreateAuthPacket(code=pyrad.packet.AccessRequest,
                             User_Name=args.username, NAS_Identifier=args.nasId)
  request["User-Password"] = request.PwCrypt(args.password)

  start = time.time()
  try:
    # send request
    response = srv.SendPacket(request)
  except Timeout as e:
    critical('radius timeout occured', elapsed(start))
  except Exception as e:
    critical('connection error: ' + str(e), elapsed(start))

  if response.code == pyrad.packet.AccessAccept:
    if elapsed(start) >= args.criticalThreshold:
      critical('access granted, but request took too long', elapsed(start))
    if elapsed(start) >= args.warningThreshold:
      warning('access granted, but request took too long', elapsed(start))
    ok('access granted', elapsed(start))
  if response.code == pyrad.packet.AccessReject:
    critical('access rejected', elapsed(start))
  else:
    unknown('radius response code: ' + str(response.code), elapsed(start));

if __name__ == "__main__":
  main(sys.argv)
