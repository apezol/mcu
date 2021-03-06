#!/usr/bin/env python
'''
mcu: Modeling and Crystallographic Utilities
Copyright (C) 2019 Hung Q. Pham. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Email: Hung Q. Pham <pqh3.14@gmail.com>
'''

'''
Utilities for vasp module
'''

import numpy as np
from ..utils.misc import check_exist
from ..cell import parameters, utils            

    
def read_unk(path='.', spin=0, kpt=1, band=1):
    '''Export the periodic part of BF in a real space grid for plotting with wannier90
    '''	
    spin = spin + 1
    file = path + '/' + 'UNK' + "%05d" % (kpt) + '.' + str(spin)
    assert check_exist(file), 'Cannot find the %s file. Check the path:' + file
        
    from scipy.io import FortranFile
    unk_file = FortranFile(file, 'r')
    temp = unk_file.read_record(dtype=np.int32)
    ngrid, kpt, nbands = temp[:3], temp[3], temp[4]
    assert band <= nbands, 'The band index is larger than the No. of bands in the unk file'

    for i in range(band):
        temp = unk_file.read_record(dtype=np.complex128)
        if i == band - 1:
            unk = temp
        del temp 

    unk_file.close()
    
    return unk.reshape(ngrid, order='F')
    
def read_U_matrix(filename):
    '''Read seedname_u.mat file
    '''	
    
    with open(filename, "r") as file:
        data = file.read().split('\n')
        nkpts, nwann, nband =  np.int64(data[1].split())
        temp = data[2:-1]
        block_length = nband*nwann + 2
        kpts = []
        U_kpts = []
        for kpt_th in range(nkpts):
            Uk = temp[(kpt_th*block_length):(kpt_th*block_length + block_length)]
            kpts.append(np.float64(Uk[1].split()))
            U = np.asarray([np.float64(line.split()[0]) + 1j*np.float64(line.split()[1]) for line in Uk[2:]])
            U_kpts.append(U.reshape(nwann, nband).T) 

        kpts = np.float64(kpts)
        U_kpts = np.asarray(U_kpts)

    return kpts, U_kpts