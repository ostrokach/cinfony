"""
opsinjpype - A Cinfony module for accessing OPSIN from CPython

Global variables:
  opsin - the underlying CDK Java library (org.openscience.cdk)
  informats - a dictionary of supported input formats
  outformats - a dictionary of supported output formats
"""

import os

from jpype import *

if not isJVMStarted():
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
    >>> input = "propane"
    >>> mymol = readstring("iupac", input)
    """
    if format!="iupac":
        raise ValueError("%s is not a recognised OPSIN format" % format)

    result = _nametostruct.parseChemicalName(string, False)
    if str(result.getStatus()) == "FAILURE":
        raise IOError("Failed to convert '%s' to format '%s'\n%s" % (
            string, format, result.getMessage()))

    return Molecule(result)

    
class Molecule(object):
    """Represent a opsinjpype Molecule.

    Required parameters:
       OpsinResult -- the result of using OPSIN to parse an IUPAC string

    Methods:
       write()
      
    The underlying OpsinResult can be accessed using the attribute:
       OpsinResult
    """
    
    def __init__(self, OpsinResult):
            
        self.OpsinResult = OpsinResult
        
    def __str__(self):
        return self.write()

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
        """        
        if format not in outformats:
            raise ValueError,"%s is not a recognised OPSIN format" % format
        
        if filename is not None and not overwrite and os.path.isfile(filename):
            raise IOError, "%s already exists. Use 'overwrite=True' to overwrite it." % filename

        if format == "cml":
            result = self.OpsinResult.getCml().toXML()
        elif format == "inchi":
            result = _restoinchi(self.OpsinResult, False)
        else:
            raise ValueError, "%s is not a recognised OPSIN format" % format
        if filename:
            outputfile = open(filename, "w")
            print >> outputfile, result
            outputfile.close()
        else:
            return result

if __name__=="__main__": #pragma: no cover
    mol = readstring("iupac", "propane")
    print mol.write("inchi")
