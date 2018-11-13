#!/usr/bin/env python

# Make a traffic light display current alert state from OpsGenie
# uses api v2

import signal
import sys
import time
import urllib
import urllib2
import json
import RPi.GPIO as GPIO
from settings import UPDATE_INTERVAL, RED, YELLOW, GREEN, \
        OG_API_URL, OG_API_KEY, OG_TEAMS,ON,OFF

def on(color):
    print 'on: ' + str(color)
    GPIO.output(color,ON)
    return

def off(color):
    print 'off: ' + str(color)
    GPIO.output(color,OFF)
    return

def signal_handler(signal, frame):
    print('caught sigint, exiting')
    GPIO.cleanup()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(RED,GPIO.OUT)
GPIO.setup(YELLOW,GPIO.OUT)
GPIO.setup(GREEN,GPIO.OUT)

open_request_values = {'query': 'status:open teams:' + OG_TEAMS}
acked_request_values = {'query': 'status:open acknowledged:true teams:' + OG_TEAMS}

open_request_params = urllib.urlencode(open_request_values)
acked_request_params = urllib.urlencode(acked_request_values)

# Need a GET request, so have to put em together this way rather than data param
open_request = urllib2.Request(OG_API_URL + '/?' + open_request_params)
acked_request = urllib2.Request(OG_API_URL + '/?' + acked_request_params)

open_request.add_header('Authorization','GenieKey ' + OG_API_KEY)
acked_request.add_header('Authorization','GenieKey ' + OG_API_KEY)

while True:
    try:
	try:
            json_returned = urllib2.urlopen(open_request).read()
            parsed_json = json.loads(json_returned)
            print json_returned
            if parsed_json['data']['count'] == 0:
                off(RED)
                off(YELLOW)
                on(GREEN)
                print "green"
            else:
                json_returned = urllib2.urlopen(acked_request).read()
                parsed_json = json.loads(json_returned)
                if parsed_json['data']['count'] == 0:
                    off(GREEN)
                    off(YELLOW)
                    on(RED)
                    print "red"
                else:
                    off(GREEN)
                    off(RED)
                    on(YELLOW)
                    print "yellow"
        except urllib2.URLError,e:
            print e.reason
            off(RED)
            off(YELLOW)
            off(GREEN)
    except urllib2.HTTPError,e:
        print e.code
        off(RED)
        off(YELLOW)
        off(GREEN)
    time.sleep(UPDATE_INTERVAL)

GPIO.cleanup()
