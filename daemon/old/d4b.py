#!/usr/bin/python

import sys
import time
import signal
import copy
import argparse
import ConfigParser
import sdnotify

from sense_hat import SenseHat

# # # # # # # # # #

default_opts = {
	'foo': '1',
	'bar': '2',
	'flag': False,
	'verbose': 0,
	'delay': '10'    # this is str for now, will convert to int later
}
opts = copy.deepcopy( default_opts )

# # # # # # # # # #

# initialize some sub-systems
sensor = SenseHat()
sdn = sdnotify.SystemdNotifier()

# get command line args
parser = argparse.ArgumentParser(
	description = 'Periodically read temperature and humidity sensors',
	epilog = 'More info here'
)
parser.add_argument( '-c', default='/home/pi/code/d4.cfg', help='read from config file' )
parser.add_argument( '-d', help='set delay (S sec, MM:SS min:sec)' )
parser.add_argument( '-f', action='store_true', help='set flag' )
parser.add_argument( '-v', action='count', default=0, help='verbose output' )
parser.add_argument( '-V', action='count', default=0, help='really verbose output' )
args = parser.parse_args()

# process the config file
def process_config_file():
	global opts
	# overwrite old data so we always know what's in there
	opts = copy.deepcopy( default_opts )
	# read config file
	config = ConfigParser.ConfigParser()
	try:
		print( 'reading config file '+args.c )
		config.read( args.c )
	except:
		print( '* Error in cfg file' )

	# now overwrite config file with cmdline args
	if( args.f is not None ):
		opts['flag'] = args.f
	elif( config.has_option('Main','flag') ):
		opts['flag'] = config.get('Main','flag')
	if( args.d is not None ):
		opts['delay'] = args.d
	elif( config.has_option('Main','delay') ):
		opts['delay'] = config.get('Main','delay')
	if( (args.v > 0) or (args.V > 0) ):
		opts['verbose'] = int(args.v) + 10*int(args.V)
	elif( config.has_option('Main','verbose') ):
		opts['verbose'] = int(config.get('Main','verbose'))

	# now convert some options to more useful values
	x = opts['delay']
	if( ':' in x ):
		# hh:mm:ss or mm:ss format .. convert to seconds
		i = x.find(':')
		if( ':' in x[i+1:] ):
			j = x.find(':',i+1 )
			v = 60*60*int(x[:i]) + 60*int(x[i+1:j]) + int(x[j+1:])
		else:
			v = 60*int(x[:i]) + int(x[i+1:])
		opts['delay'] = v
	else:
		opts['delay'] = int(opts['delay'])

	if( opts['verbose'] > 10 ):
		for k,v in opts.iteritems():
			print "k="+k+"  v="+str(v)+" ("+str(type(v))+")"
		print( "args=", args )

	# every time we process the config file, we can
	# force the imu sensors to be "off"
	sensor.set_imu_config( False, False, False )

# process the config/cmd line arg info
process_config_file()

# # # # # # # # # #

# per systemd specs, can prepend "<0>" to "<7>" to set log-level
#    0=EMERG, 1=ALERT, 2=CRIT, 3=ERR, 4=WARNING, 5=NOTICE, 6=INFO, 7=DEBUG,
#    or just let systemd/service file handle that instead
def log_data( humantime ):
	temp = sensor.get_temperature()
	humid = sensor.get_humidity()
	temp2 = sensor.get_temperature_from_pressure()
	pressure = sensor.get_pressure()
	orientation = sensor.get_orientation()
	#orientation = sensor.get_gyroscope()

	#+ " pitch=" + str(orientation['pitch']) \
	#+ " roll=" + str(orientation['roll']) \
	#+ " yaw=" + str(orientation['yaw']) \
	msg = "temp=" + str(temp) + " humidity=" + str(humid) \
		+ " temp2=" + str(temp2) + " pressure="+ str(pressure) \
		+ "\n"
	sys.stderr.write( msg )

# # # # # # # # # #

# prep some signal handlers
# - to keep signal handlers small, we just set a global var
last_signal = 0
def simple_handler( signum, frame ):
	global last_signal
	last_signal = signum

signal.signal( signal.SIGUSR1, simple_handler )
signal.signal( signal.SIGUSR2, simple_handler )
# under systemd, SIGHUP should force a reload of the config file
signal.signal( signal.SIGHUP, simple_handler )
# under systemd, SIGTERM should terminate the process
signal.signal( signal.SIGTERM, simple_handler )

#signal.signal( signal.SIGINT, signal.SIG_IGN )
#signal.signal( signal.SIGQUIT, signal.SIG_IGN )
#signal.signal( signal.SIGPIPE, signal.SIG_IGN )
#signal.signal( signal.SIGTSTP, signal.SIG_IGN )

# TODO: there is a slight race condition that could miss signals
#   sent while the non-time.sleep code is running; e.g. USR2 arrives
#   immediately after last_signal=0 ... it will wait one cycle before
#   reloading config; if USR1 arrives during process_config_file, it
#   may be ignored
#   WORKAROUND: issue the signal multiple times?

# # # # # # # # # # # # # # # # # # # #
## # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # #

sdn.notify( "READY=1" )


#
# MAIN LOOP:
last_unixtime = time.time()
while True:
	# get current time
	unixtime = time.time()
	humantime = time.strftime( '%Y-%m-%d %H:%M:%S' )

	# if we woke from a signal, deltatime != delay time
	deltatime = unixtime - last_unixtime

	# read the sensors and log the data
	log_data( humantime )

	# sleep until next iteration
	time.sleep( opts['delay'] )

	# did we wake due to signal handler?
	if( last_signal == signal.SIGUSR2 ):
		sdn.notify( "RELOADING=1" )
		process_config_file()
		sdn.notify( "READY=1" )
	elif( last_signal == signal.SIGTERM ):
		break
	last_signal = 0

	last_unixtime = unixtime

sdn.notify( "STOPPING=1" )
