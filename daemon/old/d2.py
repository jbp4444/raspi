#!/opt/local/bin/python

import time
import signal
import argparse
import ConfigParser

# get command line args
parser = argparse.ArgumentParser(
	description = 'Periodically read temperature and humidity sensors',
	epilog = 'More info here'
)
parser.add_argument( '-c', default='d2.cfg', help='read from config file' )
parser.add_argument( '-d', help='set delay (S sec, MM:SS min:sec)' )
parser.add_argument( '-f', action='store_true', help='set flag' )
parser.add_argument( '-v', action='count', default=0, help='verbose output' )
args = parser.parse_args()
print( args )

# read config file
# -- list ALL possible options here
config = ConfigParser.SafeConfigParser({
	'foo': '1',
	'bar': '2',
	'flag': False,
	'delay': '10'
})
try:
	print( 'reading config file '+args.c )
	config.read( args.c )
except:
	print( '* Error in cfg file' )

# now overwrite config file with cmdline args
if( args.f is not None ):
	config.set( 'Main', 'flag', str(args.f) )
if( args.d is not None ):
	config.set( 'Main', 'delay', args.d )

#print "foo=["+config.get( 'Main', 'foo' )+"]"
#print "bar=["+config.get( 'Main', 'bar' )+"]"
#print "flag=["+config.get( 'Main', 'flag' )+"]"
#print "delay=["+config.get( 'Main', 'delay' )+"]"

# now convert some options to more useful values
x = config.get( 'Main', 'delay' )
if( ':' in x ):
	# hh:mm:ss or mm:ss format .. convert to seconds
	i = x.find(':')
	if( ':' in x[i+1:] ):
		j = x.find(':',i+1 )
		v = 60*60*int(x[:i]) + 60*int(x[i+1:j]) + int(x[j+1:])
	else:
		v = 60*int(x[:i]) + int(x[i+1:])
	config.set( 'Main', 'delay', str(v) )

#print "delay2=["+config.get( 'Main', 'delay' )+"] = " + str(config.getint('Main','delay'))

# prep some signal handlers
def handler_USR1( signum, frame ):
	# this no-op function will abort time.sleep in the main loop
	pass
signal.signal( signal.SIGUSR1, handler_USR1 )

#
# MAIN LOOP:
last_unixtime = time.time()
while True:
	# get current time
	unixtime = time.time()
	humantime = time.strftime( '%Y-%m-%d %H:%M:%S' )
	deltatime = unixtime - last_unixtime

	# read the sensors
	print( humantime+" temp=100 humidity=100" )

	# sleep until next iteration
	last_unixtime = unixtime
	time.sleep( config.getint('Main','delay') )
