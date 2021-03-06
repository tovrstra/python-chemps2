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

cimport Ham
cimport ConvScheme
cimport DMRGSCFopt

cdef extern from "chemps2/CASSCF.h" namespace "CheMPS2":
    cdef cppclass CASSCF:
        CASSCF(Ham.Hamiltonian *, int *, int *) except +
        void setupStart(int *, int *, int *)
        double doCASSCFnewtonraphson(const int, const int, const int, ConvScheme.ConvergenceScheme *, const int, DMRGSCFopt.DMRGSCFoptions *)
        void deleteStoredUnitary()
        void deleteStoredDIIS()
