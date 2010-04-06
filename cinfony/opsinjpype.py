"""
cdkjpype - A Cinfony module for accessing the CDK from CPython

Global variables:
  cdk - the underlying CDK Java library (org.openscience.cdk)
  informats - a dictionary of supported input formats
  outformats - a dictionary of supported output formats
  descs - a list of supported descriptors
  fps - a list of supported fingerprint types
  forcefields - a list of supported forcefields
"""

import os
import bz2
import math
import urllib
import base64
import tempfile
import StringIO

from jpype import *

_jvm = os.environ['JPYPE_JVM']
_cp = os.environ['CLASSPATH']
startJVM(_jvm, "-Djava.class.path=" + _cp)

opsin = JPackage("uk").ac.cam.ch.wwmm.opsin
try:
    _nametostruct = opsin.NameToStructure.getInstance()
    _restoinchi = opsin.NameToInchi.convertResultToInChI
except TypeError:
    raise ImportError("The OPSIN Jar file cannot be found.")

informats = {'iupac': 'IUPAC name'}
"""A dictionary of supported input formats"""
outformats = {'cml': "Chemical Markup Language", 'inchi': "InChI"}
"""A dictionary of supported output formats"""

def readstring(format, string):
    """Read in a molecule from a string.

    Required parameters:
       format - see the informats variable for a list of available
                input formats
       string

    Example:
    >>> input = "C1=CC=CS1"
    >>> mymol = readstring("smi", input)
    >>> len(mymol.atoms)
    5
    """
    if format=="iupac":
        return Molecule(_nametostruct.parseChemicalName(string, False))
    else:
        raise ValueError,"%s is not a recognised OPSIN format" % format

class Outputfile(object):
    """Represent a file to which *output* is to be sent.
   
    Required parameters:
       format - see the outformats variable for a list of available
                output formats
       filename

    Optional parameters:
       overwite -- if the output file already exists, should it
                   be overwritten? (default is False)
                   
    Methods:
       write(molecule)
       close()
    """
    def __init__(self, format, filename, overwrite=False):
        self.format = format
        self.filename = filename
        if not overwrite and os.path.isfile(self.filename):
            raise IOError, "%s already exists. Use 'overwrite=True' to overwrite it." % self.filename
        if not format in outformats:
            raise ValueError,"%s is not a recognised CDK format" % format
        if self.format == "smi":
            self._sg = cdk.smiles.SmilesGenerator()
            self._sg.setUseAromaticityFlag(True)
            self._outputfile = open(self.filename, "w")
        else:
            self._writer = java.io.FileWriter(java.io.File(self.filename))
            self._molwriter = _outformats[self.format](self._writer)
        self.total = 0 # The total number of molecules written to the file
    
    def write(self, molecule):
        """Write a molecule to the output file.
        
        Required parameters:
           molecule
        """
        if not self.filename:
            raise IOError, "Outputfile instance is closed."
        if self.format == "smi":
            self._outputfile.write("%s\n" % self._sg.createSMILES(molecule.Molecule))
        else:
            self._molwriter.write(molecule.Molecule)
        self.total += 1

    def close(self):
        """Close the Outputfile to further writing."""
        self.filename = None
        if self.format == "smi":
            self._outputfile.close()
        else:
            self._molwriter.close()
            self._writer.close()

    
