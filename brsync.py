#!/usr/bin/env python3

import os
import sys
import yaml   # PyYAML: use pip3 to install it
import subprocess

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

# Sample config file (.rsync):
#  ---
#  #source: defaults to the current directory
#  dst: dell:Code/RsyncWorkarea/
#  exclude:
#  - .mypy_cache
#  - .rsync
#  run: 'ls -l'
#  run_make: 'cd BLD && make x86'
#  ...

class  Rsync():
    'Perform rsync between the CWD and the remote directory listed in the config file.'
    def __init__( self, fname ):
        self.exclude = []
        self.run_cmd = ''
        self.command = [ 'rsync',   '--progress',  '--compress', '--recursive', '--times',
                         '--perms', '--links',     '--delete',   '--cvs-exclude' ]
        self.src_dir = os.path.dirname( fname ) + '/'
        # read configuration from the file
        with open( fname, 'rt' ) as infile:
            data = yaml.load( infile, Loader=Loader )
            self.dst_dir = data[ 'dst' ]
            if 'exclude' in data:
                for excl in data[ 'exclude' ]:
                    self.command.append( '--exclude=' + excl )
            if 'run' in data:
                self.run_cmd = data[ 'run' ]

    def sync( self ):
        'Run rsync using settings from config file'
        self.command.extend( [self.src_dir, self.dst_dir] )
        cout = subprocess.Popen( self.command, stderr=subprocess.STDOUT, stdout=subprocess.PIPE )
        for line in cout.stdout:
            print( line.decode('utf-8' ), end='' )
        self.run()

    def run( self ):
        'If config file contains "run" command - run it on remote box'
        if len( self.run_cmd ) < 2:
            return
        host, remote_dir = self.dst_dir.split( ':' )
        cout = subprocess.Popen( [ 'ssh', host, 'cd ' + remote_dir + ' && ' + self.run_cmd ], stderr=subprocess.STDOUT, stdout=subprocess.PIPE )
        for line in cout.stdout:
            print( line.decode('utf-8' ), end='' )

def get_cmd_line_args():   # FIXME not used
    'Get command line arguments FIXME from Freecycle'
    # vidi file:///usr/share/doc/python-doc/html/library/argparse.html#module-argparse
    cmdline = argparse.ArgumentParser( description='Check for emails from Freecycle' )
    cmdline.add_argument( '-d', '--delay', type=int, default=120,
                          help='delay (in seconds) between two consecutive runs; default: 120s' )
    cmdline.add_argument( '-k', '--keep-running', type=bool, default=True,
                          help='run continuously when True, run once when False; default: True' )
    return cmdline.parse_args()


def get_config_file( cfg_fname ):
    '''Search up the directory tree for config file 'cfg_fname', return its full path.
    Exit if nothing found.
    '''
    cwd = os.getcwd()
    while True:
        full_path = os.path.join( cwd, cfg_fname )
        if os.path.exists( full_path ):
            print( 'Found', full_path )
            return full_path
        cwd = os.path.abspath( os.path.join( cwd, '..' ) )
        if cwd == '/':
            print( "\nERROR: didn't find config file %s\nExiting" % cfg_fname )
            sys.exit( 1 )



rsync = Rsync( get_config_file( '.rsync') )
rsync.sync()


# vidi Bacikutija/Posal/Ali/bin_egm/bb_rsync.sh

# FIXME trailing whitespace
#
