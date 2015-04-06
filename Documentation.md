#summary How to use cinfony

# Cinfony - the toolkit of cheminformatics toolkits #

## Introduction ##

Cinfony presents a common interface to the four main open source cheminformatics toolkits (Open Babel, the CDK, Indigo and the RDKit) as well as to the commercial toolkit JChem, and to cheminformatics webservices and OPSIN. Its goal is to make it easy to carry most of the common tasks in cheminformatics such as file input/output, calculating descriptors and fingerprints, and SMARTS searching.

For more fine-grained control, or to use additional features, the underlying toolkit can be accessed. The Molecule classes used by Cinfony can be interconverted between different toolkits, as well as converted to and from the molecule class used by the underlying toolkit.

## How to use Cinfony from Python ##

(For installation instructions, please see the pages for [Windows](InstallationOnWindowsV12.md) or [Linux](InstallationOnLinuxV12.md))

Cinfony has seven modules corresponding to the supported toolkits: **_pybel_**, **_cdk_**, **_rdk_**, **_indy_**, **_jchem_**, **_opsin_**, **_webel_**.

Cinfony supports both regular Python, Jython (the Java implementation of Python) and IronPython (the .NET implementation). All of the Cinfony modules can be used from regular Python, but currently _rdk_ cannot be used from Jython, and only _pybel_, _indy_ and _webel_ can be used from IronPython.

