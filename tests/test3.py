#
#   CheMPS2: a spin-adapted implementation of DMRG for ab initio quantum chemistry
#   Copyright (C) 2013-2015 Sebastian Wouters
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License along
#   with this program; if not, write to the Free Software Foundation, Inc.,
#   51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

import numpy as np
import math as m
import sys
import PyCheMPS2
import ReadinHamiltonianPsi4
import ctypes

# Set the seed of the random number generator and cout.precision
Initializer = PyCheMPS2.PyInitialize()
Initializer.Init()

# Read in the Hamiltonian from the Psi4 plugin
Ham = ReadinHamiltonianPsi4.Read('matrixelements/CH4_N10_S0_c2v_I0.dat')

# Define the symmetry sector
TwoS  = 0    # Two times the targeted spin
Nelec = 10   # The number of electrons
Irrep = 0    # The targeted irrep

# Setting up the Problem
Prob = PyCheMPS2.PyProblem(Ham, TwoS, Nelec, Irrep)

# Setting up the ConvergenceScheme
# setInstruction(instruction, D, Econst, maxSweeps, noisePrefactor)
OptScheme = PyCheMPS2.PyConvergenceScheme(2) # 2 instructions
OptScheme.setInstruction(0,   30, 1e-10,  3, 0.1)
OptScheme.setInstruction(1, 1000, 1e-10, 10, 0.0)

# Do DMRG calculation
theDMRG = PyCheMPS2.PyDMRG(Prob, OptScheme)
EnergyDMRG = theDMRG.Solve()
theDMRG.calc2DMandCorrelations()

# Do FCI calculation
Nel_up   = ( Nelec + TwoS ) / 2
Nel_down = ( Nelec - TwoS ) / 2
maxMemWorkMB = 10.0
FCIverbose = 1
theFCI = PyCheMPS2.PyFCI(Ham, Nel_up, Nel_down, Irrep, maxMemWorkMB, FCIverbose)
GSvector = np.zeros([ theFCI.getVecLength() ], dtype=ctypes.c_double)
GSvector[ theFCI.LowestEnergyDeterminant() ] = 1.0
EnergyFCI = theFCI.GSDavidson(GSvector)
theFCI.CalcSpinSquared(GSvector)
TwoRDM = np.zeros([ Ham.getL()**4 ], dtype=ctypes.c_double)
theFCI.Fill2RDM(GSvector, TwoRDM)
RMSerror2DM = 0.0
for orb1 in range(0, Ham.getL()):
    for orb2 in range(0, Ham.getL()):
        for orb3 in range(0, Ham.getL()):
            for orb4 in range(0, Ham.getL()):
                temp = TwoRDM[orb1 + Ham.getL()*(orb2 + Ham.getL()*(orb3 + Ham.getL()*orb4))] - theDMRG.get2DMA(orb1,orb2,orb3,orb4)
                RMSerror2DM += temp*temp
RMSerror2DM = m.sqrt(RMSerror2DM)
print "Frobenius norm of the difference of the DMRG and FCI 2-RDMs =", RMSerror2DM

# Clean-up
# theDMRG.deleteStoredMPS()
theDMRG.deleteStoredOperators()
del theFCI
del theDMRG
del OptScheme
del Prob
del Ham
del Initializer

# Check whether the test succeeded
if ((np.fabs(EnergyDMRG - EnergyFCI) < 1e-10) and (RMSerror2DM < 1e-6)):
    print "================> Did test 3 succeed : yes"
else:
    print "================> Did test 3 succeed : no"