class Molecule(object):
    """Represent a cdkjpype Molecule.

    Required parameters:
       Molecule -- a CDK Molecule or any type of cinfony Molecule

    Attributes:
       atoms, data, exactmass, formula, molwt, title
    
    Methods:
       addh(), calcfp(), calcdesc(), draw(), removeh(), write()
      
    The underlying CDK Molecule can be accessed using the attribute:
       Molecule
    """
    _cinfony = True

    def __init__(self, Molecule):
        
        if hasattr(Molecule, "_cinfony"):
            a, b = Molecule._exchange
            if a == 0:
                mol = readstring("smi", b)
            else:
                mol = readstring("sdf", b)    
            Molecule = mol.Molecule
            
        self.OpsinResult = Molecule
        
    @property
    def atoms(self): return [Atom(self.Molecule.getAtom(i)) for i in range(self.Molecule.getAtomCount())]
    @property
    def data(self): return MoleculeData(self.Molecule)
    @property
    def formula(self):
        manip = cdk.tools.manipulator.MolecularFormulaManipulator
        mf = manip.getMolecularFormula(self.Molecule)
        return manip.getString(mf) # GetHillString
    @property
    def exactmass(self):
        clone = Molecule(self.Molecule.clone())
        clone.addh()
        manip = cdk.tools.manipulator.MolecularFormulaManipulator
        mf = manip.getMolecularFormula(clone.Molecule)
        return manip.getMajorIsotopeMass(mf)
    @property
    def molwt(self):
        clone = Molecule(self.Molecule.clone())
        clone.addh()
        atommanip = cdk.tools.manipulator.AtomContainerManipulator
        return atommanip.getNaturalExactMass(clone.Molecule)
    def _gettitle(self): return self.Molecule.getProperty(cdk.CDKConstants.TITLE)
    def _settitle(self, val): self.Molecule.setProperty(cdk.CDKConstants.TITLE, val)
    title = property(_gettitle, _settitle)
    @property
    def _exchange(self):
        gt = cdk.geometry.GeometryTools
        if gt.has2DCoordinates(self.Molecule) or gt.has3DCoordinates(self.Molecule):
            return (1, self.write("mol"))
        else:
            return (0, self.write("smi"))

    def __iter__(self):
        """Iterate over the Atoms of the Molecule.
        
        This allows constructions such as the following:
           for atom in mymol:
               print atom
        """
        return iter(self.atoms)

    def __str__(self):
        return self.write()

    def addh(self):
        """Add hydrogens."""
        atommanip = cdk.tools.manipulator.AtomContainerManipulator
        atommanip.convertImplicitToExplicitHydrogens(self.Molecule)

    def removeh(self):
        """Remove hydrogens."""        
        atommanip = cdk.tools.manipulator.AtomContainerManipulator
        self.Molecule = atommanip.removeHydrogens(self.Molecule)

    def write(self, format="smi", filename=None, overwrite=False):
        """Write the molecule to a file or return a string.
        
        Optional parameters:
           format -- see the informats variable for a list of available
                     output formats (default is "smi")
           filename -- default is None
           overwite -- if the output file already exists, should it
                       be overwritten? (default is False)

        If a filename is specified, the result is written to a file.
        Otherwise, a string is returned containing the result.

        To write multiple molecules to the same file you should use
        the Outputfile class.
        """        
        if format not in outformats:
            raise ValueError,"%s is not a recognised OPSIN format" % format
        
        if filename is not None and not overwrite and os.path.isfile(filename):
            raise IOError, "%s already exists. Use 'overwrite=True' to overwrite it." % filename

        if format == "cml":
            return self.OpsinResult.getCml().toXML()
        elif format == "inchi":
            return _restoinchi(self.OpsinResult, False)
        else:
            raise ValueError, "%s is not a recognised OPSIN format" % format

    def calcfp(self, fp="daylight"):
        """Calculate a molecular fingerprint.
        
        Optional parameters:
           fptype -- the fingerprint type (default is "daylight"). See the
                     fps variable for a list of of available fingerprint
                     types.
        """        
        # if fp == "substructure":
        #    fingerprinter = cdk.fingerprint.SubstructureFingerprinter(
        #        cdk.fingerprint.StandardSubstructureSets.getFunctionalGroupSubstructureSet()
        #        )
        fp = fp.lower()
        if fp == "graph":
            fingerprinter = cdk.fingerprint.GraphOnlyFingerprinter()
        elif fp == "daylight":
            fingerprinter = cdk.fingerprint.Fingerprinter()
        else:
            raise ValueError, "%s is not a recognised CDK Fingerprint type" % fp
        return Fingerprint(fingerprinter.getFingerprint(self.Molecule))

    def calcdesc(self, descnames=[]):
        """Calculate descriptor values.

        Optional parameter:
           descnames -- a list of names of descriptors

        If descnames is not specified, all available descriptors are
        calculated. See the descs variable for a list of available
        descriptors.
        """
        if not descnames:
            descnames = descs
        ans = {}
        for descname in descnames:
            try:
                desc = _descdict[descname]
            except KeyError:
                raise ValueError, "%s is not a recognised CDK descriptor type" % descname
            try:
                value = desc.calculate(self.Molecule).getValue()
                if hasattr(value, "get"): # Instead of array
                    for i in range(value.length()):
                        ans[descname + ".%d" % i] = value.get(i)
                elif hasattr(value, "doubleValue"):
                    ans[descname] = value.doubleValue()
                else:
                    ans[descname] = value.intValue()
            except JavaException, ex:
                # Can happen if molecule has no 3D coordinates
                pass
        return ans    

    def draw(self, show=True, filename=None, update=False,
             usecoords=False):
        """Create a 2D depiction of the molecule.

        Optional parameters:
          show -- display on screen (default is True)
          filename -- write to file (default is None)
          update -- update the coordinates of the atoms to those
                    determined by the structure diagram generator
                    (default is False)
          usecoords -- don't calculate 2D coordinates, just use
                       the current coordinates (default is False)

        OASA is used for depiction. Tkinter and Python
        Imaging Library are required for image display.
        """
        web = False # Disable the use of ChemBioGrid web services
        writetofile = filename is not None

        if not usecoords:            
            # Do the SDG
            sdg = cdk.layout.StructureDiagramGenerator()
            sdg.setMolecule(self.Molecule)
            sdg.generateExperimentalCoordinates()
            newmol = Molecule(sdg.getMolecule())
            if update:
                for atom, newatom in zip(self.atoms, newmol.atoms):
                    coords = newatom.Atom.getPoint2d()
                    atom.Atom.setPoint3d(javax.vecmath.Point3d(
                                         coords.x, coords.y, 0.0))    
        else:
            newmol = self
            
        if writetofile or show:
            if writetofile:
                filedes = None
            else:
                filedes, filename = tempfile.mkstemp()
            if not web:
                # Create OASA molecule
                if not oasa:
                    errormessage = ("OASA not found, but is required for 2D structure "
                            "depiction. OASA is part of BKChem. "
                            "See installation instructions for more "
                            "information.")
                    raise ImportError, errormessage                
                mol = oasa.molecule()
                atomnos = []
                for newatom in newmol.atoms:
                    if not usecoords:
                        coords = newatom.Atom.getPoint2d()
                    else:
                        coords = newatom.Atom.getPoint3d()
                        if not coords:
                            coords = newatom.Atom.getPoint2d()
                    v = mol.create_vertex()
                    v.charge = newatom.formalcharge
                    v.symbol = _isofact.getElement(newatom.atomicnum).getSymbol()
                    mol.add_vertex(v)
                    v.x, v.y, v.z = coords.x * 30., coords.y * 30., 0.0
                for i in range(self.Molecule.getBondCount()):
                    bond = self.Molecule.getBond(i)
                    bo = _revbondtypes[bond.getOrder()]
                    atoms = [self.Molecule.getAtomNumber(x) for x in bond.atoms().iterator()]
                    e = mol.create_edge()
                    e.order = bo
                    if bond.getStereo() == cdk.CDKConstants.STEREO_BOND_DOWN:
                        e.type = "h"
                    elif bond.getStereo() == cdk.CDKConstants.STEREO_BOND_UP:
                        e.type = "w"
                    mol.add_edge(atoms[0], atoms[1], e)
                mol.remove_unimportant_hydrogens()
                maxx = max([v.x for v in mol.vertices])
                minx = min([v.x for v in mol.vertices])
                maxy = max([v.y for v in mol.vertices])
                miny = min([v.y for v in mol.vertices])
                maxcoord = max(maxx - minx, maxy - miny)
                for v in mol.vertices:
                    if str(v.x) == "-1.#IND":
                        v.x = minx
                    if str(v.y) == "-1.#IND":
                        v.y = miny
                fontsize = 16
                bondwidth = 6
                linewidth = 2
                if maxcoord > 270: # 300  - margin * 2
                    for v in mol.vertices:                       
                        v.x *= 270. / maxcoord
                        v.y *= 270. / maxcoord
                    fontsize *= math.sqrt(270. / maxcoord)
                    bondwidth *= math.sqrt(270. / maxcoord)
                    linewidth *= math.sqrt(270. / maxcoord)
                # print "Debug#", [str(a.x) for a in mol.vertices if not a.x >-100]
                
                canvas = oasa.cairo_out.cairo_out()
                canvas.show_hydrogens_on_hetero = True
                canvas.font_size = fontsize
                canvas.bond_width = bondwidth
                canvas.line_width = linewidth
                canvas.mol_to_cairo(mol, filename)
            else:
                encodesmiles = base64.urlsafe_b64encode(bz2.compress(self.write("smi")))
                imagedata = urllib.urlopen("http://www.chembiogrid.org/cheminfo/rest/depict/" +
                                       encodesmiles).read()
                if writetofile:
                    print >> open(filename, "wb"), imagedata
            if show:
                if not tk:
                    errormessage = ("Tkinter or Python Imaging "
                                    "Library not found, but is required for image "
                                    "display. See installation instructions for "
                                    "more information.")
                    raise ImportError, errormessage                    
                root = tk.Tk()
                root.title((hasattr(self, "title") and self.title)
                           or self.__str__().rstrip())
                frame = tk.Frame(root, colormap="new", visual='truecolor').pack()
                if web:
                    image = PIL.open(StringIO.StringIO(imagedata))
                else:
                    image = PIL.open(filename)
                imagedata = piltk.PhotoImage(image)
                label = tk.Label(frame, image=imagedata).pack()
                quitbutton = tk.Button(root, text="Close", command=root.destroy).pack(fill=tk.X)
                root.mainloop()
            if filedes:
                os.close(filedes)
                os.remove(filename)

