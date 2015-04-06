# Installing cinfony on Windows #

**Cinfony** contains the following five wrappers (dependencies listed in parentheses):

  1. **pybel** - OpenBabel wrapper (Python)
  1. **jybel** - OpenBabel wrapper (Java, Jython)
  1. **cdkjpype** - CDK wrapper (Python, Java)
  1. **cdkjython** - CDK wrapper (Java, Jython)
  1. **rdkit** - RDKit wrapper (Python)

## Installing dependencies ##

You should install the dependencies first. Depending on what wrappers you wish to use, you should install [Python 2.5](http://www.python.org/download/), [Java 1.5 ("JRE 5.0")](http://java.sun.com/javase/downloads/index_jdk5.jsp) and/or [Jython 2.2](http://www.jython.org/Project/download.html). If you are installing Jython, you should install Java first.

## Installing cinfony ##

Here I describe how to download and install the main part of **cinfony**. I will assume that you want to install **cinfony** into the folder `C:\cinfony`. If you install it somewhere else, remember this when you are following the instructions.

  * Download [cinfony 0.8](http://cinfony.googlecode.com/files/cinfony-0.8.zip), and unzip it, for example, as `C:\cinfony`. This includes the following libraries so you don't need to download them separately:
    * OpenBabel 2.2.0 - Many contributors including Geoff Hutchison, Tim Vandermeesch and Chris Morley
    * OASA 0.12.1 - Beda Kosata
    * JPype 0.5.3 (Steve Menard) - connects CPython to a JVM
    * Numeric 24.2 (many) - fast linear algebra for Python
    * Pycairo 1.4.12 - Python interface to Cairo (drawing library)
    * AggDraw 1.2a3 (Fredrik Lundh) - Python interface to Agg (drawing library)
    * Python Imaging Library 1.1.6 (Fredrik Lundh) - Image manipulation in Python
  * Download [CDK 1.0.3](http://downloads.sourceforge.net/cdk/cdk-1.0.3.jar) (many contributors) and place in `C:\cinfony\Java`
  * Download [RDKit May2008](http://downloads.sourceforge.net/rdkit/RDKit_May2008_1.win32.py25.tgz) (Greg Landrum) and unzip into `C:\cinfony\RDKit`
    * If unzipped correctly, there should be a file `C:\cinfony\RDKit\README`
  * Open the file `C:\cinfony\cinfony.bat` with Notepad and follow the instructions therein to configure cinfony
  * Add the cinfony directory to the Windows PATH or just copy `C:\cinfony\cinfony.bat` to a folder that's already on the Windows PATH
    * To add a folder to the Windows PATH, you need to go to Control Panel, System, Advanced, Environment Variables
    * In the top panel (user variables) search for one called PATH
      * If it's there, click Edit and add `;C:\cinfony` to the end
      * If it's not there, click New, and enter `PATH` for the name and `C:\cinfony` for the value
  * If you are using Jython, open the folder where you installed Jython, and edit the file named `registry` as follows:
    * Before the line `# This is how Jim sets his path etc`, add
```
python.path=C:\\cinfony
```

## Testing cinfony ##

Open a command prompt anywhere on your computer and type the following
```
C:\Documents and Settings\Noel> cinfony
cinfony is configured for user! At the Python 2.5 prompt type:
   from cinfony import pybel, rdkit, cdk
or at the Jython 2.2 prompt type:
   from cinfony import jybel, cdk

C:\Documents and Settings\Noel> python

Python 2.5 (r25:51908, Sep 19 2006, 09:52:17) [MSC v.1310 32 bit (Intel)] on win
32
Type "help", "copyright", "credits" or "license" for more information.
>>> from cinfony import rdkit, cdk, pybel
>>> mol = pybel.readstring("smi", "CC=O")
>>> mol.draw()
>>> print rdkit.Molecule(mol).calcdesc()
{'BertzCT': 10.264662506490405, 'fr_C_O_noCOO': 1, 'Chi4v': 0.0, 'fr_Ar_COO': 0,
 'Chi4n': 0.0, 'SMR_VSA4': 0.0, 'fr_urea': 0, 'fr_para_hydroxylation': 0, 'fr_ba
...
one': 0, 'fr_nitro_arom_nonortho': 0, 'Chi0v': 1.9855985596534889, 'fr_ArN': 0,
'NumRotatableBonds': 0}
>>> cdkmol = cdk.Molecule(mol)
>>> cdkmol.addh()
>>> print cdkmol.molwt
44.0525588989
>>> (CTRL+Z, Enter)


C:\Documents and Settings\Noel> jython
*sys-package-mgr*: processing new jar, 'C:\cinfony\CDK\cdk-1.0.3.jar'
Jython 2.2.1 on java1.5.0_15
Type "copyright", "credits" or "license" for more information.
>>> from cinfony import cdk, jybel
>>> mol = cdk.readstring("smi", "CC=O")
>>> mol.draw()
>>> print jybel.Molecule(mol).molwt
44.05256
>>> (CTRL+Z, Enter)
```

## Using cinfony from IDLE ##

  * If you want to run cinfony scripts from within IDLE, you need to add the following line to `idle.bat` (on my computer this is in `C:\Python25\Lib\idlelib\idle.bat`) just before the `start idle.pyw` line:
```
call cinfony.bat
```
  * Make a shortcut to `idle.bat` on your desktop and use this to start IDLE. You can also drag-and-drop Python scripts onto this shortcut.