#summary This page describes how to install cinfony on Linux

# Installing cinfony on Linux #

The following instructions take you through the process of installing cinfony and all of its dependencies.

## A brief word about installing Python packages ##

After extracting the .tar.gz file, Python packages are generally installed in one of two ways:
  * globally, with `python setup.py install` (requires root)
  * locally, with `python setup.py install --prefix=$HOME`
    * This requires the PYTHONPATH variable to be set to include the directory where the files were installed (in this case, $HOME/lib/python2.4/site-packages or so).

## Prerequisites ##

  * **Python** - 2.4 or 2.5
  * **Java** - Install JDK 5.0 (1.5.0\_16)
  * **[Jython](http://www.jython.org)** 2.2

## cinfony ##

  * Download and install [cinfony 0.8](http://cinfony.googlecode.com/files/cinfony-0.8.tar.gz)
    * Test at the Python prompt as follows:
```
>>> import cinfony
```
  * If you want to draw 2D diagrams for any of **pybel**, **rdkit** and **cdkjpype**, you need to install the Python Imaging Library (PIL)
    * Use your distribution's package manager to install PIL. On Debian Etch, for example, the package is split into python-imaging and python-imaging-tk
    * Test at the Python prompt as follows:
```
>>> import Image
>>> import ImageTk
```
  * In order for Jython to find Cinfony, add a line to the `registry` file in the Jython installation directory as follows:
    * `python.path = /usr/local/lib/python2.4/site-packages` where you should replace the path by the path to the directory where Cinfony was installed
      * Test at the Jython prompt as follows:
```
>>> import cinfony
```

Cinfony contains five wrappers:
  1. **pybel** - OpenBabel wrapper (CPython)
  1. **jybel** - OpenBabel wrapper (Jython)
  1. **cdkjpype** - CDK wrapper (CPython)
  1. **cdkjython** - CDK wrapper (Jython)
  1. **rdkit** - RDKit wrapper (CPython)

To install the dependencies for each wrapper, follow the appropriate instructions below. _Note: there is no need to install the dependencies for a wrapper you are not going to use._

## OpenBabel ##

OpenBabel is a C++ library and can be accessed from both CPython and Jython.

  * Download and extract **[OpenBabel](http://openbabel.org/wiki/Install)** 2.2.0
  * Follow the [instructions](http://openbabel.org/wiki/Install_%28source_code%29) to compile and install OpenBabel

### pybel ###

  * Follow the [instructions](http://openbabel.org/wiki/Install_%28source_code%29) to compile and install the OpenBabel Python bindings
  * Test at the Python prompt as follows:
```
>>> from cinfony import obabel
>>> print pybel.readstring("smi", "CCC").molwt
44.09562
```
  * If you want to be able to create a 2D diagram of a molecule, you need to install OASA
    * OASA has a dependency on the Cairo library and its Python bindings, so use your package manager to install these (in Debian, install the python-cairo package)
    * Download and install the Python package **[OASA](http://bkchem.zirael.org/oasa_en.html)** 0.12.1
    * Test at the Python prompt as follows:
```
>>> from cinfony import obabel
>>> pybel.readstring("smi", "CCC").draw()
```

### jybel ###

In the following section $OB\_SRCDIR refers to the directory where OpenBabel was extracted and compiled (something like /home/user/Tools/openbabel-2.2.0), and $OB\_INSTALLDIR refers to the directory where it was installed (typically /usr/local/lib).

  * Download and extract the new [OpenBabel Java bindings](http://cinfony.googlecode.com/files/OBJava-1.0.tar.gz) into the `$OB_SRCDIR/scripts` directory
    * This creates a directory `$OB_SRCDIR/scripts/newjava`
  * Follow the instructions in `newjava/README` to compile the OpenBabel Java bindings
  * Add `$OB_SRCDIR/scripts/newjava` and `$OB_INSTALLDIR` to the LD\_LIBRARY\_PATH environment variable
  * Add `$OB_SRCDIR/scripts/newjava/openbabel.jar` to the CLASSPATH environment variable
  * Test at the Jython prompt as follows:
```
>>> from cinfony import obabel
```

## RDKit ##

The RDKit is a C++ library currently accessible only from CPython.

  * Download and extract **[RDKit](http://rdkit.googlecode.com/files/RDKit_May2008_1.tgz)** May2008\_1
  * Follow the [installation instructions](http://code.google.com/p/rdkit/wiki/BuildingOnLinux)
  * Add the `RDKit_May2008_1\Python` directory to the PYTHONPATH environment variable
  * Test at the Python prompt as follows:
```
>>> from cinfony import rdkit
>>> mol = rdkit.readstring("smi", "CCC")
>>> print mol.molwt
44.097
>>> mol.draw()
```

## CDK ##

The CDK is a Java library and can be accessed from both CPython and Jython.

  * Download **[CDK](http://sourceforge.net/project/showfiles.php?group_id=20024&package_id=35118&release_id=581120)** 1.0.3
  * Add the `cdk.1.0.3.jar` file to your CLASSPATH environment variable (remember to include the full path to the jar file)

### cdkjpype ###

  * Download and install **[JPype](http://jpype.sf.net)**
    * You need to set JAVA\_HOME to the Java installation directory before running `setup.py`.
  * Set JPYPE\_JVM environment variable to point to the `libjvm.so` file in your Java installation directory
    * On my system, it's `/home/user/Tools/jdk1.5.0_16/jre/lib/i386/client/libjvm.so`
  * Add to the LD\_LIBRARY\_PATH environment variable, the directory in your Java installation containing libawt.so
    * On my system, it's `/home/user/Tools/jdk1.5.0_16/jre/lib/i386`
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