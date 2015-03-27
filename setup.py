#!/usr/bin/env
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
from glob import glob
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext


def get_depends(dirname):
    result = glob('%s/*.h' % dirname)
    result += glob('%s/*.pxd' % dirname)
    print result
    return result


setup(
    name='PyCheMPS2',
    version='1.4',
    description='A spin-adapted implementation of DMRG for ab initio quantum chemistry',
    author='Sebastian Wouters',
    author_email='sebastianwouters@gmail.com',
    download_url='https://github.com/SebWouters/CheMPS2',
    license='GNU General Public License, version 2',
    py_modules=['ReadinHamiltonianPsi4'],
    cmdclass = {'build_ext': build_ext},
    ext_modules=[
        Extension("PyCheMPS2",
            sources=['PyCheMPS2/PyCheMPS2.pyx'],
            depends=get_depends('PyCheMPS2'),
            library_dirs=[],
            libraries=['chemps2'],
            include_dirs=[np.get_include(), './PyCheMPS2'],
            language="c++"),
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2',
        'Programming Language :: Cython',
        'Programming Language :: C++',
        'Topic :: Science/Engineering :: Molecular Science'
    ],
)
