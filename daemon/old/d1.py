#!/opt/local/bin/python

import os
import grp
import signal
import daemon
#import lockfile

#from spam import (
#    initial_program_setup,
#    do_main_program,
#    program_cleanup,
#    reload_program_config,
#    )

context = daemon.DaemonContext(
    working_directory='./foo',   #/var/lib/foo,
    umask=0o002,
    #pidfile=lockfile.FileLock('./foo.pid'),  # '/var/run/spam.pid'
	pidfile = './foo.pid'
    )

context.signal_map = {
    signal.SIGTERM: program_cleanup,
    signal.SIGHUP: 'terminate',
    signal.SIGUSR1: reload_program_config,
    }

mail_gid = grp.getgrnam('mail').gr_gid
context.gid = mail_gid

important_file = open('spam.data', 'w')
interesting_file = open('eggs.data', 'w')
context.files_preserve = [important_file, interesting_file]

#initial_program_setup()

with context:
    #do_main_program()
	print( "foo" )