To import a particular Cinfony module such as _pybel_, use:
```
>>> from cinfony import pybel
```
If you are using more than one cinfony module, you could do:
```
>>> from cinfony import pybel, rdk, cdk
```
Information on the Cinfony API can be found at the interactive Python prompt using the `help()` function:
```
>>> from cinfony import rdk
>>> help(rdk) # All of the documentation on the rdk module
...
>>> help(rdk.Molecule) # Just the documentation on the Molecule
...
>>> help(rdk.Molecule.draw) # Documentation on a single method
...
```
The same information API information is available as [web pages](http://www.redbrick.dcu.ie/~noel/cinfony/current/).

## Molecules ##

### Creating a Cinfony Molecule ###

A Cinfony Molecule can be created in any of four ways:

  * By reading from a file (see [Reading molecular file formats](#Reading.md) below)
  * By reading from a string (see [Reading molecular file formats](#Reading.md) below)
  * From the molecule object of the underlying toolkit, using **`Molecule(myMol)`**

> This feature allows you to wrap the molecule objects used by the underlying toolkit. You can then use all of the Cinfony methods. For example, if you have an OpenBabel OBMol, you can create a _pybel_ Molecule using `pybel.Molecule(myOBMol)`. Similarly, RDKit's Mol object can be wrapped with `rdk.Molecule(myMol)`, and CDK's Molecule object can be wrapped with `cdk.Molecule(myCDKMolecule)`.

  * From another Cinfony Molecule, using **`Molecule(myMolecule)`**

> This feature allows you to pass molecular information between different toolkits. If you have a _pybel_ Molecule called 'myobmol', you can create the corresponding rdk Molecule with `rdk.Molecule(myobmol)`. The conversion is done (behind the scenes) using the MOL file format for molecules with coordinates, or SMILES strings for molecules without coordinates.

### Attributes of a Cinfony Molecule ###

All Cinfony Molecules have the following attributes:
  * **`atoms`** - a list of the Atoms in a Molecule
  * **`data`** - a dictionary-like object for accessing and editing the data fields associated with the Molecule
  * **`formula`** (not _rdk_) - the molecular formula
  * **`molwt`** - the molecular weight
  * **`title`** - the title field of the Molecule
  * **`Mol`** or **`Molecule`** or **`OBMol`** - the underlying toolkit molecule on which this Cinfony Molecule is based. The name of the attribute depends on the particular Cinfony module. It's either OBMol (for _pybel_), Mol (for _rdk_) or Molecule (for _cdk_ and _jchem_... note that _jchem_ also has a MolHandler attribute). In this way, it is easy to combine the convenience of Cinfony with the many additional capabilities present in the underlying toolkits.

_pybel_ Molecules have the following additional attributes:
  * **`charge`** - formal charge
  * **`conformers`** - the entire set of conformers for this molecule
  * **`dim`** - number of dimensions (3 for a 3D structure)
  * **`energy`** - heat of formation
  * **`exactmass`** - the mass given by isotopes (or the most abundant isotope if not specified)
  * **`spin`** - total spin on the molecule (1 is singlet)
  * **`sssr`** - the smallest set of smallest rings
  * **`unitcell`** - unit cell data associated with the molecule (see [OBUnitCell](http://openbabel.org/api/current/classOpenBabel_1_1OBUnitCell.shtml))

All of these attributes are read-only, except for the `title` and the contents of the `data` attribute.

#### Example ####
Let's suppose we have an SD file containing descriptor values in the data fields:
```
>>> mol = pybel.readfile("sdf", "calculatedprops.sdf").next() # (readfile is described below)
>>> print mol.molwt
100.1
>>> print len(mol.atoms)
16
>>> print mol.data.keys()
{'Comment': 'Created by CDK', 'NSC': 1, 'Hydrogen Bond Donors': 3, 'Surface Area': 342.43, .... }
>>> print mol.data['Hydrogen Bond Donors']
3
>>> mol.data['Random Value'] = random.randint(0,1000) # Add a descriptor containing noise
```
Remember that the data object behaves like a regular dictionary, so that you can use its `update()` method to update it with the contents of another dictionary. This is useful if you have a dictionary of descriptor names and values (like that returned by `calcdesc()` below) and want to store these values in an SD file.

### Methods of a Cinfony Molecule ###

Cinfony Molecules have the following methods:
  * **`addh()`** and **`removeh()`** - add or remove hydrogens
  * **`calcfp()`** - calculate a molecular fingerprint (see [Fingerprints](#Fingerprints.md) below)
  * **`calcdesc()`** - calculate descriptor values. A list of available descriptors is contained in the `descs` variable. The default is to calculate all available descriptors, but instead a list of descriptor names can be supplied. The result is a dictionary of descriptor names and values.
  * **`draw()`** (not _jybel_) - generate 2D coordinates and a 2D depiction of a molecule. The default options are to show the image on the screen (`show=True`), not to write to a file (`filename=None`), to calculate 2D coordinates (`usecoords=False`) but not to store them (`update=False`).
  * **`localopt()`** (not _cdk_) - minimise the energy using a forcefield. The default options for _pybel_ are `forcefield="MMFF94"` and `steps=500`. For _rdk_, forcefield="UFF". The list of available forcefields is stored in the **`forcefields`** variable. **Note:** for _pybel_, hydrogens need to be added before calling `localopt()`.
  * **`make3D()`** (not _cdk_) - generate 3D coordinates. By default, this includes 50 steps of a geometry optimisation using the MMFF94 forcefield for _pybel_, and the UFF forcefield for _rdk_. You may want to call `localopt()` afterwards to improve the structure further. **Note:** for _pybel_, hydrogens need to be added before calling `make3D()`.
  * **`write()`** - write a representation of a Molecule to a file or to a string (see [Writing molecular file formats](#Writing.md) below)

#### Example ####
Since the .data attribute of a Molecule is also a dictionary, you can easily add the result of calcdesc() to an SD file (for example) as follows:
```
mol = readfile("sdf", "without_desc.sdf").next()
descvalues = mol.calcdesc()
# In Python, the update method of a dictionary allows you
# to add the contents of one dictionary to another
mol.data.update(descvalues)
output = Outputfile("sdf", "with_desc.sdf")
output.write(mol)
output.close()
```

## Atoms ##

### Creating a Cinfony Atom ###

An Atom can be created in three different ways:

  * By accessing the **`atoms`** attribute of a Molecule
  * From the atom object of the underlying toolkit, using **`Atom(myAtom)`**.  This feature allows you to wrap the molecule objects used by the underlying toolkit. You can then use all of the Cinfony methods. For example, if you have an OpenBabel OBAtom, you can create a _pybel_ Atom using `pybel.Atom(myOBAtom)`. Similarly, RDKit's Atom object can be wrapped with `rdk.Atom(myRDKitAtom)`, and CDK's Atom object can be wrapped with `cdk.Atom(myCDKAtom)`.
  * Using a Molecule's iterator. This is used as follows:
```
for atom in myMolecule:
   # do something with atom
```

### Atom Attributes ###

All Cinfony Atoms have the following attributes:
  * **`atomicnum`** - the atomic number
  * **`coords`** - a tuple (x, y, z) of the Atom's coordinates.
  * **`formalcharge`**
  * **`Atom`** or **`OBAtom`** - the underlying toolkit molecule on which this Cinfony Atom is based. The name of the attribute depends on the particular Cinfony module. It's either OBAtom (for _pybel_), or Atom (for _cdk_ and _rdk_).

_pybel_ Atoms have the following additional attributes:
  * **`atomicmass`** - the atomic mass
  * **`exactmass`** - the mass of the isotope (or the most abundant isotope if not specified)
  * **`heavyvalence`** - the number of non-hydrogen atoms connected to this atom
  * **`heterovalence`** - the number of heteroatoms connected to an atom
  * **`hyb`** - the hybridization of this atom (i.e. 1 for sp, 2 for sp2, 3 for sp3)
  * **`idx`** - the index of the atom in the molecule
  * **`implicitvalence`** - the implicit valence of this atom type (i.e. maximum number of connections expected)
  * **`isotope`** - the isotope for this atom, if specified, or 0 for unspecified
  * **`partialcharge`** - the partial charge of this atom, calculating a Gasteiger charge if needed
  * **`spin`** - the atomic spin; 0 for normal atoms, 2 for radical, 1 or 3 for carbene
  * **`type`** - the atom type
  * **`valence`** - the current number of explicit connections

## Reading and writing molecular file formats ##

One of the most common tasks any cheminformatician needs to do is to read and write molecular file formats. Cinfony greatly simplifies the process of reading and writing molecules to and from strings or files.

### Reading ###

Each Cinfony module supports a different set of input formats. These are stored in the dictionary **`informats`**, where the keys are the codes for each format (e.g. 'pdb') and the values are the descriptions (e.g. 'Protein Data Bank format').

There are two functions for reading Molecules:

  * **`readstring(format, string)`** reads a Molecule from a string
  * **`readfile(format, filename)`** provides an iterator over the Molecules in a file

#### Example ####
Here are some examples of their use. Note in particular the use of `next()` (a method of Python iterators) to access the first (and possibly only) molecule in a file:
```
>>> mymol = rdk.readstring("smi", "CCCC")
>>> print mymol.molwt
58
>>> for mymol in rdk.readfile("sdf", "largeSDfile.sdf"): # Read one molecule at a time
...	   print mymol.molwt
>>> allmols = list(rdk.readfile("sdf", "largeSDfile.sdf")) # Read the whole file into memory
>>> singlemol = pybel.readfile("pdb", "1CRN.pdb").next() # Read a single molecule
```

### Writing ###

The set of output formats supported by a particular Cinfony module is stored in the dictionary **`outformats`**, where the keys are the three-letter codes for each format (e.g. 'pdb') and the values are the descriptions (e.g. 'Protein Data Bank format').

If a single molecule is to be written to an outputfile or to a string, the `write()` method of the Molecule should be used:

  * **`mymol.write(format)`** returns a string
  * **`mymol.write(format, filename)`** writes the Molecule to a file. An optional additional parameter, `overwrite`, should be set to True if you wish to overwrite an existing file.

For files containing multiple molecules, the **`Outputfile`** class should be used instead. This is initialised with a format and filename (and optional `overwrite` parameter). To write a Molecule to the file, the **`write()`** method of the Outputfile is called with the Molecule as a parameter. When all molecules have been written, the **`close()`** method of the Outputfile should be called.

#### Example ####
```
>>> print mymol.write("smi")
'CCCC'
>>> mymol.write("smi", "outputfile.txt")
>>> largeSDfile = rdk.Outputfile("sdf", "multipleSD.sdf")
>>> largeSDfile.write(mymol)
>>> largeSDfile.write(myothermol)
>>> largeSDfile.close()
```

## Fingerprints ##

A Fingerprint can be created in either of two ways:

  * By calling the **`calcfp()`** method of a Molecule. This calculates the default path-based fingerprint for that toolkit, "FP2" for _pybel_, "Daylight" for _rdk_ and _cdk_. A list of available fingerprints is stored in the variable **`fps`**. Note that only binary fingerprints will be wrapped by the Fingerprint object. All other fingerprints will be returned unwrapped.
  * From a vector representing a binary fingerprint in the underlying toolkit

Once created, the Fingerprint has two attributes:
  * **`fp`** gives the original vector corresponding to the fingerprint
  * **`bits`** gives a list of the bits that are set.

The Tanimoto coefficient of two Fingerprints can be calculated using the "|" operator.

Here is an example of its use:
```
>>> smiles = ['CCCC', 'CCCN']
>>> mols = [pybel.readstring("smi", x) for x in smiles] # Create two molecules from the SMILES
>>> fps = [x.calcfp() for x in mols] # Calculate their fingerprints
>>> print fps[0].bits, fps[1].bits
[261, 385, 671] [83, 261, 349, 671, 907]
>>> print fps[0] | fps[1] # Print the Tanimoto coefficient
0.3333
```

## SMARTS matching ##

Cinfony provides a simplified API to the SMARTS pattern matchers of OpenBabel, RDKit and CDK. A Smarts object is created from a smarts string using **`Smarts(my_smarts_string)`**, and the **`findall()`** method is then used to return a list of the matches to a given Molecule. Only unique matches are returned, and it should be noted that the atom indices returned by `findall()` are the same as in the underlying toolkit (for example, OpenBabel numbers atoms from 1).

The SMARTS pattern matcher provided by _webel_ uses the CDK webservices. However, instead of a `findall()` method it just has a `match()` method that returns True or False.

Here is an example of the use of the Smarts object:
```
>>> mol = pybel.readstring("smi","CCN(CC)CC") # triethylamine
>>> smarts = pybel.Smarts("[#6][#6]") # Matches an ethyl group
>>> print smarts.findall(mol) 
[(1, 2), (4, 5), (6, 7)]
```

## Accessing the underlying toolkit ##

It is easy to combine the ease of use of Cinfony with the more comprehensive features of the underlying toolkits. There are two ways to do this:
  * By accessing the underlying atom or molecule wrapped by the Cinfony Atom or Molecule (see [Atom Attributes](#Atom_Attributes.md) and [Molecule Attributes](#Attributes_of_a_Cinfony_Molecule.md) above).
  * By accessing the underlying library

> The underlying library can be accessed through global variables of each Cinfony module (or indeed, can be imported independently of Cinfony):
    * **`ob`** in _pybel_ - the SWIG bindings to the OpenBabel library. See http://openbabel.org/wiki/Python for more information. Also see the OpenBabel API at http://openbabel.org/api/current.
    * **`cdk`** in _cdk_ - this is the equivalent of org.openscience.cdk in the CDK Java API. The CDK 1.2.3 API is not available on the web, but the 1.2.3 documentation is available at http://sourceforge.net/projects/cdk/files/cdk/1.2.3/cdk-javadoc-1.2.3.tar.gz/download.
    * **`Chem`** and **`AllChem`** in _rdk_ - these are the RDKit Python bindings. See the introduction at http://rdkit.org/RDKit_Overview.pdf, and the full API at http://rdkit.org/Python_Docs/.
    * **`chemaxon`** in _jchem_. The JChem API is available online at http://www.chemaxon.com/jchem/doc/dev/java/api/index.html.

> The situation for _webel_ is slightly different in that there isn't an underlying toolkit, rather there are underlying webservices:
    * **`rajweb`** and **`nci`** in _webel_ - these are Rajarshi Guha's CDK webservices (hosted at Uppsala University) and Markus Sitzmann's Chemical Identifier Resolver webservices (NIH National Cancer Institute). The appropriate documentation can be found at http://rest.rguha.net and http://cactus.nci.nih.gov/chemical/structure/documentation, respectively.

#### Example ####

The following example shows how to read a molecule from a PDB file using _pybel_, and then how to add hydrogens by calling a method on the underlying OBMol (note: this is just an example - all Cinfony Molecules have an `addh()` method that does exactly this).
```
>>> mol = pybel.readfile("pdb", "1PYB").next()
>>> help(mol)
Help on Molecule in module pybel object:
...
 |  Attributes:
 |     atoms, charge, dim, energy, exactmass, flags, formula,
 |     mod, molwt, spin, sssr, title.
...
 |  The original Open Babel molecule can be accessed using the attribute:
 |     OBMol
...
>>> print len(mol.atoms), mol.molwt
3430 49315.2
>>> dir(mol.OBMol) # Show the list of methods provided by the underlying OBMol
['AddAtom', 'AddBond', 'AddConformer', 'AddHydrogens', 'AddPolarHydrogens', ... ]
>>> mol.OBMol.AddHydrogens()
>>> print len(mol.atoms), mol.molwt
7244 49406.0
```