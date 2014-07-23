VanHElsing
==========

Automatic Theorem Prover using Machine Learning of Strategies in Python based on the E prover and Satallax.

Dependencies
============

This project has been tested with:
* Ubuntu 13.10, 14.04, Red Hat Linux 6.3
* Python 2.7.4

VanHElsing can be used without root access to the host machine. The only
requirement is the availability of Python, basic compilation tools like GCC,
gfortran and Pip. (the alternative package manager for python)

TPTP
====

Some components of `VanHElsing` require the [TPTP library](http://www.cs.miami.edu/~tptp/).
Odds are you are using this library already. You can download the library
if this is not the case:

```
$ wget http://www.cs.miami.edu/~tptp/TPTP/Distribution/TPTP-v6.1.0.tgz
$ tar -zxf TPTP-v6.1.0.tgz
```

And then add the local TPTP variable (preferably to your .bashrc):

```
$ export TPTP=`pwd`/TPTP-v6.1.0
```

Installation (complete)
=======================

On any Debian-like OS using aptitude, use: (with root)

```
# apt-get install python python-dev python-pip build-essential libblas-dev liblapack-dev gfortran
```

Then, clone this git repository and run:

```
$ git submodule sync
$ git submodule update --init
$ ./install_deps
```

For this approach you need to add the pip binary path to your local PATH
variable (preferably to your .bashrc):

```
$ export PATH=$PATH:~/.local/bin
```

Installation (minimal)
======================

Alternatively, if you have Ubuntu 14.04, you can directly install the minimally required dependencies:

```
# apt-get install python python-pip build-essential python-numpy python-scipy python-sklearn
```

Then, clone this git repository and run:

```
$ git submodule sync
$ git submodule update --init
$ ./build_contrib
```

Tests
=====

Tests can be run using:

```
$ cd tests
$ ./test_all
```
