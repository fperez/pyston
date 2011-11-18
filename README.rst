===========================================================
 pyston: a simple tool for managing python source packages
===========================================================

Quickstart
==========

If you want to get started with this repository in a single shot and want to
clone and build all the default projects (a list of popular scientific
computing Python projects hosted) , copy and paste this (assuming you have the
necessary build dependencies and compilers already on your system)::

    git clone git://github.com/fperez/pyston.git
    cd pyston
    ./pyston clone install all

For regular use, the most convenient is to symlink the ``pyston`` script from
somewhere in your ``$PATH``.  You can then use ``pyston`` as a command from
anywhere in your system to quickly clone, update and install github-hosted
python packages.  See how to customize the install location or default package
list below.


Purpose
=======

``pyston`` is a simple tool meant to easily manage a collection of
github-hosted python packages from source, so that it's quick to clone, build,
install and update them with few commands.


Usage
=====

The general command line usage is (assuming ``pyston`` is in your path,
otherwise use the full path to the script)::

  pyston  [ACTION1  ACTION2 ... TARGET1 TARGET2 ...]

At least one action or target must be provided.  Actions and targets are
identified because the list of valid actions is short and fixed (see below).
All words not recognized as actions are treated as targets.  It's OK for
targets to have a trailing slash (which happens if you tab-complete names),
they will be removed.

If no action is given, the default action is 'update' (see below).

The targets can be either the string 'all' or the names of git repositories
available in the working directory.  If the 'clone' action is provided, you can
also include the names of projects on github.com.  As long as they are named
with the convention ``github.com/name/name``), they will be cloned first.

If no target is given, 'all' is assumed. The 'all' target expands to the
default builtin list of packages (a collection of scientific computing python
tools) for cloning, and to all the git repositories in the working directory
for all other actions.

The simplest way to use it is to simply clone the included default list of
packages with::

    pyston clone install all

.. note::

   This will clone roughly 10 packages from github, several of which have
   complex build dependencies (such as scipy or matplotlib), so don't clone the
   full default list unless you really want them all and have all the build
   dependencies.

Afterwards, this::

    pyston update

will run an update of all packages (i.e. pull from git and reinstall).
Individual packages can be updated::

    pyston update numpy scipy

You can also clone and install any project that's hosted on github with a URL
of the pattern ``github.com/PROJECT/PROJECT`` with::

    pyston clone install PROJECT

even if it is not listed on the default project list.  And since all locally
available packages (directories with ``.git`` and ``setup.py``) are
automatically loaded, you can use this tool to continue updating them without
need for further customization.


Available actions
=================

clone
  Clone a repository hosted on github with the name pattern
  github.com/target/target.

pull
  Change to the target directory and run ``git pull``.

install
  Run ``python setup.py install`` with the appropriate installation prefix
  variable (see below in customization section).

install_clean
  Clean the installation directory for the target.

clean
  Clean the build directory for the target.

update
  Run pull, then install.

full_update
  Run pull, clean, install_clean and install.


Customization
=============

The install location directive is controlled by the ``prefix`` variable.  If
set to None, then ``--user`` is passed to the setup.py installation routine.
Otherwise, the value is used with the ``--prefix`` argument.  If you define the
environment variable ``PREFIX``, it will override the internal default.

The list of projects to install is set in the ``projects`` variable, which
should be a list of strings corresponding to project names on github.  This
list is automatically updated with any other paths that contain a ``.git``
subdirectory *and* a ``setup.py`` file.  You can therefore manually clone any
other github python projects you want and they will be automatically picked up
as well, without having to update the ``projects`` list by hand each time
(updating the default ``projects`` is only needed for the ``clone`` action).

These two variables, ``prefix`` and ``projects``, are set to their defaults in
this file, but can be modified by the user by defining them in a file named
``pyston_conf.py`` located in this same directory (a file overrides also the
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
