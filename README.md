VanHElsing
==========

Automatic Theorem Prover in Python based on the E prover

Dependencies
============

This project has been tested with:
* Ubuntu 13.10
* Python 2.7.4

VanHElsing can be used without root access to the host machine. The only
requirement is the availability of Python and Pip, the alternative package
manager for python.

On any Debian-like OS using aptitude, use: (with root)

```
# apt-get install python python-pip
```

Then, clone this git repository and run:

```
$ git submodule sync
$ git submodule update --init
$ ./install_deps
```

Tests
=====

Tests can be run using:

```
$ cd src/tests
$ ./test_all
```
