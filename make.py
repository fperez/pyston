#!/usr/bin/env python
"""Clone/update from github and locally install Python packages.

Usage
=====

  ./make.py  TARGET1,TARGET2  ACTION1  ACTION2 ...

TARGET is 'all' or a *comma-separated* list of targets.

ACTION defaults to 'update', which pulls from git, fully cleans all
build/installation products, and installs.


Current configuration
=====================

Valid targets:
  %(targets)s

Valid actions:
  %(actions)s

Install location directive:
  %(install)s


Customization
=============

The install location directive is controlled by the 'prefix' variable.  If set
to None, then '--user' is passed to the setup.py installation routine.
Otherwise, the value is used with the '--prefix' argument.

The list of projects to install is set in the 'projects' variable, which should
be a list of strings corresponding to project names on github.

These two variables, 'prefix' and 'projects', are set to their defaults in this
file, but can be modified by the user by defining them in a file named
'make_conf.py' located in this same directory.  A template for that file should
have been provided along with this script, but absent that, it's just a python
script that declares two variables named 'prefix' and 'projects' as indicated.

If you use the default prefix, Python will automatically find packages
installed with `--user`, but scripts will go to `~/.local/bin`.  You should
thus configure your $PATH to include this by using something such as this in
your `~/.bashrc` file::

  export PATH=$HOME/.local/bin:$PATH
  

License
=======

Released under the terms of the simplified BSD license.

Authors
=======

* John D. Hunter <jdh2358@gmail.com>, @jdh2358 at github.
* Fernando Perez <fernando.perez@berkeley.edu>, @fperez at github.
"""

#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------

from __future__ import print_function

from subprocess import check_call
import os
import sys

#-----------------------------------------------------------------------------
# Function definitions
#-----------------------------------------------------------------------------
def sh(cmd):
    print('$', cmd)
    check_call(cmd, shell=True)


def clone(targets):
    clone_template = 'git clone git://github.com/%(project)s/%(project)s.git'
    for target in targets:
        if target=='pandas':
            command = 'git clone git://github.com/wesm/pandas.git'
        else:
            command = clone_template % {'project' : target}

        if not os.path.exists(target):
            sh(command)
        else:
            print ('already have a clone of %s'%target)


def pull(targets):
    for target in targets:
        if not os.path.exists(target):
            clone([target])

        print ('pulling %s'%target)
        command = 'cd %s; git pull; cd ..'%target
        sh(command)


def install(targets):
    install_template = 'cd %s; python setup.py install %s; cd ..'

    if not os.path.isdir(site_packages):
        print('Site packages missing, making it:', site_packages)
        os.makedirs(site_packages)
        
    for target in targets:
        command = install_template % (target, install_location)
        print ('installing %s'%target)
        sh(command)


def install_clean(targets):
    for target in targets:
        command = 'rm -rf %s/%s*'%(site_packages, target)
        print ('cleaning install dir for %s: %s'%(target, command))
        sh(command)
        if target == 'matplotlib':
            print('Extra cleanup for matplotlib')
            # Special cleanup needed because matplotlib leaves things outside
            # of its package directory
            c = 'rm -rf %s/' % site_packages
            for p in ['pytz', 'dateutil', 'pylab*']:
                sh(c+p)


def update(targets):
    for target in targets:
        target = [target]
        pull(target)
        clean(target)
        install_clean(target)
        install(target)


def clean(targets):
    for target in targets:
        command = 'rm -rf %s/build'%target
        print ('cleaning %s'%target)
        sh(command)


actiond = dict( (f.__name__, f) for f in
                [clone, pull, install, clean, install_clean, update] )


def usage():
    install = install_location
    targets = sorted(projects)
    actions = sorted(actiond)
    print(__doc__ % locals())
    sys.exit(1)


def validate(given, full, type):
    bad = set(given) - set(full)
    if bad:
        print('*** ERROR ***')
        for target in bad:
            print('Bad %s=%s' % (type, target))
        usage()


#-----------------------------------------------------------------------------
# Main script
#-----------------------------------------------------------------------------

if __name__=='__main__':

    # Default configuration.  This can be overridden in teh make_conf.py file
    prefix = None  # amounts to installing with --user, to ~/.local/

    projects = ['ipython', 'numpy', 'scipy', 'matplotlib', 'sympy', 'cython',
                'pandas', 'statsmodels', 'scikit-learn', 'scikits-image' ]

    # Users can override the defaults in an (optional) make_conf.py file
    if os.path.exists('make_conf.py'):
        overrides = {}
        execfile('make_conf.py', overrides)
        prefix = overrides.get('prefix', prefix)
        projects = overrides.get('projects', projects)
        
    # Actual code execution starts here.

    # Compute location of site-packages and actual arguments for installation
    if prefix is None:
        install_location = '--user'
        prefix = '~/.local'
    else:
        install_location = '--prefix=' + prefix
        
    pythonXY = 'python%d.%d' % sys.version_info[:2]
    sp = '%s/lib/%s/site-packages' % (prefix, pythonXY)
    site_packages = os.path.expanduser(os.path.expandvars(sp))
    
    # This could be done more nicely with argparse, but that's a 2.7
    # dependency, so let's do it manually for now.
    if len(sys.argv)<2:
        usage()

    # Targets must be given
    targets = sys.argv[1].split(',')
    if targets == ['all']:
        targets = projects

    # Actions, default is to update all targets
    actions = sys.argv[2:]
    if not actions:
        actions = ['update']
        
    # Ensure all actions and targets are valid, and execute
    validate(actions, actiond, 'action')
    validate(targets, projects, 'target')

    for action in actions:
        actiond[action](targets)
