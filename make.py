#!/usr/bin/env python
"""Clone/update from github and locally install Python packages.

Purpose
=======

This is a simple tool meant to easily manage a collection of github-hosted
python packages from source, so that it's quick to clone, build, install and
update them with a simple command.


Usage
=====

  ./make.py  TARGET1,TARGET2  ACTION1  ACTION2 ...

TARGET is 'all' or a *comma-separated* list of targets.

ACTION defaults to `update`, which pulls from git, fully cleans all
build/installation products, and installs.


The simplest way to use it is to 

Afterwards, this::

    ./make.py all

will run a full update of all packages (i.e. pull from git, remove previous
build/install, rebuild from scratch and reinstall).  Individual packages can be
updated::

    ./make.py numpy,scipy

and if you want finer control (for example, pull from github and install
without removing previous build/installation data)::

    ./make.py all pull install

You can also clone and install any project that's hosted on github with a URL
of the pattern ``github.com/PROJECT/PROJECT`` with::

    ./make.py PROJECT clone install

even if it is not listed on the default project list.  And since all locally
available packages (directories with ``.git`` and ``setup.py``) are
automatically loaded, you can use this tool to continue updating them without
need for further customization.
    
The general syntax is::
    
    ./make.py  TARGET1,TARGET2  ACTION1  ACTION2 ...

    
Customization
=============

The install location directive is controlled by the ``prefix`` variable.  If
set to None, then ``--user`` is passed to the setup.py installation routine.
Otherwise, the value is used with the ``--prefix`` argument.  If you define the
*environment* variable called ``PREFIX``, it will be used as the value for
``prefix``.

The list of projects to install is set in the ``projects`` variable, which
should be a list of strings corresponding to project names on github.  This
list is automatically updated with any other paths that contain a ``.git``
subdirectory *and* a ``setup.py`` file.  You can therefore manually clone any
other github python projects you want and they will be automatically picked up
as well, without having to update the ``projects`` list by hand each time
(updating the default ``projects`` is only needed for the ``clone`` action).

These two variables, ``prefix`` and ``projects``, are set to their defaults in
this file, but can be modified by the user by defining them in a file named
``make_conf.py`` located in this same directory (a file overrides also the
``PREFIX`` environment variable).  A template for that file should have been
provided along with this script, but absent that, it's just a python script
that declares two variables named ``prefix`` and ``projects`` as indicated.

If you use the default prefix, Python will automatically find packages
installed with ``--user``, but scripts will go to ``~/.local/bin``.  You should
thus configure your $PATH to include this by using something such as this in
your ``~/.bashrc`` file::

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
# Utility functions
#-----------------------------------------------------------------------------

def sh(cmd):
    print('$', cmd)
    check_call(cmd, shell=True)


def usage():
    install = install_location
    targets = sorted(projects)
    actions = sorted(actiond)
    config = """
Current configuration
=====================

Valid targets:
  %(targets)s

Valid actions:
  %(actions)s

Install location directive:
  %(install)s
