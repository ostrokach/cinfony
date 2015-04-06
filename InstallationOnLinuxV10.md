#summary This page describes how to install cinfony 1.0.x on Linux

# Installing cinfony on Linux #

The following instructions take you through the process of installing cinfony and all of its dependencies.

## A brief word about installing Python packages ##

After extracting the .tar.gz file, Python packages are generally installed in one of two ways:
  * globally, with `python setup.py install` (requires root)
  * locally, with `python setup.py install --prefix=$HOME`
    * This requires the PYTHONPATH variable to be set to include the directory where the files were installed (in this case, $HOME/lib/python2.5/site-packages or so).

## Prerequisites ##

  * **Python** - 2.5 or 2.6
  * **Java** - Install JDK 6.0 (1.6.0\_18)
  * **[Jython](http://www.jython.org)** 2.5

## cinfony ##

  * Download and install [cinfony 1.0](http://cinfony.googlecode.com/files/cinfony-1.0.tar.gz)
    * Test at the Python prompt as follows:
```
>>> import cinfony
```
  * If you want to draw 2D diagrams for any of **pybel**, **rdkit** and **cdkjpype**, you need to install the Python Imaging Library (PIL)
    * Use your distribution's package manager to install PIL. On Debian Etch, for example, the package was split into python-imaging and python-imaging-tk
    * Test at the Python prompt as follows:
```
>>> import Image
>>> import ImageTk
```
  * In order for Jython to find Cinfony, add a line to the `registry` file in the Jython installation directory as follows:
    * `python.path = /usr/local/lib/python2.5/site-packages` where you should replace the path by the path to the directory where Cinfony was installed
      * Test at the Jython prompt as follows:
```
>>> import cinfony
```

**Cinfony** contains the following 7 modules (dependencies listed in parentheses):

  1. **pybel** - OpenBabel wrapper (Python)
  1. **jybel** - OpenBabel wrapper (Java, Jython)
  1. **ironable** - OpenBabel wrapper (IronPython - **not yet available for Linux**)
  1. **cdkjpype** - CDK wrapper (Python, Java)
  1. **cdkjython** - CDK wrapper (Java, Jython)
  1. **rdk** - RDKit wrapper (Python)
  1. **webel** - Uses web services

To install the dependencies for each wrapper, follow the appropriate instructions below. _Note: there is no need to install the dependencies for a wrapper you are not going to use._

## OpenBabel ##

OpenBabel is a C++ library and can be accessed from all of CPython, Jython and IronPython.

  * Download and extract **[OpenBabel](http://openbabel.org/wiki/Install)** 2.2.3
  * Follow the [instructions](http://openbabel.org/wiki/Install_%28source_code%29) to compile and install OpenBabel

### pybel ###

  * Follow the [instructions](http://openbabel.org/wiki/Install_Python_bindings#Linux_and_MacOSX) to compile and install the OpenBabel Python bindings
  * Test at the Python prompt as follows:
```
>>> from cinfony import obabel
>>> print obabel.readstring("smi", "CCC").molwt
44.09562
```
  * If you want to be able to create a 2D diagram of a molecule, you need to install OASA
    * OASA has a dependency on the Cairo library and its Python bindings, so use your package manager to install these (in Debian, install the python-cairo package)
    * Download and install the Python package **[OASA](http://bkchem.zirael.org/oasa_en.html)** 0.13.1
    * Test at the Python prompt as follows:
```
>>> from cinfony import obabel
>>> pybel.readstring("smi", "CCC").draw()
```

### jybel ###

In the following section $OB\_SRCDIR refers to the directory where OpenBabel was extracted and compiled (something like /home/user/Tools/openbabel-2.2.3), and $OB\_INSTALLDIR refers to the directory where it was installed (typically /usr/local/lib).

  * Follow the instructions in `$OB_SRCDIR/scripts/java/README` to compile the OpenBabel Java bindings
  * Add `$OB_SRCDIR/scripts/java` and `$OB_INSTALLDIR` to the LD\_LIBRARY\_PATH environment variable
  * Add `$OB_SRCDIR/scripts/java/openbabel.jar` to the CLASSPATH environment variable
  * Test at the Jython prompt as follows:
```
>>> from cinfony import obabel
```

### ironable ###

In theory, OpenBabel can be accessed from IronPython running on Mono in Linux. However, I have updated the Windows release of !OBDotNet since the release of OpenBabel 2.2.3 to overcome problems with the initial release. Support for ironable on Linux will be available with the next release of OpenBabel.

## RDKit ##

The RDKit is a C++ library currently accessible only from CPython.

  * Download and extract **[RDKit](http://rdkit.googlecode.com/files/RDKit_Q42009_1.tar.gz)** Q42009
  * Follow the [installation instructions](http://code.google.com/p/rdkit/wiki/BuildingWithCmake)
  * Add the `RDKit_Q42009_1` directory to the PYTHONPATH environment variable
  * Test at the Python prompt as follows:
```
>>> from cinfony import rdk
>>> mol = rdk.readstring("smi", "CCC")
>>> print mol.molwt
44.097
>>> mol.draw()
```

## CDK ##

The CDK is a Java library and can be accessed from both CPython and Jython.

  * Download **[CDK](http://sourceforge.net/projects/cdk/files/cdk/cdk-1.2.5.jar/download)** 1.2.5
  * Add the `cdk-1.2.5.jar` file to your CLASSPATH environment variable (remember to include the full path to the jar file)

### cdkjpype ###

  * Download and install **[JPype](http://jpype.sf.net)**
    * You need to set JAVA\_HOME to the Java installation directory before running `setup.py`.
  * Set JPYPE\_JVM environment variable to point to the `libjvm.so` file in your Java installation directory
    * On my system, it's `/home/user/Tools/jdk1.6.0_16/jre/lib/i386/client/libjvm.so`
  * Add to the LD\_LIBRARY\_PATH environment variable, the directory in your Java installation containing libawt.so
    * On my system, it's `/home/user/Tools/jdk1.6.0_16/jre/lib/i386`
  * Test at the Python prompt as follows:
```
>>> from cinfony import cdk
>>> mol = cdk.readstring("smi", "CCC")
>>> mol.addh()
>>> print mol.molwt
44.0956192017
```
  * If you want to be able to create a 2D diagram of a molecule, you need to install OASA (see installation instructions in the Pybel section above).
    * Test at the Python prompt as follows:
```
>>> from cinfony import cdk
>>> cdk.readstring("smi", "CCC").draw()
```

### cdkjython ###

  * At this point you should already have configured Jython to find Cinfony and have added the CDK jar to the CLASSPATH
  * Test at the Jython prompt as follows:
```
>>> from cinfony import cdk
>>> cdk.readstring("smi", "CCC").draw()
```

## Webel ##

Webel is a Cinfony module that uses web services. It is pure-Python and does not require any additional configuration. It will work equally well from all versions of Python.