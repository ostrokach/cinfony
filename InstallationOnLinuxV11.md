# Installing Cinfony on Linux #

The following instructions take you through the process of installing Cinfony and all of its dependencies. Note that all dependencies are optional so if you don't want to use a particular toolkit, there is no need to follow the instructions for installing it.

## A brief word about installing Python packages ##

After extracting the .tar.gz file, Python packages are generally installed in one of two ways:
  * globally, with `python setup.py install` (requires root)
  * locally, with `python setup.py install --prefix=$HOME`
    * This requires the PYTHONPATH variable to be set to include the directory where the files were installed (in this case, $HOME/lib/python2.6/site-packages or so).

## Prerequisites ##

  * A recent **Python**, **Jython** or **IronPython** in the 2.x series
  * **Java** - If using Jython, or accessing a Java library (e.g. CDK, or OPSIN)
    * Install JDK 6.0 (1.6.0)
  * **Mono** - If using IronPython

## Cinfony ##

  * Download and install [Cinfony 1.1](http://cinfony.googlecode.com/files/cinfony-1.1.tar.gz)
    * Test at the Python prompt as follows:
```
>>> import cinfony
```
  * If you want to draw 2D diagrams for some of the modules, you need to install the Python Imaging Library (PIL)
    * Use your distribution's package manager to install PIL. On Debian Etch, for example, the package was split into python-imaging and python-imaging-tk
    * Test at the Python prompt as follows:
```
>>> import Image
>>> import ImageTk
```
  * In order for Jython to find Cinfony, add a line to the `registry` file in the Jython installation directory as follows:
    * `python.path = /usr/local/lib/python2.6/site-packages` where you should replace the path by the path to the directory where Cinfony was installed
  * In order for IronPython to find Cinfony, add the installation directory to the IRONPYTHONPATH environment variable
  * Test at the Jython or IronPython prompt as follows:
```
>>> import cinfony
```


**Cinfony** contains the following 9 modules (prerequisites listed in parentheses):

  1. **pybel** - Open Babel wrapper (Python)
  1. **jybel** - Open Babel wrapper (Java+Jython)
  1. **ironable** - Open Babel wrapper (Mono+IronPython)
  1. **cdkjpype** - CDK wrapper (Java+Python)
  1. **cdkjython** - CDK wrapper (Java+Jython)
  1. **rdk** - RDKit wrapper (Python)
  1. **opsin** - OPSIN wrapper (Java+Python or Java+Jython)
  1. **indy** - Indigo wrapper (Python or Jython+Java)
  1. **webel** - Access web services (no dependencies)

To install the dependencies for each wrapper, follow the appropriate instructions below. _Note: there is no need to install the dependencies for a wrapper you are not going to use._

## Open Babel ##

Open Babel is a C++ library and can be accessed from all of CPython, Jython and IronPython.

  * Download and extract **[Open Babel](http://openbabel.org/wiki/Install)** 2.3.1
  * Follow the [instructions](http://openbabel.org/docs/current/Installation/install.html#compiling-open-babel) to compile and install Open Babel
    * If you want to be able to create a 2D diagram of a molecule, you need to make sure that you have compiled Open Babel with support for Png output. This requires the Cairo library (and development headers) which you should install using your package manager, prior to compiling Open Babel.
  * Follow the [instructions](http://openbabel.org/docs/current/Installation/install.html#compile-language-bindings) to compile and install the Open Babel **Python** bindings, **Java** bindings or **CSharp** bindings

In the following section $OB\_INSTALLDIR refers to the directory where the Open Babel library was installed (typically `/usr/local/lib`).

### pybel ###

  * Add the directory where the Python bindings were installed to the PYTHONPATH environment variable (if necessary)

### jybel ###

  * Add the directory containing `libopenbabel_java.so` (typically `$OB_INSTALLDIR`) to the LD\_LIBRARY\_PATH environment variable
  * Add the directory containing `openbabel.jar` (typically `$OB_INSTALLDIR`) to the CLASSPATH environment variable

### ironable ###

  * Add the directory containing `libopenbabel_csharp.so` (typically `$OB_INSTALLDIR`) to the LD\_LIBRARY\_PATH environment variable
  * Add the directory containing `OBDotNet.dll` (typically `$OB_INSTALLDIR`) to the OBDOTNET environment variable

### Test ###

  * Test at the Python, Jython or IronPython prompt as follows:
```
>>> from cinfony import obabel
>>> mol = obabel.readstring("smi", "CCC")
>>> print mol.molwt
44.09562
>>> mol.draw()
```


## RDKit ##

The RDKit is a C++ library currently accessible only from CPython.

  * Download and extract **[RDKit](http://code.google.com/p/rdkit/downloads/detail?name=RDKit_2011_09_1.tgz&can=2&q=)** 2011.09
  * Follow the [installation instructions](http://code.google.com/p/rdkit/wiki/BuildingWithCmake)
  * Add the `RDKit_2011_09_1` directory to the PYTHONPATH environment variable
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

  * Download **[CDK](http://sourceforge.net/projects/cdk/files/cdk/cdk-1.4.5.jar/download)** 1.4.5
  * Add the `cdk-1.4.5.jar` file to your CLASSPATH environment variable (remember to include the full path to the jar file)

No additional configuration is required to use the CDK from Jython, but to use it from CPython:

  * Use your package manager to install **JPype**, or else [download](http://jpype.sf.net) and install it
    * You need to set JAVA\_HOME to the Java installation directory before running `setup.py`.
  * Set JPYPE\_JVM environment variable to point to the `libjvm.so` file in your Java installation directory
    * On my system, it's `/home/user/Tools/jdk1.6.0_16/jre/lib/i386/client/libjvm.so`

### Test ###

  * Test at the Python or Jython prompt as follows:
```
>>> from cinfony import cdk
>>> mol = cdk.readstring("smi", "CCC")
>>> print mol.molwt
44.0956192017
>>> mol.draw()
```

## Indigo ##

Indigo is a C++/C library and can be accessed from CPython and Jython (GGASoftware does not provide the .NET bindings for Linux).

  * [Download](http://ggasoftware.com/download/indigo) the Python and/or Java API for Linux and unzip them
  * To access Indigo from CPython, add the extracted Python directory to PYTHONPATH
  * To access Indigo from Jython, add all of the jar files in the extracted Java directory to CLASSPATH
  * Test at the Python or Jython prompt as follows:
```
>>> from cinfony import indy
>>> mol = indy.readstring("smi", "CCC")
>>> print mol.molwt
44.0956192017
>>> mol.draw()
```


## OPSIN ##

OPSIN can be accessed from both CPython (using JPype) and from Jython.
**Please follow the same instructions as for the CDK (above), but using the [OPSIN 1.1 jar file](https://bitbucket.org/dan2097/opsin/downloads/opsin-1.1.0-jar-with-dependencies.jar).** Test at the Python or Jython prompt as follows:
```
>>> from cinfony import opsin
>>> mol = opsin.readstring("iupac", "2-chloro-propane")
>>> print mol.write("smi")
ClC(C)C
```

## Webel ##

Webel is a Cinfony module that uses web services. It is pure-Python and does not require any additional configuration. It will work equally well from all versions of Python.

## Common problems ##

1. If when using one of the Java bindings, you get a complaint about not being able to find `libawt.so`, add to the LD\_LIBRARY\_PATH environment variable the directory in your Java installation containing `libawt.so`.
  * On my system, it's `/home/user/Tools/jdk1.6.0_16/jre/lib/i386`