##    def localopt(self, forcefield="MMFF94", steps=100):
##        forcefield = forcefield.lower()
##        
##        geoopt = cdk.modeling.forcefield.GeometricMinimizer()
##        geoopt.setMolecule(self.Molecule, False)
##        points = [t.Atom.point3d for t in self.atoms]
##        coords = [(t.x, t.y, t.z) for t in points]
##        print coords
##        if forcefield == "MMFF94":
##            ff = cdk.modeling.forcefield.MMFF94Energy(self.Molecule,
##                                geoopt.getPotentialParameterSet())
##        # geoopt.setMMFF94Tables()
##        geoopt.steepestDescentsMinimization(coords, forcefield)
##
##    def make3D(self, forcefield="MMFF94", steps=50):
##        """Generate 3D coordinates.
##        
##        Optional parameters:
##           forcefield -- default is "MMFF94"
##           steps -- default is 50
##
##        Hydrogens are added, coordinates are generated and a quick
##        local optimization is carried out with 50 steps and the
##        MMFF94 forcefield. Call localopt() if you want
##        to improve the coordinates further.
##        """
##        forcefield = forcefield.lower()
##        if forcefield not in forcefields:
##            print "hey"
##            pass
##        self.addh()
##        th3d = cdk.modeling.builder3d.TemplateHandler3D.getInstance()
##        mb3d = cdk.modeling.builder3d.ModelBuilder3D.getInstance(
##            th3d, forcefield)
##        self.Molecule = mb3d.generate3DCoordinates(self.Molecule, False)
##        self.localopt(forcefield, steps)

