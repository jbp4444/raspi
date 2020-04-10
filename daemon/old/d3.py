#!/opt/local/bin/python

import time
import signal
import os
import syslog
import argparse
import ConfigParser

# get command line args
parser = argparse.ArgumentParser(
	description = 'Periodically read temperature and humidity sensors',
	epilog = 'More info here'
)
parser.add_argument( '-c', default='_DEFAULT', help='read from config file' )
parser.add_argument( '-d', help='set delay (S sec, MM:SS min:sec)' )
parser.add_argument( '-f', action='store_true', help='set flag' )
parser.add_argument( '-v', action='count', default=0, help='verbose output' )
parser.add_argument( '-V', action='count', default=0, help='really verbose output' )
args = parser.parse_args()

syslog_levels = {
	'LOG_EMERG':   syslog.LOG_EMERG,
	'LOG_ALERT':   syslog.LOG_ALERT,
	'LOG_CRIT':    syslog.LOG_CRIT,
	'LOG_ERR':     syslog.LOG_ERR,
	'LOG_WARNING': syslog.LOG_WARNING,
	'LOG_NOTICE':  syslog.LOG_NOTICE,
	'LOG_INFO':    syslog.LOG_INFO,
	'LOG_DEBUG':   syslog.LOG_DEBUG
}
syslog_facilities = {
	'LOG_USER':   syslog.LOG_USER,
	'LOG_LOCAL0': syslog.LOG_LOCAL0,
	'LOG_LOCAL1': syslog.LOG_LOCAL1,
	'LOG_LOCAL2': syslog.LOG_LOCAL2,
	'LOG_LOCAL3': syslog.LOG_LOCAL3,
	'LOG_LOCAL4': syslog.LOG_LOCAL4,
	'LOG_LOCAL5': syslog.LOG_LOCAL5,
	'LOG_LOCAL6': syslog.LOG_LOCAL6,
	'LOG_LOCAL7': syslog.LOG_LOCAL7
}

opts = {
	'foo': '1',
	'bar': '2',
	'flag': False,
	'verbose': 0,
	'delay': '10',    # this is str for now, will convert to int later
	'log_enabled': False,
	'facility': 'LOG_LOCAL1',
	'identity': 'foobarbaz',
	'level': 'LOG_DEBUG'
}

def process_config_file():
	global opts
	opts = {              # overwrite old data so we always know what's in there
		'foo': '1',
		'bar': '2',
		'flag': False,
		'verbose': 0,
		'delay': '10',    # this is str for now, will convert to int later
		'log_enabled': False,
		'facility': 'LOG_LOCAL1',
		'identity': 'foobarbaz',
		'level': 'LOG_DEBUG'
	}
	# read config file
	config = ConfigParser.ConfigParser()
	cfg_file = 'd3.cfg'
	if( args.c == '_DEFAULT' ):
		if( os.getenv('D3_CONFIG') is not None ):
			cfg_file = os.environ['D3_CONFIG']
	else:
		cfg_file = args.c
	try:
		print( 'reading config file '+cfg_file )
		config.read( cfg_file )
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

	if( config.has_option('Logging','facility') ):
		opts['facility'] = config.get('Logging','facility')
	if( config.has_option('Logging','identity') ):
		opts['identity'] = config.get('Logging','identity')
	if( config.has_option('Logging','level') ):
		opts['level'] = config.get('Logging','level')
	if( config.has_option('Logging','enabled') ):
		opts['log_enabled'] = config.get('Logging','enabled')

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

	if( opts['level'] not in syslog_levels.keys() ):
		# TODO: this is an error - improper selection - how to alert?
		opts['level'] = 'LOG_INFO'
	if( opts['facility'] not in syslog_facilities.keys() ):
		# TODO: this is an error - improper selection - how to alert?
		opts['facility'] = 'LOG_LOCAL0'

	if( opts['verbose'] > 10 ):
		for k,v in opts.iteritems():
			print "k="+k+"  v="+str(v)+" ("+str(type(v))+")"
		print( "args=", args )


def enable_logging():
	syslog.closelog()
	if( opts['log_enabled'] ):
		facility = syslog_facilities[ opts['facility'] ]
		syslog.openlog( opts['identity'], syslog.LOG_NDELAY, facility )

def log_data( temp, humid ):
	if( opts['log_enabled'] ):
		level = syslog_levels[ opts['level'] ]
		msg = " temp=" + str(temp) + " humidity=" + str(humid)
		syslog.syslog( level, msg )

# process the config/cmd line arg info
process_config_file()
# start up logging
enable_logging()

# prep some signal handlers
# - to keep signal handlers small, we just set a global var
last_signal = 0
def simple_handler( signum, frame ):
	global last_signal
	last_signal = signum

signal.signal( signal.SIGUSR1, simple_handler )
signal.signal( signal.SIGUSR2, simple_handler )

# under systemd, SIGHUP should force a reload of the config file
#signal.signal( signal.SIGHUP, signal.SIG_IGN )

#signal.signal( signal.SIGINT, signal.SIG_IGN )
#signal.signal( signal.SIGQUIT, signal.SIG_IGN )
#signal.signal( signal.SIGPIPE, signal.SIG_IGN )
#signal.signal( signal.SIGTERM, signal.SIG_IGN )
#signal.signal( signal.SIGTSTP, signal.SIG_IGN )

# TODO: there is a slight race condition that could miss signals
#   sent while the non-time.sleep code is running; e.g. USR2 arrives
#   immediately after last_signal=0 ... it will wait one cycle before
#   reloading config; if USR1 arrives during process_config_file, it
#   may be ignored
#   WORKAROUND: issue the signal multiple times?

#
# MAIN LOOP:
last_unixtime = time.time()
while True:
	# get current time
	unixtime = time.time()
	humantime = time.strftime( '%Y-%m-%d %H:%M:%S' )

	# if we woke from a signal, deltatime != delay time
	deltatime = unixtime - last_unixtime

	# read the sensors
	if( opts['verbose'] > 1 ):
		print( humantime+" temp=100 humidity=100" )
	# and log the data
	log_data( 100, 100 )

	# sleep until next iteration
	time.sleep( opts['delay'] )

	# did we wake due to signal handler?
	if( last_signal == signal.SIGUSR2 ):
		process_config_file()
		enable_logging()
	#elif( last_signal == signal.SIGUSR1 ):
	#	pass
	last_signal = 0

	last_unixtime = unixtime
