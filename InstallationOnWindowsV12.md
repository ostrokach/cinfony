# Installing Cinfony on Windows #

**Cinfony** contains the following modules (dependencies listed in parentheses):

  1. **pybel** - OpenBabel wrapper (Python or Java+Jython or IronPython)
  1. **cdk** - CDK wrapper (Java and Python+JPype or Jython)
  1. **rdk** - RDKit wrapper (Python)
  1. **opsin** - OPSIN wrapper (Java and Python+JPype or Jython)
  1. **indy** - Indigo wrapper (Python or Java+Jython or IronPython)
  1. **jchem** - JChem wrapper (Java and Python+JPype or Jython)
  1. **webel** - Uses web services

## Installing dependencies ##

You should install the dependencies first. Depending on what wrappers you wish to use, you should install (32-bit versions of) some or all of the following: [Python 2.7.x](http://www.python.org/download/releases/), [Java 1.7 ("JRE 7")](http://java.sun.com/javase/downloads/index.jsp), [Jython 2.5](http://jython.org/downloads.html), [IronPython 2.7](http://ironpython.net/). If you are installing Jython, you should install Java first.

## Installing Cinfony ##

I will assume that you want to install **Cinfony** into the folder `C:\cinfony`. If you install it somewhere else, remember this when you are following the instructions.

  * Download [cinfony 1.2](http://cinfony.googlecode.com/files/cinfony-1.2.zip), and unzip it, for example, as `C:\cinfony`. This includes the following libraries so you don't need to download them separately:
    * JPype 0.5.4.2 - connects CPython to a JVM
    * NumPy 1.6.2 - fast linear algebra for Python
    * Pycairo 1.4.12 - Python interface to Cairo (drawing library)
    * Python Imaging Library 1.1.7 - Image manipulation in Python
  * If interested in using **Open Babel**, download [OpenBabel 2.3.2](http://sourceforge.net/projects/openbabel/files/openbabel/2.3.2/OpenBabel2.3.2a_Windows_Installer.exe/download) and run the installer. Also download and run the installer for the [Python 2.7 bindings](http://sourceforge.net/projects/openbabel/files/openbabel-python/1.8/openbabel-python-1.8.py27.exe/download).
  * If interested in using the **Chemistry Development Kit**, download [CDK 1.4.15](http://downloads.sourceforge.net/cdk/cdk-1.4.15.jar) and place in `C:\cinfony\Java`
  * If interested in using the **RDKit**, download [RDKit 2012.09](http://rdkit.googlecode.com/files/RDKit_2012_09_1.win32.py27.zip) (Greg Landrum) and unzip into `C:\cinfony\RDKit`
    * If unzipped correctly, there should be a file `C:\cinfony\RDKit\README`
  * If interested in using **OPSIN**, download [OPSIN 1.3](https://bitbucket.org/dan2097/opsin/downloads/opsin-1.3.0-jar-with-dependencies.jar) and place in `C:\cinfony\Java`
  * If interested in using **Indigo**, go to the [Indigo 1.1 download page](http://ggasoftware.com/download/indigo) and...
    * ...for CPython, follow the link for Windows builds: Python API to download a zip file. Unzip this and copy all of the contents into `C:\cinfony\Python`.
    * ...for Jython, follow the link for Windows builds: Java API to download a zip file. Unzip this and place the four jar files within into `C:\cinfony\Java`.
    * ...for IronPython, follow the link for Windows builds: .NET API to download a zip file. Unzip this and copy the three DLLs within into `C:\cinfony\DLL`.
  * If interested in using **JChem**, obtain a license from [ChemAxon](http://www.chemaxon.com/) and then [download](http://www.chemaxon.com/download/jchem/) and install JChem 5.11.
  * Open the file `C:\cinfony\cinfony.bat` with Notepad and follow the instructions therein to configure Cinfony
  * Add the `cinfony` directory to the Windows PATH or just copy `C:\cinfony\cinfony.bat` to a folder that's already on the Windows PATH
    * To add a folder to the Windows PATH, you need to go to Control Panel, System, Advanced System Settings, Environment Variables
    * In the top panel (user variables) search for one called PATH
      * If it's there, click Edit and add `;C:\cinfony` to the end
      * If it's not there, click New, and enter `PATH` for the name and `C:\cinfony` for the value
  * If you are using Jython, open the folder where you installed Jython, and edit the file named `registry` as follows:
    * Before the line `# This is how Jim sets his path etc`, add
```
python.path=C:\\cinfony
```

## Testing Cinfony ##

Open a command prompt anywhere on your computer and type the following
```
C:\Documents and Settings\Noel> cinfony
Cinfony is configured for user! At the Python 2.7 prompt type:
   from cinfony import obabel, rdk, cdk, indy, jchem, opsin, webel
or at the Jython 2.5 prompt type:
   from cinfony import obabel, cdk, indy, opsin, webel
or at the IronPython 2.7 prompt type:
   from cinfony import obabel, indy, jchem, webel

C:\Documents and Settings\Noel> python
Python 2.7.1 (r271:86832, Nov 27 2010, 18:30:46) [MSC v.1500 32 bit (Intel)] on
win32
Type "help", "copyright", "credits" or "license" for more information.
>>> from cinfony import obabel, rdk, cdk, indy, opsin, webel
>>> mol = obabel.readstring("smi", "CC=O")
>>> mol.draw()
>>> print rdk.Molecule(mol).calcdesc()
{'BertzCT': 10.264662506490405, 'fr_C_O_noCOO': 1, 'Chi4v': 0.0, 'fr_Ar_COO': 0,
 'Chi4n': 0.0, 'SMR_VSA4': 0.0, 'fr_urea': 0, 'fr_para_hydroxylation': 0, 'fr_ba
...
one': 0, 'fr_nitro_arom_nonortho': 0, 'Chi0v': 1.9855985596534889, 'fr_ArN': 0,
'NumRotatableBonds': 0}
>>> cdkmol = cdk.Molecule(mol)
>>> cdkmol.addh()
>>> print cdkmol.molwt
44.0525588989
>> print webel.Molecule(mol).write("names")
['acetaldehyde', 'ethanal', '75-07-0', 'NCI-C56326', 'PS2030_SUPELCO', 'NSC7594'
, 'NCGC00091753-01', 'Octowy aldehyd', 'METALDEHYDE', 
...
'acetaldehydes', 'W200360_ALDRICH', 'C00084', 'ACETALD', 'ACETYL GROUP']
>>> (CTRL+Z, Enter)


C:\Documents and Settings\Noel> jython
*sys-package-mgr*: processing new jar, 'C:\cinfony\CDK\cdk-1.2.8.jar'
Jython 2.5.0 on java1.5.0_15
Type "copyright", "credits" or "license" for more information.
>>> from cinfony import obabel, cdk, indy, opsin, webel
>>> mol = cdk.readstring("smi", "CC=O")
>>> print obabel.Molecule(mol).molwt
44.05256
>>> (CTRL+Z, Enter)
```

## Using Cinfony from IDLE ##

  * If you want to run Cinfony scripts from within IDLE, find the file `idle.bat` (on my computer this is in `C:\Python27\Lib\idlelib\idle.bat`) and make a copy called `cinfony_idle.bat`. Edit this file in Notepad and add the following just before the `start idle.pyw` line:
```
call cinfony.bat
```
  * Make a shortcut to `cinfony_idle.bat` on your desktop and use this to start IDLE. You can also drag-and-drop Python scripts onto this shortcut.