class Fingerprint(object):
    """A Molecular Fingerprint.
    
    Required parameters:
       fingerprint -- a vector calculated by one of the fingerprint methods

    Attributes:
       fp -- the underlying fingerprint object
       bits -- a list of bits set in the Fingerprint

    Methods:
       The "|" operator can be used to calculate the Tanimoto coeff. For example,
       given two Fingerprints 'a', and 'b', the Tanimoto coefficient is given by:
          tanimoto = a | b
    """
    def __init__(self, fingerprint):
        self.fp = fingerprint
    def __or__(self, other):
        return cdk.similarity.Tanimoto.calculate(self.fp, other.fp)
    def __getattr__(self, attr):
        if attr == "bits":
            # Create a bits attribute on-the-fly
            bits = []
            idx = self.fp.nextSetBit(0)
            while idx >= 0:
                bits.append(idx)
                idx = self.fp.nextSetBit(idx + 1)
            return bits
        else:
            raise AttributeError, "Fingerprint has no attribute %s" % attr
    def __str__(self):
        return self.fp.toString()

class Atom(object):
    """Represent a cdkjpype Atom.

    Required parameters:
       Atom -- a CDK Atom
     
    Attributes:
       atomicnum, coords, formalcharge

    The original CDK Atom can be accessed using the attribute:
       Atom
    """

    def __init__(self, Atom):
        self.Atom = Atom
        
    @property
    def atomicnum(self):
        _isofact.configure(self.Atom)
        return self.Atom.getAtomicNumber().intValue()
    @property
    def coords(self):
        coords = self.Atom.point3d
        if not coords:
            coords = self.Atom.point2d
            if not coords:
                return (0., 0., 0.)
        else:
            return (coords.x, coords.y, coords.z)
    @property
    def formalcharge(self):
        _isofact.configure(self.Atom)
        return self.Atom.getFormalCharge().intValue()

    def __str__(self):
        c = self.coords
        return "Atom: %d (%.2f %.2f %.2f)" % (self.atomicnum, c[0], c[1], c[2])

