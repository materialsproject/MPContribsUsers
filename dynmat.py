# export MAST_CONTROL=$HOME/MAST/CONTROL
# export MAST_PLATFORM=pbs_generic
# export MAST_SCRATCH=$HOME/MAST/SCRATCH

import re, sys, math
import numpy as np
from MAST.ingredients.checker import VaspChecker

# Al3 OUTCAR
outcar = open('OUTCAR', 'w')
outcar.write("""
   1 f/i=    2.661027 THz    16.719728 2PiTHz   88.762316 cm-1    11.005129 meV
             X         Y         Z           dx          dy          dz
      0.000000  0.000000  0.000000     1.000000           0           0  
      0.000000  2.043133  2.043133            0           0           0  
      2.043133  0.000000  2.043133            0           0           0  

   1 f/i=    2.660281 THz    16.715037 2PiTHz   88.737411 cm-1    11.002041 meV
             X         Y         Z           dx          dy          dz
      0.000000  0.000000  0.000000            0    1.000000           0  
      0.000000  2.043133  2.043133            0           0           0  
      2.043133  0.000000  2.043133            0           0           0  

   1 f  =    5.423207 THz    34.075015 2PiTHz  180.898711 cm-1    22.428590 meV
             X         Y         Z           dx          dy          dz
      0.000000  0.000000  0.000000            0           0    1.000000  
      0.000000  2.043133  2.043133            0           0           0  
      2.043133  0.000000  2.043133            0           0           0  
""")
outcar.close()

# Al3 DYNMAT
al3_dynmat = """ 1    3    1
 26.982
    1    1  0.0100  0.0000  0.0000
  0.007818   0.000000   0.000000
  0.000000   0.000000   0.000000
  0.000000   0.000000   0.000000
    1    2  0.0000  0.0100  0.0000
  0.000000   0.007813   0.000000
  0.000000   0.000000   0.000000
  0.000000   0.000000   0.000000
    1    3  0.0000  0.0000  0.0100
  0.000000   0.000000  -0.032470
  0.000000   0.000000   0.000000
  0.000000   0.000000   0.000000"""

# UW/SI2 phonon_vac1_w4 DYNMAT
uwsi2_dynmat = """ 2  6    3
  63.546 196.966
   4    1  0.0500  0.0000  0.0000
  0.000000   0.000000   0.000000
  0.000000   0.000000   0.000000
  0.000000   0.000000   0.000000
 -0.297585   0.055901   0.000000
  0.000000   0.000000   0.000000
  0.000000   0.000000   0.000000
   4    2  0.0000  0.0500  0.0000
  0.000000   0.000000   0.000000
  0.000000   0.000000   0.000000
  0.000000   0.000000   0.000000
  0.055046  -0.298080   0.000000
  0.000000   0.000000   0.000000
  0.000000   0.000000   0.000000
   4    3  0.0000  0.0000  0.0500
  0.000000   0.000000   0.000000
  0.000000   0.000000   0.000000
  0.000000   0.000000   0.000000
 -0.000623  -0.000623  -0.347529
  0.000000   0.000000   0.000000
  0.000000   0.000000   0.000000"""

# from OUTCAR
# https://github.com/raman-sc/VASP/blob/master/vasp_raman.py
nat = 3 # TODO
outcar_fh = open('OUTCAR', 'r')
eigval = []
for i in range(nat):
    outcar_fh.readline() # empty line
    p = re.search(r'^\s*(\d+).+?([\.\d]+) cm-1', outcar_fh.readline())
    eigval.append(float(p.group(2)))
    outcar_fh.readline() #  X Y ...
    eigvec = None
    for j in range(nat):
        tmp = outcar_fh.readline().split()
        if eigvec is not None and sum(eigvec) > 0.: continue
        eigvec = [ float(tmp[x]) for x in range(3,6) ]
    norm = math.sqrt( sum( [abs(x)**2 for x in eigvec] ) )
outcar_fh.close()

# from DYNMAT
def from_dynmat(dynmat_str):
    dynmat = open('DYNMAT', 'w')
    dynmat.write(dynmat_str)
    dynmat.close()
    vpc = VaspChecker(name = "dynamics")
    dynmat_dict = vpc.read_my_dynamical_matrix_file('.')
    for k,v0 in dynmat_dict['atoms'].iteritems():
        for v1 in v0.itervalues():
            eigvec = map(float, v1['dynmat'][k-1].split())
            frequencies = np.sqrt(np.abs(np.array(eigvec))) *1000.
            frequency = math.sqrt( sum( [abs(x)**2 for x in frequencies] ) )
            print eigvec, frequency#, eigval[i]/frequency

from_dynmat(al3_dynmat)
from_dynmat(uwsi2_dynmat)
