VanHElsing
==========

Automatic Theorem Prover using Machine Learning of Strategies in Python based on the E prover and Satallax.

Usage
=====

```
VanHElsing$ python src/helsing.py -h
usage: helsing.py [-h] [-t TIME] [-p PROBLEM] [-c CONFIGURATION]

Van HElsing 1.0 --- June 2014.

optional arguments:
  -h, --help            show this help message and exit
  -t TIME, --time TIME  Maximum runtime of Van HElsing.
  -p PROBLEM, --problem PROBLEM
                        The location of the problem.
  -c CONFIGURATION, --configuration CONFIGURATION
                        Which configuration file to use.
```

`VanHElsing` is [CASC](http://www.cs.miami.edu/~tptp/CASC/) compliant, and can be prepared using:

```
$ mkdir tmp
$ python src/data.py -c configs/CASC-J7-e.ini
$ python src/learn.py -c configs/CASC-J7-e.ini
```

And then run using for example:

```
$ python src/helsing.py -c configs/CASC-J7-e.ini -t 300 -p data/PUZ001+1.p
```

`Satallax-MaLeS 1.3` is started by using a different config file:

```
$ mkdir tmp
$ python src/data.py -c configs/CASC-J7-satallax.ini
$ python src/learn.py -c configs/CASC-J7-satallax.ini
```

And then run using for example:

```
$ python src/helsing.py -c configs/CASC-J7-satallax.ini -t 300 -p data/PUZ081^1.p
```

For both VanHElsing and Satallax-MaLeS, the initialisation via data.py and learn.py need to by run only once.
Note that the config files use relative paths. You'll need to change them if you want to use VanHElsing/Satallax-MaLeS from anywhere. 

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
# apt-get install python python-dev python-pip build-essential libblas-dev liblapack-dev gfortran zlib1g-dev
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
# apt-get install python python-pip build-essential python-numpy python-scipy python-sklearn zlib1g-dev
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