class Smarts(object):
    """A Smarts Pattern Matcher

    Required parameters:
       smartspattern
    
    Methods:
       findall()
    
    Example:
    >>> mol = readstring("smi","CCN(CC)CC") # triethylamine
    >>> smarts = Smarts("[#6][#6]") # Matches an ethyl group
    >>> print smarts.findall(mol) 
    [(1, 2), (4, 5), (6, 7)]
    """
    def __init__(self, smartspattern):
        """Initialise with a SMARTS pattern."""
        self.smarts = cdk.smiles.smarts.SMARTSQueryTool(smartspattern)
        
    def findall(self, molecule):
        """Find all matches of the SMARTS pattern to a particular molecule.
        
        Required parameters:
           molecule
        """
        match = self.smarts.matches(molecule.Molecule)
        return list(self.smarts.getUniqueMatchingAtoms())

class MoleculeData(object):
    """Store molecule data in a dictionary-type object
    
    Required parameters:
      Molecule -- a CDK Molecule

    Methods and accessor methods are like those of a dictionary except
    that the data is retrieved on-the-fly from the underlying Molecule.

    Example:
    >>> mol = readfile("sdf", 'head.sdf').next()
    >>> data = mol.data
    >>> print data
    {'Comment': 'CORINA 2.61 0041  25.10.2001', 'NSC': '1'}
    >>> print len(data), data.keys(), data.has_key("NSC")
    2 ['Comment', 'NSC'] True
    >>> print data['Comment']
    CORINA 2.61 0041  25.10.2001
    >>> data['Comment'] = 'This is a new comment'
    >>> for k,v in data.iteritems():
    ...    print k, "-->", v
    Comment --> This is a new comment
    NSC --> 1
    >>> del data['NSC']
    >>> print len(data), data.keys(), data.has_key("NSC")
    1 ['Comment'] False
    """
    def __init__(self, Molecule):
        self._mol = Molecule
    def _data(self):
        return self._mol.getProperties()
    def _testforkey(self, key):
        if not key in self:
            raise KeyError, "'%s'" % key
    def keys(self):
        return list(self._data().keySet())
    def values(self):
        return list(self._data().values())
    def items(self):
        return [(k, self[k]) for k in self._data().keySet()]
    def __iter__(self):
        return iter(self.keys())
    def iteritems(self):
        return iter(self.items())
    def __len__(self):
        return len(self._data())
    def __contains__(self, key):
        return key in self._data()
    def __delitem__(self, key):
        self._testforkey(key)
        self._mol.removeProperty(key)
    def clear(self):
        for key in self:
            del self[key]
    def has_key(self, key):
        return key in self
    def update(self, dictionary):
        for k, v in dictionary.iteritems():
            self[k] = v
    def __getitem__(self, key):
        self._testforkey(key)
        return self._mol.getProperty(key)
    def __setitem__(self, key, value):
        self._mol.setProperty(key, str(value))
    def __repr__(self):
        return dict(self.iteritems()).__repr__()

##>>> readstring("smi", "CCC").calcfp().bits
##[542, 637, 742]
##>>> readstring("smi", "CCC").calcfp("graph").bits
##[595, 742, 927]
##>>> readstring("smi", "CC=C").calcfp().bits
##[500, 588, 637, 742]
##>>> readstring("smi", "CC=C").calcfp("graph").bits
##[595, 742, 927]
##>>> readstring("smi", "C").calcfp().bits
##[742]
##>>> readstring("smi", "CC").calcfp().bits
##[637, 742]

# >>> readstring("smi", "CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
# CCCCCCCCCCCCCC").calcdesc(["lipinskifailures"])
# {'lipinskifailures': 1}

if __name__=="__main__": #pragma: no cover
    mol = readstring("smi", "CCCC")
    print mol

    for mol in readfile("sdf", "head.sdf"):
        pass
    #mol = readstring("smi","CCN(CC)CC") # triethylamine
    #smarts = Smarts("[#6][#6]")
    # print smarts.findall(mol)
    mol = readstring("smi", "CC=O")
    # d = mol.calcdesc()
