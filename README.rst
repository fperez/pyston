============================================
 Python Source Package Update/Build utility
============================================

Quickstart
==========

If you want to get started with this repository in a single shot and want to
clone and build all the default projects (assuming you have the necessary build
dependencies and compilers already on your system), type this::

    git clone git://github.com/fperez/pysources.git
    cd pysources
    ./make.py all clone install


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
Otherwise, the value is used with the ``--prefix`` argument.

The list of projects to install is set in the ``projects`` variable, which
should be a list of strings corresponding to project names on github.  This
list is automatically updated with any other paths that contain a ``.git``
subdirectory *and* a ``setup.py`` file.  You can therefore manually clone any
other github python projects you want and they will be automatically picked up
as well, without having to update the ``projects`` list by hand each time
(updating the default ``projects`` is only needed for the ``clone`` action).

These two variables, ``prefix`` and ``projects``, are set to their defaults in
this file, but can be modified by the user by defining them in a file named
``make_conf.py`` located in this same directory.  A template for that file
should have been provided along with this script, but absent that, it's just a
python script that declares two variables named ``prefix`` and ``projects`` as
indicated.

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
