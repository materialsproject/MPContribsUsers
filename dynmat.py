# export MAST_CONTROL=$HOME/MAST/CONTROL
# export MAST_PLATFORM=pbs_generic
# export MAST_SCRATCH=$HOME/MAST/SCRATCH

from StringIO import StringIO
import re, sys, math
import numpy as np
from MAST.ingredients.checker import VaspChecker

# Al3
version = "01" # 02, 03
outcar = {}
outcar["01"] = StringIO("""
   1 f/i=    2.661027 THz    16.719728 2PiTHz   88.762316 cm-1    11.005129 meV
             X         Y         Z           dx          dy          dz
      0.000000  0.000000  0.000000     1.000000           0           0  
      0.000000  2.043133  2.043133            0           0           0  
      2.043133  0.000000  2.043133            0           0           0  
""")
outcar["02"] = StringIO("""
   1 f/i=    2.660281 THz    16.715037 2PiTHz   88.737411 cm-1    11.002041 meV
             X         Y         Z           dx          dy          dz
      0.000000  0.000000  0.000000            0    1.000000           0  
      0.000000  2.043133  2.043133            0           0           0  
      2.043133  0.000000  2.043133            0           0           0  
""")
outcar["03"] = StringIO("""
   1 f  =    5.423207 THz    34.075015 2PiTHz  180.898711 cm-1    22.428590 meV
             X         Y         Z           dx          dy          dz
      0.000000  0.000000  0.000000            0           0    1.000000  
      0.000000  2.043133  2.043133            0           0           0  
      2.043133  0.000000  2.043133            0           0           0  
""")

# phonon_vac1_w4
    2  5    3
  63.546 196.966
   12    1  0.0500  0.0000  0.0000
  0.000000   0.000000   0.000000
  0.000000   0.000000   0.000000
 -0.297585   0.055901   0.000000
  0.000000   0.000000   0.000000
  0.000000   0.000000   0.000000
   12    2  0.0000  0.0500  0.0000
  0.000000   0.000000   0.000000
  0.000000   0.000000   0.000000
  0.055046  -0.298080   0.000000
  0.000000   0.000000   0.000000
  0.000000   0.000000   0.000000
   12    3  0.0000  0.0000  0.0500
  0.000000   0.000000   0.000000
  0.000000   0.000000   0.000000
 -0.000623  -0.000623  -0.347529
  0.000000   0.000000   0.000000
  0.000000   0.000000   0.000000

# from OUTCAR
# https://github.com/raman-sc/VASP/blob/master/vasp_raman.py
outcar[version].readline() # empty line
p = re.search(r'^\s*(\d+).+?([\.\d]+) cm-1', outcar[version].readline())
eigval = float(p.group(2))
print eigval
outcar[version].readline() #  X Y ...
eigvec = []
for j in range(3):
    tmp = outcar[version].readline().split()
    eigvec.append([ float(tmp[x]) for x in range(3,6) ])
norm = math.sqrt( sum( [abs(x)**2 for sublist in eigvec for x in sublist] ) )
print np.array(eigvec), norm

# from DYNMAT
vaspdir = "/Users/patrick/Downloads/MAST-1.2.9.4/MAST/test/checker_test_vasp/dynamics_split/phon_%s" % version
vpc = VaspChecker(name = "dynamics")
dynmat_dict = vpc.read_my_dynamical_matrix_file(vaspdir)
eigvec = []
for r in dynmat_dict['atoms'][1][1]['dynmat']:
        eigvec.append(map(float, r.split()))
eigvec = np.array(eigvec)
norm = math.sqrt( sum( [abs(x)**2 for sublist in eigvec for x in sublist] ) )
print eigvec, norm
#frequencies = np.sqrt(np.abs(-0.03247)) * np.sign(-0.03247)
#print frequencies
#conversion_factor_to_THz = 15.633302
#print frequencies * conversion_factor_to_THz
