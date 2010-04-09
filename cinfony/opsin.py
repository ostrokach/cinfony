"""
opsin - A Cinfony module for accessing OPSIN

opsin can be used from both CPython and Jython. It imports the appropriate
Cinfony module, either opsinjpype and opsinjython, depending on the Python
implementation.
"""
import sys

if sys.platform[:4] == "java":
    from opsinjython import *
else:
    from opsinjpype import *
