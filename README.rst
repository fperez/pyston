============================================
 Python Source Package Update/Build utility
============================================

Clone/update from github and locally install Python packages.

This is a simple script meant to easily manage a collection of github-hosted
python packages from source, so that it's quick to clone, build, install and
update them with a simple command.

Usage
=====

  ./make.py  TARGET1,TARGET2  ACTION1  ACTION2 ...

TARGET is 'all' or a *comma-separated* list of targets.

ACTION defaults to 'update', which pulls from git, fully cleans all
build/installation products, and installs.


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
