#!/usr/bin/env python
import signal
import sys
import time
import urllib
import urllib2
#import RPi.GPIO as GPIO
from settings import UPDATE_INTERVAL,RED,YELLOW,GREEN, \
        PD_API_URL,PD_API_TOKEN,PD_TEAMS,ON,OFF

def on(color):
    print 'on: ' + str(color)
    #GPIO.output(color,ON)
    return

def off(color):
    print 'off: ' + str(color)
    #GPIO.output(color,OFF)
    return

def signal_handler(signal, frame):
    print('caught sigint, exiting')
    #GPIO.cleanup()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

#GPIO.setmode(GPIO.BOARD)
#GPIO.setup(RED,GPIO.OUT)
#GPIO.setup(YELLOW,GPIO.OUT)
#GPIO.setup(GREEN,GPIO.OUT)

triggered_request_values = {'status': 'triggered',
                            'teams': PD_TEAMS }
acked_request_values = {'status': 'acknowledged',
                        'teams': PD_TEAMS }

triggered_request_params = urllib.urlencode(triggered_request_values)
acked_request_params = urllib.urlencode(acked_request_values)

# Need a GET request, so have to put em together this way rather than data param
triggered_request = urllib2.Request(PD_API_URL + '/?' + triggered_request_params)
acked_request = urllib2.Request(PD_API_URL + '/?' + acked_request_params)

# Must ask for json!
triggered_request.add_header('Content-type', 'application/json')
triggered_request.add_header('Authorization', 'Token token=' + PD_API_TOKEN)

acked_request.add_header('Content-type', 'application/json')
acked_request.add_header('Authorization', 'Token token=' + PD_API_TOKEN)

while True:
    try:
        json_returned = urllib2.urlopen(triggered_request).read()
    except urllib2.HTTPError,e:
        print e.code
        # turn all lights off
        # off(RED)
        # off(YELLOW)
        # off(GREEN)
    time.sleep(UPDATE_INTERVAL)

#GPIO.cleanup()