"""  % locals()
    print(__doc__)
    print(config)
    sys.exit(1)


def validate(given, full, type):
    bad = set(given) - set(full)
    if bad:
        print('*** ERROR ***')
        for target in bad:
            print('Bad %s=%s' % (type, target))
        usage()


def update_projects():
    """Update the global `projects` list with repos in the current directory"""

    local_projects = []
    for root, dirs, files in os.walk('.', followlinks=True):
        if root != '.':
            # Avoid recursing deeper, we only want to look at the top-level
            break
        # Only check for things not already in the projects list
        for d in set(dirs) - set(projects):
            if os.path.isdir('%s/.git' % d) and \
               os.path.isfile('%s/setup.py' % d):
                local_projects.append(d)
    projects.extend(local_projects)


#-----------------------------------------------------------------------------
# Action definitions
#-----------------------------------------------------------------------------

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
            print ('already have a clone of %s' % target)


def pull(targets):
    for target in targets:
        if not os.path.exists(target):
            clone([target])

        print ('pulling %s'%target)
        command = 'cd %s; git pull; cd ..' % target
        sh(command)


def install(targets):
    install_template = 'cd %s; python setup.py install %s; cd ..'

    if not os.path.isdir(site_packages):
        print('Site packages missing, making it:', site_packages)
        os.makedirs(site_packages)
        
    for target in targets:
        command = install_template % (target, install_location)
        print ('installing %s' % target)
        sh(command)


def install_clean(targets):
    base = 'rm -rf %s/' % site_packages
    for target in targets:
        command = base + target
        print ('cleaning install dir for %s: %s' % (target, command))
        sh(command)
        sh(command + '*.egg*')
        # Special cleanups for certain projects with different naming
        # conventions or that leave things outside their main package dir
        if target == 'matplotlib':
            for p in ['pytz', 'dateutil', 'pylab*', 'mpl_toolkits']:
                sh(base+p)
        elif target == 'cython':
            sh(base+'Cython*')
            sh(base+'pyximport')


def update(targets):
    for target in targets:
        target = [target]
        pull(target)
        clean(target)
        install_clean(target)
        install(target)


def clean(targets):
    for target in targets:
        command = 'rm -rf %s/build' % target
        print ('cleaning %s' % target)
        sh(command)

#-----------------------------------------------------------------------------
# Main script
#-----------------------------------------------------------------------------

if __name__=='__main__':

    # Default configuration.  This can be overridden in the make_conf.py file.
    # None amounts to installing with --user, which puts things in ~/.local/.
    prefix = os.environ.get('PREFIX')

    projects = ['ipython', 'numpy', 'scipy', 'matplotlib', 'sympy', 'cython',
                'pandas', 'statsmodels', 'scikit-learn', 'scikits-image' ]

    # Users can override the defaults in an (optional) make_conf.py file
    if os.path.exists('make_conf.py'):
        # Preload the namespace of make_conf with our variables so the user can
        # append/extend them if desired
        overrides = dict(prefix=prefix, projects=projects)
        execfile('make_conf.py', overrides)
        prefix = overrides['prefix']
        projects = overrides['projects']
        
    # Actual code execution starts here.
    actiond = dict( (f.__name__, f) for f in
                    [clone, pull, install, clean, install_clean, update] )

    # Compute location of site-packages and actual arguments for installation
    if prefix is None:
        install_location = '--user'
        prefix = '~/.local'
    else:
        install_location = '--prefix=' + prefix
        
    pythonXY = 'python%d.%d' % sys.version_info[:2]
    sp = '%s/lib/%s/site-packages' % (prefix, pythonXY)
    site_packages = os.path.expanduser(os.path.expandvars(sp))
    
    # Find other git-managed projects in the current directory so the user
    # doesn't have to manually update the projects list all every time he may
    # want to clone an extra project
    update_projects()

    # This could be done more nicely with argparse, but that's a 2.7
    # dependency, so let's do it manually for now.
    if len(sys.argv)<2:
        usage()

    # Targets must be given
    targets = sys.argv[1].split(',')

    # Actions, default is to update all targets
    actions = sys.argv[2:]
    if not actions:
        actions = ['update']

    if targets == ['all']:
        # Unless cloning, 'all' should be interpreted as 'all available', so
        # that it doesn't complain about missing targets that are in the
        # default list.
        if 'clone' in actions:
            targets = projects
        else:
            targets = [p for p in projects if os.path.isdir(p)]
        
    # Ensure all actions and targets are valid, and execute
    validate(actions, actiond, 'action')

    # If users call 'clone', that action should be performed first without
    # target validation, so people can clone any github project without having
    # to edit the config at all.
    if 'clone' in actions:
        clone(targets)
        actions.remove('clone')
        update_projects()

    # After clone, all other actions should only be performed on valid targets
    validate(targets, projects, 'target')
    for action in actions:
        actiond[action](targets)
