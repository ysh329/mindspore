# Copyright 2021 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================

"""Operators for sponge."""

from ..primitive import PrimitiveWithInfer, prim_attr_register
from ..._checkparam import Rel
from ..._checkparam import Validator as validator
from ...common import dtype as mstype


class BondForce(PrimitiveWithInfer):
    """
    BondForce:

    Calculate the force exerted by the simple harmonic bond on the
    corresponding atoms. Assume the number of harmonic bonds is M and
    the number of atoms is N.

    .. math::

        dr = (x_1-x_2, y_1-y_2, z_1-z_2)
        F = (F_x, F_y, F_z) = 2*k*(1 - r_0/|dr|)*dr

    Inputs:
        - **atom_numbers** (int32) - the number of atoms N.
        - **bond_numbers** (int32) - the number of harmonic bonds M.
        - **uint_crd_f** (Tensor, uint32 ) - [N, 3], the unsigned int coordinate
        value of each atom.
        - **scaler_f** (Tensor, float32) - [3,], the 3-D scale factor (x, y, z),
    between the real space float coordinates and the unsigned int coordinates.
        - **atom_a** (Tensor, int32) - [M,], the first atom index of each bond.
        - **atom_b** (Tensor, int32) - [M,], the second atom index of each bond.
        - **bond_k** (Tensor, float32) - [M,], the force constant of each bond.
        - **bond_r0** (Tensor, float32) - [M,], the equlibrium length of each bond.

    Outputs:
        - **frc_f** (float32 Tensor) - [N, 3], the force felt by each atom.

    Supported Platforms:
        ``GPU``
    Examples:
    """

    @prim_attr_register
    def __init__(self, bond_numbers, atom_numbers):
        self.bond_numbers = bond_numbers
        self.atom_numbers = atom_numbers
        self.add_prim_attr('bond_numbers', self.bond_numbers)
        self.add_prim_attr('atom_numbers', self.atom_numbers)
        self.init_prim_io_names(inputs=['uint_crd_f', 'scaler_f', 'atom_a', 'atom_b', 'bond_k', 'bond_r0'],
                                outputs=['frc_f'])

    def infer_shape(self, uint_crd_f_shape, scaler_f_shape, atom_a_shape, atom_b_shape, bond_k_shape, bond_r0_shape):
        cls_name = self.name
        N = self.atom_numbers
        M = self.bond_numbers
        validator.check_int(uint_crd_f_shape[0], N, Rel.EQ, "uint_crd_f_shape", cls_name)
        validator.check_int(uint_crd_f_shape[1], 3, Rel.EQ, "uint_crd_f_shape", cls_name)
        validator.check_int(scaler_f_shape[0], 3, Rel.EQ, "scaler_f_shape", cls_name)
        validator.check_int(atom_a_shape[0], M, Rel.EQ, "uint_crd_f_shape", cls_name)
        validator.check_int(atom_b_shape[0], M, Rel.EQ, "atom_b_shape", cls_name)
        validator.check_int(bond_k_shape[0], M, Rel.EQ, "bond_k_shape", cls_name)
        validator.check_int(bond_r0_shape[0], M, Rel.EQ, "bond_r0_shape", cls_name)
        return uint_crd_f_shape

    def infer_dtype(self, uint_crd_f_dtype, scaler_f_type, atom_a_type, atom_b_type, bond_k_type, bond_r0_type):
        validator.check_tensor_dtype_valid('uint_crd_f_dtype', uint_crd_f_dtype, [mstype.uint32], self.name)
        validator.check_tensor_dtype_valid('scaler_f_type', scaler_f_type, [mstype.float32], self.name)
        validator.check_tensor_dtype_valid('atom_a_type', atom_a_type, [mstype.int32], self.name)
        validator.check_tensor_dtype_valid('atom_b_type', atom_b_type, [mstype.int32], self.name)
        validator.check_tensor_dtype_valid('bond_k_type', bond_k_type, [mstype.float32], self.name)
        validator.check_tensor_dtype_valid('bond_r0_type', bond_r0_type, [mstype.float32], self.name)
        return bond_r0_type


class BondEnergy(PrimitiveWithInfer):
    """
    BondEnergyCuda:

    Calculate the harmonic potential energy between each bonded atom pair.
    Assume our system has N atoms and M harmonic bonds.

    .. math::

        dr = (x_1-x_2, y_1-y_2, z_1-z_2)
        E = k*(|dr| - r_0)^2

    Inputs:
        Same as operator BondForce().

    .. math::

        dr = (x_1-x_2, y_1-y_2, z_1-z_2)
        E = k*(|dr| - r_0)^2

    Outputs:
        - **bond_ene** (Tensor, float32) - [M,], the harmonic potential energy
        for each bond.

    Supported Platforms:
        ``GPU``
    Examples:
    """

    @prim_attr_register
    def __init__(self, bond_numbers, atom_numbers):
        self.bond_numbers = bond_numbers
        self.atom_numbers = atom_numbers
        self.add_prim_attr('bond_numbers', self.bond_numbers)
        self.add_prim_attr('atom_numbers', self.atom_numbers)
        self.init_prim_io_names(inputs=['uint_crd_f', 'scaler_f', 'atom_a', 'atom_b', 'bond_k', 'bond_r0'],
                                outputs=['bond_ene'])

    def infer_shape(self, uint_crd_f_shape, scaler_f_shape, atom_a_shape, atom_b_shape, bond_k_shape, bond_r0_shape):
        cls_name = self.name
        N = self.atom_numbers
        M = self.bond_numbers
        validator.check_int(uint_crd_f_shape[0], N, Rel.EQ, "uint_crd_f_shape", cls_name)
        validator.check_int(uint_crd_f_shape[1], 3, Rel.EQ, "uint_crd_f_shape", cls_name)
        validator.check_int(scaler_f_shape[0], 3, Rel.EQ, "scaler_f_shape", cls_name)
        validator.check_int(atom_a_shape[0], M, Rel.EQ, "uint_crd_f_shape", cls_name)
        validator.check_int(atom_b_shape[0], M, Rel.EQ, "atom_b_shape", cls_name)
        validator.check_int(bond_k_shape[0], M, Rel.EQ, "bond_k_shape", cls_name)
        validator.check_int(bond_r0_shape[0], M, Rel.EQ, "bond_r0_shape", cls_name)

        return bond_k_shape

    def infer_dtype(self, uint_crd_f_dtype, scaler_f_type, atom_a_type, atom_b_type, bond_k_type, bond_r0_type):
        validator.check_tensor_dtype_valid('uint_crd_f_dtype', uint_crd_f_dtype, [mstype.uint32], self.name)
        validator.check_tensor_dtype_valid('scaler_f_type', scaler_f_type, [mstype.float32], self.name)
        validator.check_tensor_dtype_valid('atom_a_type', atom_a_type, [mstype.int32], self.name)
        validator.check_tensor_dtype_valid('atom_b_type', atom_b_type, [mstype.int32], self.name)
        validator.check_tensor_dtype_valid('bond_k_type', bond_k_type, [mstype.float32], self.name)
        validator.check_tensor_dtype_valid('bond_r0_type', bond_r0_type, [mstype.float32], self.name)
        return bond_r0_type


class BondAtomEnergy(PrimitiveWithInfer):
    """
    BondAtomEnergyCuda:

    Add the potential energy caused by simple harmonic bonds to the total
    potential energy of each atom.

    The calculation formula is the same as operator BondEnergy().

    Inputs:
        Same as operator BondForce().

    Outputs:
        - **atom_ene** (Tensor, float32) - [N,], the accumulated potential
        energy for each atom.

    Supported Platforms:
        ``GPU``
    Examples:
    """

    @prim_attr_register
    def __init__(self, bond_numbers, atom_numbers):
        self.bond_numbers = bond_numbers
        self.atom_numbers = atom_numbers
        self.add_prim_attr('bond_numbers', self.bond_numbers)
        self.add_prim_attr('atom_numbers', self.atom_numbers)
        self.init_prim_io_names(inputs=['uint_crd_f', 'scaler_f', 'atom_a', 'atom_b', 'bond_k', 'bond_r0'],
                                outputs=['atom_ene'])

    def infer_shape(self, uint_crd_f_shape, scaler_f_shape, atom_a_shape, atom_b_shape, bond_k_shape, bond_r0_shape):
        cls_name = self.name
        N = self.atom_numbers
        M = self.bond_numbers
        validator.check_int(uint_crd_f_shape[0], N, Rel.EQ, "uint_crd_f_shape", cls_name)
        validator.check_int(uint_crd_f_shape[1], 3, Rel.EQ, "uint_crd_f_shape", cls_name)
        validator.check_int(scaler_f_shape[0], 3, Rel.EQ, "scaler_f_shape", cls_name)
        validator.check_int(atom_a_shape[0], M, Rel.EQ, "uint_crd_f_shape", cls_name)
        validator.check_int(atom_b_shape[0], M, Rel.EQ, "atom_b_shape", cls_name)
        validator.check_int(bond_k_shape[0], M, Rel.EQ, "bond_k_shape", cls_name)
        validator.check_int(bond_r0_shape[0], M, Rel.EQ, "bond_r0_shape", cls_name)

        return [N,]

    def infer_dtype(self, uint_crd_f_dtype, scaler_f_type, atom_a_type, atom_b_type, bond_k_type, bond_r0_type):
        validator.check_tensor_dtype_valid('uint_crd_f_dtype', uint_crd_f_dtype, [mstype.uint32], self.name)
        validator.check_tensor_dtype_valid('scaler_f_type', scaler_f_type, [mstype.float32], self.name)
        validator.check_tensor_dtype_valid('atom_a_type', atom_a_type, [mstype.int32], self.name)
        validator.check_tensor_dtype_valid('atom_b_type', atom_b_type, [mstype.int32], self.name)
        validator.check_tensor_dtype_valid('bond_k_type', bond_k_type, [mstype.float32], self.name)
        validator.check_tensor_dtype_valid('bond_r0_type', bond_r0_type, [mstype.float32], self.name)
        return bond_r0_type


class BondForceWithAtomEnergy(PrimitiveWithInfer):
    """
    BondForceWithAtomEnergy:

    Calculate bond force and harmonic potential energy together.

    The calculation formula is the same as operator BondForce() and BondEnergy().

    Inputs:
        Same as operator BondForce().

    Outputs:
        - **frc_f** (Tensor, float32) - [N, 3], same as operator BondForce().
        - **atom_e** (Tensor, float32) - [N,], same as atom_ene in operator BondAtomEnergy().

    Supported Platforms:
        ``GPU``
    Examples:
    """

    @prim_attr_register
    def __init__(self, bond_numbers, atom_numbers):
        self.bond_numbers = bond_numbers
        self.atom_numbers = atom_numbers
        self.add_prim_attr('bond_numbers', self.bond_numbers)
        self.add_prim_attr('atom_numbers', self.atom_numbers)
        self.init_prim_io_names(inputs=['uint_crd_f', 'scaler_f', 'atom_a', 'atom_b', 'bond_k', 'bond_r0'],
                                outputs=['frc_f', 'atom_e'])

    def infer_shape(self, uint_crd_f_shape, scaler_f_shape, atom_a_shape, atom_b_shape, bond_k_shape, bond_r0_shape):
        cls_name = self.name
        N = self.atom_numbers
        M = self.bond_numbers
        validator.check_int(uint_crd_f_shape[0], N, Rel.EQ, "uint_crd_f_shape", cls_name)
        validator.check_int(uint_crd_f_shape[1], 3, Rel.EQ, "uint_crd_f_shape", cls_name)
        validator.check_int(scaler_f_shape[0], 3, Rel.EQ, "scaler_f_shape", cls_name)
        validator.check_int(atom_a_shape[0], M, Rel.EQ, "uint_crd_f_shape", cls_name)
        validator.check_int(atom_b_shape[0], M, Rel.EQ, "atom_b_shape", cls_name)
        validator.check_int(bond_k_shape[0], M, Rel.EQ, "bond_k_shape", cls_name)
        validator.check_int(bond_r0_shape[0], M, Rel.EQ, "bond_r0_shape", cls_name)

        return uint_crd_f_shape, [N,]

    def infer_dtype(self, uint_crd_f_dtype, scaler_f_type, atom_a_type, atom_b_type, bond_k_type, bond_r0_type):
        validator.check_tensor_dtype_valid('uint_crd_f_dtype', uint_crd_f_dtype, [mstype.uint32], self.name)
        validator.check_tensor_dtype_valid('scaler_f_type', scaler_f_type, [mstype.float32], self.name)

        validator.check_tensor_dtype_valid('atom_a_type', atom_a_type, [mstype.int32], self.name)
        validator.check_tensor_dtype_valid('atom_b_type', atom_b_type, [mstype.int32], self.name)

        validator.check_tensor_dtype_valid('bond_k_type', bond_k_type, [mstype.float32], self.name)
        validator.check_tensor_dtype_valid('bond_r0_type', bond_r0_type, [mstype.float32], self.name)
        return bond_r0_type, bond_r0_type


class BondForceWithAtomVirial(PrimitiveWithInfer):
    """
    BondForceWithAtomVirial:

    Calculate bond force and the virial coefficient caused by simple harmonic
    bond for each atom together.

    The calculation formula of the force part is the same as operator BondForce().
    The Virial part is as follows:

    .. math::

        dr = (x_1-x_2, y_1-y_2, z_1-z_2)
        virial = |dr|*(|dr| - r_0)*k

    Inputs:
        Same as operator BondForce()

    Outputs:
        - **frc_f** (Tensor, float32) - [N, 3], same as operator BondForce().
        - **atom_v** (Tensor, float32) - [N,], the accumulated virial coefficient
        for each atom.

    Supported Platforms:
        ``GPU``
    Examples:
    """

    @prim_attr_register
    def __init__(self, bond_numbers, atom_numbers):
        self.bond_numbers = bond_numbers
        self.atom_numbers = atom_numbers
        self.add_prim_attr('bond_numbers', self.bond_numbers)
        self.add_prim_attr('atom_numbers', self.atom_numbers)
        self.init_prim_io_names(inputs=['uint_crd_f', 'scaler_f', 'atom_a', 'atom_b', 'bond_k', 'bond_r0'],
                                outputs=['frc_f', 'atom_v'])

    def infer_shape(self, uint_crd_f_shape, scaler_f_shape, atom_a_shape, atom_b_shape, bond_k_shape, bond_r0_shape):
        cls_name = self.name
        N = self.atom_numbers
        M = self.bond_numbers
        validator.check_int(uint_crd_f_shape[0], N, Rel.EQ, "uint_crd_f_shape", cls_name)
        validator.check_int(uint_crd_f_shape[1], 3, Rel.EQ, "uint_crd_f_shape", cls_name)
        validator.check_int(scaler_f_shape[0], 3, Rel.EQ, "scaler_f_shape", cls_name)
        validator.check_int(atom_a_shape[0], M, Rel.EQ, "uint_crd_f_shape", cls_name)
        validator.check_int(atom_b_shape[0], M, Rel.EQ, "atom_b_shape", cls_name)
        validator.check_int(bond_k_shape[0], M, Rel.EQ, "bond_k_shape", cls_name)
        validator.check_int(bond_r0_shape[0], M, Rel.EQ, "bond_r0_shape", cls_name)

        return uint_crd_f_shape, [N,]

    def infer_dtype(self, uint_crd_f_dtype, scaler_f_type, atom_a_type, atom_b_type, bond_k_type, bond_r0_type):
        validator.check_tensor_dtype_valid('uint_crd_f_dtype', uint_crd_f_dtype, [mstype.uint32], self.name)
        validator.check_tensor_dtype_valid('scaler_f_type', scaler_f_type, [mstype.float32], self.name)

        validator.check_tensor_dtype_valid('atom_a_type', atom_a_type, [mstype.int32], self.name)
        validator.check_tensor_dtype_valid('atom_b_type', atom_b_type, [mstype.int32], self.name)

        validator.check_tensor_dtype_valid('bond_k_type', bond_k_type, [mstype.float32], self.name)
        validator.check_tensor_dtype_valid('bond_r0_type', bond_r0_type, [mstype.float32], self.name)
        return bond_r0_type, bond_r0_type


class DihedralForce(PrimitiveWithInfer):
    """
    DihedralForce:

    Calculate the force exerted by the dihedral term which made of 4-atoms
    on the corresponding atoms. Assume the number of dihedral terms is M and
    the number of atoms is N.

    .. math::

        dr_{ab} = (x_b-x_a, y_b-y_a, z_b-z_a)
        dr_{cb} = (x_b-x_c, y_b-y_c, z_b-z_c)
        dr_{cd} = (x_d-x_c, y_d-y_c, z_d-z_c)

        r1 = dr_{ab}*dr_{cb}
        r2 = dr_{cd}*dr_{cb}

        phi = pi - sign(inner_product(r1*r2), dr_{cb})
            * arccos(inner_product(r1, r2)/|r1|/|r2|)
        dEdphi = n*phi*(k*cos(phi_0)*sin(n*phi) - k*sin(phi_0)*cos(n*phi))/sin(phi)
        dphidr1 = r2/|r1|/|r2| + cos(phi)/|r1|^2*r1
        dphidr2 = r1/|r1|/|r2| + cos(phi)/|r2|^2*r2

        dEdra = dEdphi * dr_{cb} * dphidr1
        dEdrd = dEdphi * dphi_dr2 * dr_{cb}
        dEdrjpart = dEdphi * ((dr_{ab} * dphidr1) + (dr_{cd} * dphidr2))

        F_a = dEdri
        F_b = dEdrjpart - dEdri
        F_c = - dEdrl - dEdrjpart
        F_d = dEdrl

    Inputs:
        - **dihedral_numbers** (int32) - the number of dihedral terms M.
        - **uint_crd_f** (Tensor, uint32) - [N, 3], the unsigned int coordinates
        value of each atom.
        - **scalar_f** (Tensor, float32) - [3, ], the 3-D scale factor between
        the real space float coordinates and the unsigned int coordinates.
        - **atom_a** (Tensor, int32) - [M, ], the 1st atom index of each dihedral.
        - **atom_b** (Tensor, int32) - [M, ], the 2nd atom index of each dihedral.
        - **atom_c** (Tensor, int32) - [M, ], the 3rd atom index of each dihedral.
        - **atom_d** (Tensor, int32) - [M, ], the 4th atom index of each dihedral.
        4 atoms are connected in the form a-b-c-d.
        - **ipn** (Tensor, int32) - [M, ], the period of dihedral angle of each dihedral.
        - **pk** (Tensor, float32) - [M, ], the force constant of each dihedral.
        - **gamc** (Tensor, float32) - [M, ], k*cos(phi_0) of each dihedral.
        - **gams** (Tensor, float32) - [M, ], k*sin(phi_0) of each dihedral.
        - **pn** (Tensor, float32) - [M, ], the floating point form of ipn.

    Outputs:
        - **frc_f** (Tensor, float32) - [N, 3], the force felt by each atom.

    Supported Platforms:
        ``GPU``

    Examples:
    """

    @prim_attr_register
    def __init__(self, dihedral_numbers):
        self.dihedral_numbers = dihedral_numbers
        self.init_prim_io_names(inputs=['uint_crd_f', 'scaler_f', 'atom_a', 'atom_b', 'atom_c', 'atom_d', 'ipn', 'pk',
                                        'gamc', 'gams', 'pn'],
                                outputs=['frc_f'])
        self.add_prim_attr('dihedral_numbers', self.dihedral_numbers)

    def infer_shape(self, uint_crd_f_shape, scaler_f_shape, atom_a_shape, atom_b_shape, atom_c_shape, atom_d_shape,
                    ipn_shape, pk_shape, gamc_shape, gams_shape, pn_shape):
        cls_name = self.name
        M = atom_a_shape[0]
        validator.check_int(uint_crd_f_shape[1], 3, Rel.EQ, "uint_crd_f_shape", cls_name)
        validator.check_int(scaler_f_shape[0], 3, Rel.EQ, "scaler_f_shape", cls_name)
        validator.check_int(atom_a_shape[0], M, Rel.EQ, "atom_a_shape", cls_name)
        validator.check_int(atom_b_shape[0], M, Rel.EQ, "atom_b_shape", cls_name)
        validator.check_int(atom_c_shape[0], M, Rel.EQ, "atom_c_shape", cls_name)
        validator.check_int(atom_d_shape[0], M, Rel.EQ, "atom_d_shape", cls_name)
        validator.check_int(ipn_shape[0], M, Rel.EQ, "ipn_shape", cls_name)
        validator.check_int(pk_shape[0], M, Rel.EQ, "pk_shape", cls_name)
        validator.check_int(gamc_shape[0], M, Rel.EQ, "gamc_shape", cls_name)
        validator.check_int(gams_shape[0], M, Rel.EQ, "gams_shape", cls_name)
        validator.check_int(pn_shape[0], M, Rel.EQ, "pn_shape", cls_name)
        return uint_crd_f_shape

    def infer_dtype(self, uint_crd_f_dtype, scaler_f_type, atom_a_type, atom_b_type, atom_c_type, atom_d_type,
                    ipn_type, pk_type, gamc_type, gams_type, pn_type):
        validator.check_tensor_dtype_valid('uint_crd_f_dtype', uint_crd_f_dtype, [mstype.uint32], self.name)
        validator.check_tensor_dtype_valid('scaler_f_type', scaler_f_type, [mstype.float32], self.name)
        validator.check_tensor_dtype_valid('atom_a_type', atom_a_type, [mstype.int32], self.name)
        validator.check_tensor_dtype_valid('atom_b_type', atom_b_type, [mstype.int32], self.name)
        validator.check_tensor_dtype_valid('atom_c_type', atom_c_type, [mstype.int32], self.name)
        validator.check_tensor_dtype_valid('atom_d_type', atom_d_type, [mstype.int32], self.name)
        validator.check_tensor_dtype_valid('ipn_type', ipn_type, [mstype.int32], self.name)
        validator.check_tensor_dtype_valid('pk_type', pk_type, [mstype.float32], self.name)
        validator.check_tensor_dtype_valid('gamc_type', gamc_type, [mstype.float32], self.name)
        validator.check_tensor_dtype_valid('gams_type', gams_type, [mstype.float32], self.name)
        validator.check_tensor_dtype_valid('pn_type', pn_type, [mstype.float32], self.name)

        return pn_type


class DihedralEnergy(PrimitiveWithInfer):
    """
    DihedralEnergy:

    Calculate the potential energy caused by dihedral terms for each 4-atom pair.
    Assume our system has N atoms and M dihedral terms.

    .. math::

        E = k(1 + cos(n*phi - phi_0))

    Inputs:
        Same as operator DihedralForce().

    Outputs:
        - **ene** (Tensor, float32) - [M, ], the potential energy for each
        dihedral term.

    Supported Platforms:
        ``GPU``

    Examples:
    """

    @prim_attr_register
    def __init__(self, dihedral_numbers):
        self.dihedral_numbers = dihedral_numbers
        self.init_prim_io_names(inputs=['uint_crd_f', 'scaler_f', 'atom_a', 'atom_b', 'atom_c', 'atom_d', 'ipn', 'pk',
                                        'gamc', 'gams', 'pn'],
                                outputs=['ene'])
        self.add_prim_attr('dihedral_numbers', self.dihedral_numbers)

    def infer_shape(self, uint_crd_f_shape, scaler_f_shape, atom_a_shape, atom_b_shape, atom_c_shape, atom_d_shape,
                    ipn_shape, pk_shape, gamc_shape, gams_shape, pn_shape):
        cls_name = self.name
        M = atom_a_shape[0]
        validator.check_int(uint_crd_f_shape[1], 3, Rel.EQ, "uint_crd_f_shape", cls_name)
        validator.check_int(scaler_f_shape[0], 3, Rel.EQ, "scaler_f_shape", cls_name)
        validator.check_int(atom_a_shape[0], M, Rel.EQ, "atom_a_shape", cls_name)
        validator.check_int(atom_b_shape[0], M, Rel.EQ, "atom_b_shape", cls_name)
        validator.check_int(atom_c_shape[0], M, Rel.EQ, "atom_c_shape", cls_name)
        validator.check_int(atom_d_shape[0], M, Rel.EQ, "atom_d_shape", cls_name)
        validator.check_int(ipn_shape[0], M, Rel.EQ, "ipn_shape", cls_name)
        validator.check_int(pk_shape[0], M, Rel.EQ, "pk_shape", cls_name)
        validator.check_int(gamc_shape[0], M, Rel.EQ, "gamc_shape", cls_name)
        validator.check_int(gams_shape[0], M, Rel.EQ, "gams_shape", cls_name)
        validator.check_int(pn_shape[0], M, Rel.EQ, "pn_shape", cls_name)
        return [M,]

    def infer_dtype(self, uint_crd_f_dtype, scaler_f_type, atom_a_type, atom_b_type, atom_c_type, atom_d_type,
                    ipn_type, pk_type, gamc_type, gams_type, pn_type):
        validator.check_tensor_dtype_valid('uint_crd_f_dtype', uint_crd_f_dtype, [mstype.uint32], self.name)
        validator.check_tensor_dtype_valid('scaler_f_type', scaler_f_type, [mstype.float32], self.name)
        validator.check_tensor_dtype_valid('atom_a_type', atom_a_type, [mstype.int32], self.name)
        validator.check_tensor_dtype_valid('atom_b_type', atom_b_type, [mstype.int32], self.name)
        validator.check_tensor_dtype_valid('atom_c_type', atom_c_type, [mstype.int32], self.name)
        validator.check_tensor_dtype_valid('atom_d_type', atom_d_type, [mstype.int32], self.name)
        validator.check_tensor_dtype_valid('ipn_type', ipn_type, [mstype.int32], self.name)
        validator.check_tensor_dtype_valid('pk_type', pk_type, [mstype.float32], self.name)
        validator.check_tensor_dtype_valid('gamc_type', gamc_type, [mstype.float32], self.name)
        validator.check_tensor_dtype_valid('gams_type', gams_type, [mstype.float32], self.name)
        validator.check_tensor_dtype_valid('pn_type', pn_type, [mstype.float32], self.name)

        return pn_type


class DihedralAtomEnergy(PrimitiveWithInfer):
    """
    DihedralAtomEnergy:

    Add the potential energy caused by dihedral terms to the total potential
    energy of each atom.

    The calculation formula is the same as operator DihedralEnergy().

    Inputs:
        Same as operator DihedralEnergy().

    Outputs:
        - **ene** (Tensor, float32) - [N, ], the accumulated potential
        energy for each atom.

    Supported Platforms:
        ``GPU``

    Examples:
    """

    @prim_attr_register
    def __init__(self, dihedral_numbers):
        self.dihedral_numbers = dihedral_numbers
        self.init_prim_io_names(inputs=['uint_crd_f', 'scaler_f', 'atom_a', 'atom_b', 'atom_c', 'atom_d', 'ipn', 'pk',
                                        'gamc', 'gams', 'pn'],
                                outputs=['ene'])
        self.add_prim_attr('dihedral_numbers', self.dihedral_numbers)

    def infer_shape(self, uint_crd_f_shape, scaler_f_shape, atom_a_shape, atom_b_shape, atom_c_shape, atom_d_shape,
                    ipn_shape, pk_shape, gamc_shape, gams_shape, pn_shape):
        cls_name = self.name
        N = uint_crd_f_shape[0]
        M = atom_a_shape[0]
        validator.check_int(uint_crd_f_shape[1], 3, Rel.EQ, "uint_crd_f_shape", cls_name)
        validator.check_int(scaler_f_shape[0], 3, Rel.EQ, "scaler_f_shape", cls_name)
        validator.check_int(atom_a_shape[0], M, Rel.EQ, "atom_a_shape", cls_name)
        validator.check_int(atom_b_shape[0], M, Rel.EQ, "atom_b_shape", cls_name)
        validator.check_int(atom_c_shape[0], M, Rel.EQ, "atom_c_shape", cls_name)
        validator.check_int(atom_d_shape[0], M, Rel.EQ, "atom_d_shape", cls_name)
        validator.check_int(ipn_shape[0], M, Rel.EQ, "ipn_shape", cls_name)
        validator.check_int(pk_shape[0], M, Rel.EQ, "pk_shape", cls_name)
        validator.check_int(gamc_shape[0], M, Rel.EQ, "gamc_shape", cls_name)
        validator.check_int(gams_shape[0], M, Rel.EQ, "gams_shape", cls_name)
        validator.check_int(pn_shape[0], M, Rel.EQ, "pn_shape", cls_name)
        return [N,]

    def infer_dtype(self, uint_crd_f_dtype, scaler_f_type, atom_a_type, atom_b_type, atom_c_type, atom_d_type,
                    ipn_type, pk_type, gamc_type, gams_type, pn_type):
        validator.check_tensor_dtype_valid('uint_crd_f_dtype', uint_crd_f_dtype, [mstype.uint32], self.name)
        validator.check_tensor_dtype_valid('scaler_f_type', scaler_f_type, [mstype.float32], self.name)
        validator.check_tensor_dtype_valid('atom_a_type', atom_a_type, [mstype.int32], self.name)
        validator.check_tensor_dtype_valid('atom_b_type', atom_b_type, [mstype.int32], self.name)
        validator.check_tensor_dtype_valid('atom_c_type', atom_c_type, [mstype.int32], self.name)
        validator.check_tensor_dtype_valid('atom_d_type', atom_d_type, [mstype.int32], self.name)
        validator.check_tensor_dtype_valid('ipn_type', ipn_type, [mstype.int32], self.name)
        validator.check_tensor_dtype_valid('pk_type', pk_type, [mstype.float32], self.name)
        validator.check_tensor_dtype_valid('gamc_type', gamc_type, [mstype.float32], self.name)
        validator.check_tensor_dtype_valid('gams_type', gams_type, [mstype.float32], self.name)
        validator.check_tensor_dtype_valid('pn_type', pn_type, [mstype.float32], self.name)

        return pn_type


class DihedralForceWithAtomEnergy(PrimitiveWithInfer):
    """
    DihedralForceWithAtomEnergy:

    Calculate dihedral force and potential energy together.

    The calculation formula is the same as operator DihedralForce() and DihedralEnergy().

    Inputs:
        Same as operator DihedralForce().

    Outputs:
        - **frc_f** (Tensor, float32) - [N, 3], same as operator DihedralForce().
        - **ene** (Tensor, float32) - [N, ], same as operator DihedralAtomEnergy().

    Supported Platforms:
        ``GPU``

    Examples:
    """

    @prim_attr_register
    def __init__(self, dihedral_numbers):
        self.dihedral_numbers = dihedral_numbers
        self.init_prim_io_names(inputs=['uint_crd_f', 'scaler_f', 'atom_a', 'atom_b', 'atom_c', 'atom_d', 'ipn', 'pk',
                                        'gamc', 'gams', 'pn'],
                                outputs=['frc_f', 'ene'])
        self.add_prim_attr('dihedral_numbers', self.dihedral_numbers)

    def infer_shape(self, uint_crd_f_shape, scaler_f_shape, atom_a_shape, atom_b_shape, atom_c_shape, atom_d_shape,
                    ipn_shape, pk_shape, gamc_shape, gams_shape, pn_shape):
        cls_name = self.name
        N = uint_crd_f_shape[0]
        M = atom_a_shape[0]
        validator.check_int(uint_crd_f_shape[1], 3, Rel.EQ, "uint_crd_f_shape", cls_name)
        validator.check_int(scaler_f_shape[0], 3, Rel.EQ, "scaler_f_shape", cls_name)
        validator.check_int(atom_a_shape[0], M, Rel.EQ, "atom_a_shape", cls_name)
        validator.check_int(atom_b_shape[0], M, Rel.EQ, "atom_b_shape", cls_name)
        validator.check_int(atom_c_shape[0], M, Rel.EQ, "atom_c_shape", cls_name)
        validator.check_int(atom_d_shape[0], M, Rel.EQ, "atom_d_shape", cls_name)
        validator.check_int(ipn_shape[0], M, Rel.EQ, "ipn_shape", cls_name)
        validator.check_int(pk_shape[0], M, Rel.EQ, "pk_shape", cls_name)
        validator.check_int(gamc_shape[0], M, Rel.EQ, "gamc_shape", cls_name)
        validator.check_int(gams_shape[0], M, Rel.EQ, "gams_shape", cls_name)
        validator.check_int(pn_shape[0], M, Rel.EQ, "pn_shape", cls_name)
        return uint_crd_f_shape, [N,]

    def infer_dtype(self, uint_crd_f_dtype, scaler_f_type, atom_a_type, atom_b_type, atom_c_type, atom_d_type,
                    ipn_type, pk_type, gamc_type, gams_type, pn_type):
        validator.check_tensor_dtype_valid('uint_crd_f_dtype', uint_crd_f_dtype, [mstype.uint32], self.name)
        validator.check_tensor_dtype_valid('scaler_f_type', scaler_f_type, [mstype.float32], self.name)
        validator.check_tensor_dtype_valid('atom_a_type', atom_a_type, [mstype.int32], self.name)
        validator.check_tensor_dtype_valid('atom_b_type', atom_b_type, [mstype.int32], self.name)
        validator.check_tensor_dtype_valid('atom_c_type', atom_c_type, [mstype.int32], self.name)
        validator.check_tensor_dtype_valid('atom_d_type', atom_d_type, [mstype.int32], self.name)
        validator.check_tensor_dtype_valid('ipn_type', ipn_type, [mstype.int32], self.name)
        validator.check_tensor_dtype_valid('pk_type', pk_type, [mstype.float32], self.name)
        validator.check_tensor_dtype_valid('gamc_type', gamc_type, [mstype.float32], self.name)
        validator.check_tensor_dtype_valid('gams_type', gams_type, [mstype.float32], self.name)
        validator.check_tensor_dtype_valid('pn_type', pn_type, [mstype.float32], self.name)

        return pn_type, pn_type


class AngleForce(PrimitiveWithInfer):
    """
    AngleForce:

    Calculate the force exerted by angles made of 3 atoms on the
    corresponding atoms. Assume the number of angles is M and the
    number of atoms is N.

    .. math::

        dr_{ab} = (x_b-x_a, y_b-y_a, z_b-z_a)
        dr_{cb} = (x_b-x_c, y_b-y_c, z_b-z_c)
        theta = arccos(inner_product(dr_{ab}, dr_{cb})/|dr_{ab}|/|dr_{cb}|)
        F_a = -2*k*(theta-theta_0)/sin(theta)*[cos(theta)/|dr_{ab}|^2*dr_{ab}
            - 1/|dr_{ab}|/|dr_{cb}|*dr_{cb}]
        F_c = -2*k*(theta-theta_0)/sin(theta)*[cos(theta)/|dr_{cb}|^2*dr_{cb}
             - 1/|dr_{cb}|/|dr_{ab}|*dr_{ab}]
        F_b = -F_a - F_c

    Inputs:
        - **angle_numbers** (int32) - the number of angles M.
        - **uint_crd_f** (Tensor, uint32) - [N, 3], the unsigned int coordinate
        value of each atom.
        - **scaler_f** (Tensor, float32) - [3, ], the 3-D scale factor between
        the real space float coordinates and the unsigned int coordinates.
        - **atom_a** (Tensor, int32) - [M, ], the 1st atom index of each angle.
        - **atom_b** (Tensor, int32) - [M, ], the 2nd and the central atom index
        of each angle.
        - **atom_c** (Tensor, int32) - [M, ], the 3rd atom index of each angle.
        - **angle_k** (Tensor, float32) - [M, ], the force constant for each angle.
        - **angle_theta0** (Tensor, float32) - [M, ], the equilibrium position value
        for each angle.

    Outputs:
        - **frc_f** (Tensor, float32) - [N, 3], the force felt by each atom.

    Supported Platforms:
        ``GPU``

    Examples:
    """

    @prim_attr_register
    def __init__(self, angle_numbers):
        self.angle_numbers = angle_numbers
        self.init_prim_io_names(inputs=['uint_crd_f', 'scaler_f', 'atom_a', 'atom_b', 'atom_c', 'angle_k',
                                        'angle_theta0'],
                                outputs=['frc_f'])
        self.add_prim_attr('angle_numbers', self.angle_numbers)

    def infer_shape(self, uint_crd_f_shape, scaler_f_shape, atom_a_shape, atom_b_shape, atom_c_shape, angle_k_shape,
                    angle_theta0_shape):
        cls_name = self.name
        M = atom_a_shape[0]
        validator.check_int(uint_crd_f_shape[1], 3, Rel.EQ, "uint_crd_f_shape", cls_name)
        validator.check_int(scaler_f_shape[0], 3, Rel.EQ, "scaler_f_shape", cls_name)
        validator.check_int(atom_a_shape[0], M, Rel.EQ, "atom_a_shape", cls_name)
        validator.check_int(atom_b_shape[0], M, Rel.EQ, "atom_b_shape", cls_name)
        validator.check_int(atom_c_shape[0], M, Rel.EQ, "atom_c_shape", cls_name)
        validator.check_int(angle_k_shape[0], M, Rel.EQ, "angle_k_shape", cls_name)
        validator.check_int(angle_theta0_shape[0], M, Rel.EQ, "angle_theta0_shape", cls_name)
        return uint_crd_f_shape

    def infer_dtype(self, uint_crd_f_dtype, scaler_f_type, atom_a_type, atom_b_type, atom_c_type, angle_k_type,
                    angle_theta0_type):
        validator.check_tensor_dtype_valid('uint_crd_f_dtype', uint_crd_f_dtype, [mstype.uint32], self.name)
        validator.check_tensor_dtype_valid('scaler_f_type', scaler_f_type, [mstype.float32], self.name)
        validator.check_tensor_dtype_valid('atom_a_type', atom_a_type, [mstype.int32], self.name)
        validator.check_tensor_dtype_valid('atom_b_type', atom_b_type, [mstype.int32], self.name)
        validator.check_tensor_dtype_valid('atom_c_type', atom_c_type, [mstype.int32], self.name)
        validator.check_tensor_dtype_valid('angle_k_type', angle_k_type, [mstype.float32], self.name)
        validator.check_tensor_dtype_valid('angle_theta0_type', angle_theta0_type, [mstype.float32], self.name)
        return angle_k_type


class AngleEnergy(PrimitiveWithInfer):
    """
    AngleEnergy:

    Calculate the energy caused by 3-atoms angle term.

    .. math::

        dr_{ab} = (x_b-x_a, y_b-y_a, z_b-z_a)
        dr_{cb} = (x_b-x_c, y_b-y_c, z_b-z_c)
        theta = arccos(inner_product(dr_{ab}, dr_{cb})/|dr_{ab}|/|dr_{cb}|)
        E = k*(theta - theta_0)^2

    Inputs:
        Same as operator AngleForce().

    Outputs:
        - **ene** (Tensor, float32) - [M, ], the potential energy for
        each angle term.

    Supported Platforms:
        ``GPU``

    Examples:
    """

    @prim_attr_register
    def __init__(self, angle_numbers):
        self.angle_numbers = angle_numbers
        self.init_prim_io_names(inputs=['uint_crd_f', 'scaler_f', 'atom_a', 'atom_b', 'atom_c', 'angle_k',
                                        'angle_theta0'],
                                outputs=['ene'])
        self.add_prim_attr('angle_numbers', self.angle_numbers)

    def infer_shape(self, uint_crd_f_shape, scaler_f_shape, atom_a_shape, atom_b_shape, atom_c_shape, angle_k_shape,
                    angle_theta0_shape):
        cls_name = self.name
        M = atom_a_shape[0]
        validator.check_int(uint_crd_f_shape[1], 3, Rel.EQ, "uint_crd_f_shape", cls_name)
        validator.check_int(scaler_f_shape[0], 3, Rel.EQ, "scaler_f_shape", cls_name)
        validator.check_int(atom_a_shape[0], M, Rel.EQ, "atom_a_shape", cls_name)
        validator.check_int(atom_b_shape[0], M, Rel.EQ, "atom_b_shape", cls_name)
        validator.check_int(atom_c_shape[0], M, Rel.EQ, "atom_c_shape", cls_name)
        validator.check_int(angle_k_shape[0], M, Rel.EQ, "angle_k_shape", cls_name)
        validator.check_int(angle_theta0_shape[0], M, Rel.EQ, "angle_theta0_shape", cls_name)
        return [M,]

    def infer_dtype(self, uint_crd_f_dtype, scaler_f_type, atom_a_type, atom_b_type, atom_c_type, angle_k_type,
                    angle_theta0_type):
        validator.check_tensor_dtype_valid('uint_crd_f_dtype', uint_crd_f_dtype, [mstype.uint32], self.name)
        validator.check_tensor_dtype_valid('scaler_f_type', scaler_f_type, [mstype.float32], self.name)
        validator.check_tensor_dtype_valid('atom_a_type', atom_a_type, [mstype.int32], self.name)
        validator.check_tensor_dtype_valid('atom_b_type', atom_b_type, [mstype.int32], self.name)
        validator.check_tensor_dtype_valid('atom_c_type', atom_c_type, [mstype.int32], self.name)
        validator.check_tensor_dtype_valid('angle_k_type', angle_k_type, [mstype.float32], self.name)
        validator.check_tensor_dtype_valid('angle_theta0_type', angle_theta0_type, [mstype.float32], self.name)
        return angle_k_type


class AngleAtomEnergy(PrimitiveWithInfer):
    """
    AngleAtomEnergy:

    Add the potential energy caused by angle terms to the total potential
    energy of each atom.

    The calculation formula is the same as operator AngleEnergy().

    Inputs:
        Same as operator AngleForce().

    Outputs:
        - **ene** (Tensor, float32) - [N, ], the accumulated potential energy
        for each atom.

    Supported Platforms:
        ``GPU``

    Examples:
    """

    @prim_attr_register
    def __init__(self, angle_numbers):
        self.angle_numbers = angle_numbers
        self.init_prim_io_names(inputs=['uint_crd_f', 'scaler_f', 'atom_a', 'atom_b', 'atom_c', 'angle_k',
                                        'angle_theta0'],
                                outputs=['ene'])
        self.add_prim_attr('angle_numbers', self.angle_numbers)

    def infer_shape(self, uint_crd_f_shape, scaler_f_shape, atom_a_shape, atom_b_shape, atom_c_shape, angle_k_shape,
                    angle_theta0_shape):
        cls_name = self.name
        N = uint_crd_f_shape[0]
        M = atom_a_shape[0]
        validator.check_int(uint_crd_f_shape[1], 3, Rel.EQ, "uint_crd_f_shape", cls_name)
        validator.check_int(scaler_f_shape[0], 3, Rel.EQ, "scaler_f_shape", cls_name)
        validator.check_int(atom_a_shape[0], M, Rel.EQ, "atom_a_shape", cls_name)
        validator.check_int(atom_b_shape[0], M, Rel.EQ, "atom_b_shape", cls_name)
        validator.check_int(atom_c_shape[0], M, Rel.EQ, "atom_c_shape", cls_name)
        validator.check_int(angle_k_shape[0], M, Rel.EQ, "angle_k_shape", cls_name)
        validator.check_int(angle_theta0_shape[0], M, Rel.EQ, "angle_theta0_shape", cls_name)
        return [N,]

    def infer_dtype(self, uint_crd_f_dtype, scaler_f_type, atom_a_type, atom_b_type, atom_c_type, angle_k_type,
                    angle_theta0_type):
        validator.check_tensor_dtype_valid('uint_crd_f_dtype', uint_crd_f_dtype, [mstype.uint32], self.name)
        validator.check_tensor_dtype_valid('scaler_f_type', scaler_f_type, [mstype.float32], self.name)
        validator.check_tensor_dtype_valid('atom_a_type', atom_a_type, [mstype.int32], self.name)
        validator.check_tensor_dtype_valid('atom_b_type', atom_b_type, [mstype.int32], self.name)
        validator.check_tensor_dtype_valid('atom_c_type', atom_c_type, [mstype.int32], self.name)
        validator.check_tensor_dtype_valid('angle_k_type', angle_k_type, [mstype.float32], self.name)
        validator.check_tensor_dtype_valid('angle_theta0_type', angle_theta0_type, [mstype.float32], self.name)
        return angle_k_type


class AngleForceWithAtomEnergy(PrimitiveWithInfer):
    """
    AngleForceWithAtomEnergy:

    Calculate angle force and potential energy together.

    The calculation formula is the same as operator AngleForce() and AngleEnergy().

    Inputs:
        Same as operator AngleForce().

    Outputs:
        - **frc_f** (Tensor, float32) - [N, 3], same as operator AngleForce().
        - **ene** (Tensor, float) - [N, ], same as operator AngleAtomEnergy().

    Supported Platforms:
        ``GPU``

    Examples:
    """

    @prim_attr_register
    def __init__(self, angle_numbers):
        self.angle_numbers = angle_numbers
        self.init_prim_io_names(inputs=['uint_crd_f', 'scaler_f', 'atom_a', 'atom_b', 'atom_c', 'angle_k',
                                        'angle_theta0'],
                                outputs=['frc_f', 'ene'])
        self.add_prim_attr('angle_numbers', self.angle_numbers)

    def infer_shape(self, uint_crd_f_shape, scaler_f_shape, atom_a_shape, atom_b_shape, atom_c_shape, angle_k_shape,
                    angle_theta0_shape):
        cls_name = self.name
        N = uint_crd_f_shape[0]
        M = atom_a_shape[0]
        validator.check_int(uint_crd_f_shape[1], 3, Rel.EQ, "uint_crd_f_shape", cls_name)
        validator.check_int(scaler_f_shape[0], 3, Rel.EQ, "scaler_f_shape", cls_name)
        validator.check_int(atom_a_shape[0], M, Rel.EQ, "atom_a_shape", cls_name)
        validator.check_int(atom_b_shape[0], M, Rel.EQ, "atom_b_shape", cls_name)
        validator.check_int(atom_c_shape[0], M, Rel.EQ, "atom_c_shape", cls_name)
        validator.check_int(angle_k_shape[0], M, Rel.EQ, "angle_k_shape", cls_name)
        validator.check_int(angle_theta0_shape[0], M, Rel.EQ, "angle_theta0_shape", cls_name)
        return uint_crd_f_shape, [N,]

    def infer_dtype(self, uint_crd_f_dtype, scaler_f_type, atom_a_type, atom_b_type, atom_c_type, angle_k_type,
                    angle_theta0_type):
        validator.check_tensor_dtype_valid('uint_crd_f_dtype', uint_crd_f_dtype, [mstype.uint32], self.name)
        validator.check_tensor_dtype_valid('scaler_f_type', scaler_f_type, [mstype.float32], self.name)
        validator.check_tensor_dtype_valid('atom_a_type', atom_a_type, [mstype.int32], self.name)
        validator.check_tensor_dtype_valid('atom_b_type', atom_b_type, [mstype.int32], self.name)
        validator.check_tensor_dtype_valid('atom_c_type', atom_c_type, [mstype.int32], self.name)
        validator.check_tensor_dtype_valid('angle_k_type', angle_k_type, [mstype.float32], self.name)
        validator.check_tensor_dtype_valid('angle_theta0_type', angle_theta0_type, [mstype.float32], self.name)
        return angle_k_type, angle_k_type


class Dihedral14LJForce(PrimitiveWithInfer):
    """
    Dihedral14LJForce:

    Calculate the Lennard-Jones part of 1,4 dihedral force correction for
    each necessary dihedral terms on the corresponding atoms. Assume the
    number of necessary dihedral 1,4 terms is M, the number of atoms is N,
    and the number of Lennard-Jones types for all atoms is P, which means
    there will be Q = P*(P+1)/2 types of possible Lennard-Jones interactions
    for all kinds of atom pairs.

    .. math::

        dr = (x_a-x_b, y_a-y_b, z_a-z_b)
        F = k*(-12*A/|dr|^{14} + 6*B/|dr|^{8})*dr

    Inputs:
        - **dihedral_14_numbers** (int32) - the number of necessary dihedral
        1,4 terms M.
        - **atom_numbers** (int32) - the number of atoms N.
        - **uint_crd_f** (Tensor, uint32) - [N, 3], the unsigned int coordinate
        value of each atom.
        - **LJ_type** (Tensor, int32) - [N,], the Lennard-Jones type of each
        atom.
        - **charge** (Tensor, float32) - [N,], the charge of each atom.
        - **boxlength_f** (Tensor, float32) - [3,], the length of molecular
        simulation box in 3 dimensions.
        - **a_14** (Tensor, int32) - [M,], the first atom index of each dihedral
        1,4 term.
        - **b_14** (Tensor, int32) - [M,], the second atom index of each dihedral
        1,4 term.
        - **lj_scale_factor** (Tensor, float32) - [M,], the scale factor for the
        Lennard-Jones part of force correction of each dihedral 1,4 term.
        - **LJ_type_A** (Tensor, float32) - [Q,], the A parameter in Lennard-Jones
        scheme of each atom pair type.
        - **LJ_type_B** (Tensor, float32) - [Q,], the B parameter in Lennard-Jones
        shceme of each atom pair type.

    Outputs:
        - **frc_f** (Tensor, float32) - [N, 3], the force felt by each atom.

    Supported Platforms:
        ``GPU``
    Examples:
    """

    @prim_attr_register
    def __init__(self, nb14_numbers, atom_numbers):
        self.dihedral_14_numbers = nb14_numbers
        self.atom_numbers = atom_numbers
        self.init_prim_io_names(
            inputs=['uint_crd_f', 'LJtype', 'charge', 'boxlength_f', 'a_14', 'b_14', 'lj_scale_factor',
                    'LJ_type_A', 'LJ_type_B'],
            outputs=['frc_f'])
        self.add_prim_attr('dihedral_14_numbers', self.dihedral_14_numbers)
        self.add_prim_attr('atom_numbers', self.atom_numbers)

    def infer_shape(self, uint_crd_f_shape, LJtype_shape, charge_shape, boxlength_f_shape, a_14_shape, b_14_shape,
                    lj_scale_factor_shape,
                    LJ_type_A_shape, LJ_type_B_shape):
        return uint_crd_f_shape

    def infer_dtype(self, uint_crd_f_dtype, LJtype_dtype, charge_dtype, boxlength_f_type, a_14_type, b_14_type,
                    lj_scale_factor_type, LJ_type_A_type, LJ_type_B_type):
        validator.check_tensor_dtype_valid('uint_crd_f_dtype', uint_crd_f_dtype, [mstype.uint32], self.name)
        validator.check_tensor_dtype_valid('LJtype_dtype', LJtype_dtype, [mstype.int32], self.name)
        validator.check_tensor_dtype_valid('charge_dtype', charge_dtype, [mstype.float32], self.name)
        validator.check_tensor_dtype_valid('boxlength_f_type', boxlength_f_type, [mstype.float32], self.name)

        validator.check_tensor_dtype_valid('a_14_type', a_14_type, [mstype.int32], self.name)
        validator.check_tensor_dtype_valid('b_14_type', b_14_type, [mstype.int32], self.name)

        validator.check_tensor_dtype_valid('lj_scale_factor_type', lj_scale_factor_type, [mstype.float32], self.name)
        validator.check_tensor_dtype_valid('LJ_type_A_type', LJ_type_A_type, [mstype.float32], self.name)
        validator.check_tensor_dtype_valid('LJ_type_B_type', LJ_type_B_type, [mstype.float32], self.name)
        return LJ_type_B_type


class Dihedral14LJEnergy(PrimitiveWithInfer):
    """
    Dihedral14LJEnergy:

    Calculate the Lennard-Jones part of 1,4 dihedral energy correction for
    each necessary dihedral terms on the corresponding atoms.

    .. math:, the :

        dr = (x_a-x_b, y_a-y_b, z_a-z-b)
        E = k*(A/|dr|^{12} - B/|dr|^{6})

    Inputs:
        Same as operator Dihedral14LJForce().

    Outputs:
        - **ene** (Tensor, float32) - [M,], the Lennard-Jones potential
        energy correction for each necessary dihedral 1,4 term.

    Supported Platforms:
        ``GPU``
    Examples:
    """

    @prim_attr_register
    def __init__(self, nb14_numbers, atom_numbers):
        self.dihedral_14_numbers = nb14_numbers
        self.atom_numbers = atom_numbers

        self.init_prim_io_names(
            inputs=['uint_crd_f', 'LJtype', 'charge', 'boxlength_f', 'a_14', 'b_14', 'lj_scale_factor',
                    'LJ_type_A', 'LJ_type_B'],
            outputs=['ene'])
        self.add_prim_attr('dihedral_14_numbers', self.dihedral_14_numbers)
        self.add_prim_attr('atom_numbers', self.atom_numbers)

    def infer_shape(self, uint_crd_f_shape, LJtype_shape, charge_shape, boxlength_f_shape, a_14_shape, b_14_shape,
                    lj_scale_factor_shape, LJ_type_A_shape, LJ_type_B_shape):
        return [self.dihedral_14_numbers,]

    def infer_dtype(self, uint_crd_f_dtype, LJtype_dtype, charge_dtype, boxlength_f_type, a_14_type, b_14_type,
                    lj_scale_factor_type, LJ_type_A_type, LJ_type_B_type):
        validator.check_tensor_dtype_valid('uint_crd_f_dtype', uint_crd_f_dtype, [mstype.uint32], self.name)
        validator.check_tensor_dtype_valid('LJtype_dtype', LJtype_dtype, [mstype.int32], self.name)
        validator.check_tensor_dtype_valid('charge_dtype', charge_dtype, [mstype.float32], self.name)
        validator.check_tensor_dtype_valid('boxlength_f_type', boxlength_f_type, [mstype.float32], self.name)
        validator.check_tensor_dtype_valid('a_14_type', a_14_type, [mstype.int32], self.name)
        validator.check_tensor_dtype_valid('b_14_type', b_14_type, [mstype.int32], self.name)
        validator.check_tensor_dtype_valid('lj_scale_factor_type', lj_scale_factor_type, [mstype.float32], self.name)
        validator.check_tensor_dtype_valid('LJ_type_A_type', LJ_type_A_type, [mstype.float32], self.name)
        validator.check_tensor_dtype_valid('LJ_type_B_type', LJ_type_B_type, [mstype.float32], self.name)

        return LJ_type_A_type


class Dihedral14LJForceWithDirectCF(PrimitiveWithInfer):
    """
    Dihedral14LJForceWithDirectCF:

    Calculate the Lennard-Jones part and the Coulomb part of force correction
    for each necessary dihedral 1,4 terms.

    The calculation formula of the Lennard-Jones part is the same as operator
    Dihedral14LJForce(), and the Coulomb part is as follows:

    .. math::

        dr = (x_a-x_b, y_a-y_b, z_a-z_b)
        F = -k*q_a*q_b/|r|^3*dr

    Inputs:
        - **cf_scale_factor** (Tensor, float) - [M,], the scale factor for the
        Coulomb part of force correction for each dihedral 1,4 terms.

        The rest of the inputs is the same as operator Dihedral14LJForce().

    Outputs:
        - **frc_f** (Tensor, float) - [N, 3], the force felt by each atom.

    Supported Platforms:
        ``GPU``
    Examples:
    """

    @prim_attr_register
    def __init__(self, nb14_numbers, atom_numbers):
        self.dihedral_14_numbers = nb14_numbers
        self.atom_numbers = atom_numbers

        self.init_prim_io_names(
            inputs=['uint_crd_f', 'LJtype', 'charge', 'boxlength_f', 'a_14', 'b_14', 'lj_scale_factor',
                    'cf_scale_factor',
                    'LJ_type_A', 'LJ_type_B'],
            outputs=['frc_f'])
        self.add_prim_attr('dihedral_14_numbers', self.dihedral_14_numbers)
        self.add_prim_attr('atom_numbers', self.atom_numbers)

    def infer_shape(self, uint_crd_f_shape, LJtype_shape, charge_shape, boxlength_f_shape, a_14_shape, b_14_shape,
                    lj_scale_factor_shape, cf_scale_factor_shape, LJ_type_A_shape, LJ_type_B_shape):
        return [self.atom_numbers, 3]

    def infer_dtype(self, uint_crd_f_dtype, LJtype_dtype, charge_dtype, boxlength_f_type, a_14_type, b_14_type,
                    lj_scale_factor_type, cf_scale_factor_type, LJ_type_A_type, LJ_type_B_type):
        validator.check_tensor_dtype_valid('uint_crd_f_dtype', uint_crd_f_dtype, [mstype.uint32], self.name)
        validator.check_tensor_dtype_valid('LJtype_dtype', LJtype_dtype, [mstype.int32], self.name)
        validator.check_tensor_dtype_valid('charge_dtype', charge_dtype, [mstype.float32], self.name)
        validator.check_tensor_dtype_valid('boxlength_f_type', boxlength_f_type, [mstype.float32], self.name)
        validator.check_tensor_dtype_valid('a_14_type', a_14_type, [mstype.int32], self.name)
        validator.check_tensor_dtype_valid('b_14_type', b_14_type, [mstype.int32], self.name)
        validator.check_tensor_dtype_valid('lj_scale_factor_type', lj_scale_factor_type, [mstype.float32], self.name)
        validator.check_tensor_dtype_valid('cf_scale_factor_type', cf_scale_factor_type, [mstype.float32], self.name)
        validator.check_tensor_dtype_valid('LJ_type_A_type', LJ_type_A_type, [mstype.float32], self.name)
        validator.check_tensor_dtype_valid('LJ_type_B_type', LJ_type_B_type, [mstype.float32], self.name)

        return LJ_type_A_type


class Dihedral14LJCFForceWithAtomEnergy(PrimitiveWithInfer):
    """
    Dihedral14LJCFForceWithAtomEnergy:

    Calculate the Lennard-Jones and Coulumb energy correction and force correction
    for each necessary dihedral 1,4 terms together and add them to the total force
    and potential energy for each atom.

    The calculation formula of force correction is the same as operator
    Dihedral14LJForceWithDirectCF(), and the energy correction part is the same
    as operator Dihedral14LJEnergy() and Dihedral14CFEnergy().

    Inputs:
        Same as operator Dihedral14LJForceWithdirectCF().

    Outputs:
        - **frc_f** (Tensor, float32) - [N, 3], the force felt by each atom.
        - **atom_energy** (Tensor, float32) - [N,], the accumulated potential
        energy for each atom.

    Supported Platforms:
        ``GPU``
    Examples:
    """


    @prim_attr_register
    def __init__(self, nb14_numbers, atom_numbers):
        self.dihedral_14_numbers = nb14_numbers
        self.atom_numbers = atom_numbers

        self.init_prim_io_names(
            inputs=['uint_crd_f', 'LJtype', 'charge', 'boxlength_f', 'a_14', 'b_14', 'lj_scale_factor',
                    'cf_scale_factor',
                    'LJ_type_A', 'LJ_type_B'],
            outputs=['frc_f', 'atom_energy'])
        self.add_prim_attr('dihedral_14_numbers', self.dihedral_14_numbers)
        self.add_prim_attr('atom_numbers', self.atom_numbers)

    def infer_shape(self, uint_crd_f_shape, LJtype_shape, charge_shape, boxlength_f_shape, a_14_shape, b_14_shape,
                    lj_scale_factor_shape, cf_scale_factor_shape, LJ_type_A_shape, LJ_type_B_shape):
        return uint_crd_f_shape, charge_shape

    def infer_dtype(self, uint_crd_f_dtype, LJtype_dtype, charge_dtype, boxlength_f_type, a_14_type, b_14_type,
                    lj_scale_factor_type, cf_scale_factor_type, LJ_type_A_type, LJ_type_B_type):
        validator.check_tensor_dtype_valid('uint_crd_f_dtype', uint_crd_f_dtype, [mstype.uint32], self.name)
        validator.check_tensor_dtype_valid('LJtype_dtype', LJtype_dtype, [mstype.int32], self.name)
        validator.check_tensor_dtype_valid('charge_dtype', charge_dtype, [mstype.float32], self.name)
        validator.check_tensor_dtype_valid('boxlength_f_type', boxlength_f_type, [mstype.float32], self.name)
        validator.check_tensor_dtype_valid('a_14_type', a_14_type, [mstype.int32], self.name)
        validator.check_tensor_dtype_valid('b_14_type', b_14_type, [mstype.int32], self.name)
        validator.check_tensor_dtype_valid('lj_scale_factor_type', lj_scale_factor_type, [mstype.float32], self.name)
        validator.check_tensor_dtype_valid('cf_scale_factor_type', cf_scale_factor_type, [mstype.float32], self.name)
        validator.check_tensor_dtype_valid('LJ_type_A_type', LJ_type_A_type, [mstype.float32], self.name)
        validator.check_tensor_dtype_valid('LJ_type_B_type', LJ_type_B_type, [mstype.float32], self.name)

        return charge_dtype, charge_dtype


class Dihedral14LJAtomEnergy(PrimitiveWithInfer):
    """
    Dihedral14LJAtomEnergy:

    Add the potenrial energy caused by Lennard-Jones energy correction for each
    necessary dihedral 1,4 terms to the total potential energy of each atom.

    The calculation formula is the same as operator Dihedral14LJEnergy().

    Inputs:
        Same as operator Dihedral14LJForce().

    Outputs:
        - **ene** (Tensor, float32) - [N,], the accumulated potential energy of
        each atom.

    Supported Platforms:
        ``GPU``
    Examples:
    """


    @prim_attr_register
    def __init__(self, nb14_numbers, atom_numbers):
        self.dihedral_14_numbers = nb14_numbers
        self.atom_numbers = atom_numbers

        self.init_prim_io_names(
            inputs=['uint_crd_f', 'LJtype', 'charge', 'boxlength_f', 'a_14', 'b_14', 'lj_scale_factor',
                    'LJ_type_A', 'LJ_type_B'],
            outputs=['ene'])
        self.add_prim_attr('dihedral_14_numbers', self.dihedral_14_numbers)
        self.add_prim_attr('atom_numbers', self.atom_numbers)

    def infer_shape(self, uint_crd_f_shape, LJtype_shape, charge_shape, boxlength_f_shape, a_14_shape, b_14_shape,
                    lj_scale_factor_shape, LJ_type_A_shape, LJ_type_B_shape):
        return LJtype_shape

    def infer_dtype(self, uint_crd_f_dtype, LJtype_dtype, charge_dtype, boxlength_f_type, a_14_type, b_14_type,
                    lj_scale_factor_type, LJ_type_A_type, LJ_type_B_type):
        validator.check_tensor_dtype_valid('uint_crd_f_dtype', uint_crd_f_dtype, [mstype.uint32], self.name)
        validator.check_tensor_dtype_valid('LJtype_dtype', LJtype_dtype, [mstype.int32], self.name)
        validator.check_tensor_dtype_valid('charge_dtype', charge_dtype, [mstype.float32], self.name)
        validator.check_tensor_dtype_valid('boxlength_f_type', boxlength_f_type, [mstype.float32], self.name)
        validator.check_tensor_dtype_valid('a_14_type', a_14_type, [mstype.int32], self.name)
        validator.check_tensor_dtype_valid('b_14_type', b_14_type, [mstype.int32], self.name)
        validator.check_tensor_dtype_valid('lj_scale_factor_type', lj_scale_factor_type, [mstype.float32],
                                           self.name)
        validator.check_tensor_dtype_valid('LJ_type_A_type', LJ_type_A_type, [mstype.float32], self.name)
        validator.check_tensor_dtype_valid('LJ_type_B_type', LJ_type_B_type, [mstype.float32], self.name)

        return LJ_type_A_type


class Dihedral14CFEnergy(PrimitiveWithInfer):
    """
    Dihedral14CFEnergy:

    Calculate the Coulumb part of 1,4 dihedral energy correction for
    each necessary dihedral terms on the corresponding atoms.

    .. math::

        dr = (x_a-x_b, y_a-y_b, z_a-z_b)
        E = k*q_a*q_b/|dr|

    Inputs:
        The meaning and type of each input is the same as that of operator
        Dihedral14LJForceWithDirectCF().

    Outputs:
        - **ene** (Tensor, float32) - [M,], the accumulated potential energy
        of each atom.

    Supported Platforms:
        ``GPU``
    Examples:
    """

    @prim_attr_register
    def __init__(self, nb14_numbers, atom_numbers):
        self.dihedral_14_numbers = nb14_numbers
        self.atom_numbers = atom_numbers

        self.init_prim_io_names(
            inputs=['uint_crd_f', 'LJtype', 'charge', 'boxlength_f', 'a_14', 'b_14', 'cj_scale_factor'],
            outputs=['ene'])
        self.add_prim_attr('dihedral_14_numbers', self.dihedral_14_numbers)
        self.add_prim_attr('atom_numbers', self.atom_numbers)

    def infer_shape(self, uint_crd_f_shape, LJtype_shape, charge_shape, boxlength_f_shape, a_14_shape, b_14_shape,
                    cf_scale_factor_shape):
        return [self.dihedral_14_numbers,]

    def infer_dtype(self, uint_crd_f_dtype, LJtype_dtype, charge_dtype, boxlength_f_type, a_14_type, b_14_type,
                    cf_scale_factor_type):
        validator.check_tensor_dtype_valid('uint_crd_f_dtype', uint_crd_f_dtype, [mstype.uint32], self.name)
        validator.check_tensor_dtype_valid('LJtype_dtype', LJtype_dtype, [mstype.int32], self.name)
        validator.check_tensor_dtype_valid('charge_dtype', charge_dtype, [mstype.float32], self.name)
        validator.check_tensor_dtype_valid('boxlength_f_type', boxlength_f_type, [mstype.float32], self.name)
        validator.check_tensor_dtype_valid('a_14_type', a_14_type, [mstype.int32], self.name)
        validator.check_tensor_dtype_valid('b_14_type', b_14_type, [mstype.int32], self.name)
        validator.check_tensor_dtype_valid('lj_scale_factor_type', cf_scale_factor_type, [mstype.float32],
                                           self.name)

        return charge_dtype


class Dihedral14CFAtomEnergy(PrimitiveWithInfer):
    """
    Dihedral14CFAtomEnergy:

    Add the potential energy caused by Coulumb energy correction for each
    necessary dihedral 1,4 terms to the total potential energy of each atom.

    The calculation formula is the same as operator Dihedral14CFEnergy().

    Inputs:
        The meaning and type of each input is the same as that of operator
        Dihedral14LJForceWithDirectCF().

    Outputs:
        - **ene** (Tensor, float32) - [N,], the accumulated potential energy
        of each atom.


    Supported Platforms:
        ``GPU``
    Examples:
    """


    @prim_attr_register
    def __init__(self, nb14_numbers, atom_numbers):
        self.dihedral_14_numbers = nb14_numbers
        self.atom_numbers = atom_numbers

        self.init_prim_io_names(
            inputs=['uint_crd_f', 'LJtype', 'charge', 'boxlength_f', 'a_14', 'b_14', 'cf_scale_factor'],
            outputs=['ene'])
        self.add_prim_attr('dihedral_14_numbers', self.dihedral_14_numbers)
        self.add_prim_attr('atom_numbers', self.atom_numbers)

    def infer_shape(self, uint_crd_f_shape, LJtype_shape, charge_shape, boxlength_f_shape, a_14_shape, b_14_shape,
                    cf_scale_factor_shape):
        return LJtype_shape

    def infer_dtype(self, uint_crd_f_dtype, LJtype_dtype, charge_dtype, boxlength_f_type, a_14_type, b_14_type,
                    cf_scale_factor_type):
        validator.check_tensor_dtype_valid('uint_crd_f_dtype', uint_crd_f_dtype, [mstype.uint32], self.name)
        validator.check_tensor_dtype_valid('LJtype_dtype', LJtype_dtype, [mstype.int32], self.name)
        validator.check_tensor_dtype_valid('charge_dtype', charge_dtype, [mstype.float32], self.name)
        validator.check_tensor_dtype_valid('boxlength_f_type', boxlength_f_type, [mstype.float32], self.name)
        validator.check_tensor_dtype_valid('a_14_type', a_14_type, [mstype.int32], self.name)
        validator.check_tensor_dtype_valid('b_14_type', b_14_type, [mstype.int32], self.name)
        validator.check_tensor_dtype_valid('cf_scale_factor_type', cf_scale_factor_type, [mstype.float32],
                                           self.name)

        return charge_dtype


class MDIterationLeapFrog(PrimitiveWithInfer):
    """
    MDIterationLeapFrog:

    One step of classical leap frog algorithm to solve the finite difference
    Hamiltonian equations of motion for certain system, using Langevin dynamics
    with Liu's thermostat scheme. Assume the number of atoms is N and the target
    control temperature is T.

    Detailed iteration formula can be found in this paper: A unified thermostat
    scheme for efficient configurational sampling for classical/quantum canonical
    ensembles via molecular dynamics. DOI: 10.1063/1.4991621.

    Inputs:
        - **float4_numbers** (int32) - total length to store random numbers.
        - **atom_numbers** (int32) - the number of atoms N.
        - **dt** (float32) - time step for finite difference.
        - **half_dt** (float32) - half of time step for finite difference.
        - **exp_gamma** (float32) - parameter in Liu's dynamic, equals
        exp(-gamma_ln * dt), where gamma_ln is the firction factor in Langvin
        dynamics.
        - **max_velocity** (float32) - the upper limit of velocity, when the
        veclocity overflows, scale it to the upper limit.
        - **is_max_velocity** (int32) - whether the max velocity control is
        open or not.

        - **mass_inverse** (Tensor, float32) - [N,], the inverse value of
        mass of each atom.
        - **sqrt_mass** (Tensor, float32) - [N,], the inverse square root value
        of effect mass in Liu's dynamics of each atom.

    Outputs:
        - **vel** (Tensor, float32) - [N, 3], the velocity of each atom.
        - **crd** (Tensor, float32) - [N, 3], the coordinate of each atom.
        - **frc** (Tensor, float32) - [N, 3], the force felt by each atom.
        - **acc** (Tensor, float32) - [N, 3], the acceleration of each atom.

    Supported Platforms:
        ``GPU``
    Examples:
    """

    @prim_attr_register
    def __init__(self, float4_numbers, atom_numbers, half_dt, dt, exp_gamma, is_max_velocity, max_velocity):
        self.float4_numbers = float4_numbers
        self.atom_numbers = atom_numbers
        self.half_dt = half_dt
        self.dt = dt
        self.exp_gamma = exp_gamma
        self.is_max_velocity = is_max_velocity
        self.max_velocity = max_velocity

        self.init_prim_io_names(
            inputs=['mass_inverse', 'sqrt_mass'],
            outputs=['vel', 'crd', 'frc', 'acc'])
        self.add_prim_attr('float4_numbers', self.float4_numbers)
        self.add_prim_attr('atom_numbers', self.atom_numbers)
        self.add_prim_attr('half_dt', self.half_dt)
        self.add_prim_attr('dt', self.dt)
        self.add_prim_attr('exp_gamma', self.exp_gamma)
        self.add_prim_attr('is_max_velocity', self.is_max_velocity)
        self.add_prim_attr('max_velocity', self.max_velocity)

    def infer_shape(self, mass_inverse_shape, sqrt_mass_shape):
        return [self.atom_numbers, 3], [self.atom_numbers, 3], [self.atom_numbers, 3], [self.atom_numbers, 3]

    def infer_dtype(self, mass_inverse_dtype, sqrt_mass_dtype):
        validator.check_tensor_dtype_valid('mass_inverse_dtype', mass_inverse_dtype, [mstype.float32], self.name)
        validator.check_tensor_dtype_valid('sqrt_mass_dtype', sqrt_mass_dtype, [mstype.float32], self.name)

        return mass_inverse_dtype, mass_inverse_dtype, mass_inverse_dtype, mass_inverse_dtype


class PMEReciprocalForce(PrimitiveWithInfer):
    """
    PMEReciprocalForce:

    Calculate the reciprocal part of long-range Coulumb force using
    PME(Particle Meshed Ewald) method. Assume the number of atoms is
    N.

    The detailed calculation formula of PME(Particle Meshed Ewald) method
    can be found in this paper: A Smooth Particle Mesh Ewald Method. DOI:
    10.1063/1.470117.

    Inputs:
        - **atom_numbers** (int32) - the number of atoms, N.
        - **beta** (float32) - the PME beta parameter, determined by the
        non-bond cutoff value and simulation precision tolerance.
        - **fftx** (int32) - the number of points for Fourier transform
        in dimension X.
        - **ffty** (int32) - the number of points for Fourier transform
        in dimension Y.
        - **fftz** (int32) - the number of points for Fourier transform
        in dimension Z.

        - **boxlength** (Tensor, float32) - [3,], the length of simulation
        box in 3 dimensions.
        - **uint_crd** (Tensor, uint32) - [N, 3], the unsigned int coordinates
        value of each atom.
        - **charge** (Tensor, float32) - [N,], the charge carried by each
        atom.

    Outputs:
        - **force** (Tensor, float32) - [N, 3], the force felt by each atom.

    Supported Platforms:
        ```GPU```

    Examples:
    """

    @prim_attr_register
    def __init__(self, atom_numbers, beta, fftx, ffty, fftz):
        self.atom_numbers = atom_numbers
        self.beta = beta
        self.fftx = fftx
        self.ffty = ffty
        self.fftz = fftz
        self.init_prim_io_names(inputs=['boxlength', 'uint_crd', 'charge'],
                                outputs=['force'])
        self.add_prim_attr('atom_numbers', self.atom_numbers)
        self.add_prim_attr('beta', self.beta)
        self.add_prim_attr('fftx', self.fftx)
        self.add_prim_attr('ffty', self.ffty)
        self.add_prim_attr('fftz', self.fftz)

    def infer_shape(self, boxlength_shape, uint_crd_shape, charge_shape):
        return uint_crd_shape

    def infer_dtype(self, boxlength_type, uint_crd_type, charge_type):
        validator.check_tensor_dtype_valid('boxlength_type', boxlength_type, [mstype.float32], self.name)
        validator.check_tensor_dtype_valid('uint_crd_type', uint_crd_type, [mstype.uint32], self.name)
        validator.check_tensor_dtype_valid('charge_type', charge_type, [mstype.float32], self.name)
        return charge_type


class PMEExcludedForce(PrimitiveWithInfer):
    """
    PMEExcludedForce:

    Calculate the excluded  part of long-range Coulumb force using
    PME(Particle Meshed Ewald) method. Assume the number of atoms is
    N, and the length of excluded list is E.

    Inputs:
        - **atom_numbers** (int32) - the number of atoms, N.
        - **beta** (float32) - the PME beta parameter, determined by the
        non-bond cutoff value and simulation precision tolerance.
        - **scaler** (Tensor, float32) - [3,], the scale factor between real space
        coordinates and its unsigned int value.
        - **excluded_list_start** (Tensor, int32) - [N,], the start excluded index
        in excluded list for each atom.
        - **excluded_numbers** (Tensor, int32) - [N,], the number of atom excluded
        in excluded list for each atom.
        - **excluded_list** (Tensor, int32) - [E,], the contiguous join of excluded
        list of each atom.

        The rest of the input is the same as that of operator PMEReciprocalForce().

    Outputs:
        - **force** (Tensor, float32) - [N, 3], the force felt by each atom.

    Supported Platforms:
        ```GPU```

    Examples:
    """

    @prim_attr_register
    def __init__(self, atom_numbers, beta):
        self.atom_numbers = atom_numbers
        self.beta = beta
        self.init_prim_io_names(
            inputs=['uint_crd', 'sacler', 'charge', 'excluded_list_start', 'excluded_list', 'excluded_atom_numbers'],
            outputs=['force'])
        self.add_prim_attr('atom_numbers', self.atom_numbers)
        self.add_prim_attr('beta', self.beta)

    def infer_shape(self, uint_crd_shape, sacler_shape, charge_shape, excluded_list_start_shape, excluded_list_shape,
                    excluded_atom_numbers_shape):
        return uint_crd_shape

    def infer_dtype(self, uint_crd_type, sacler_type, charge_type, excluded_list_start_type, excluded_list_type,
                    excluded_atom_numbers_type):
        validator.check_tensor_dtype_valid('sacler_type', sacler_type, [mstype.float32], self.name)
        validator.check_tensor_dtype_valid('uint_crd_type', uint_crd_type, [mstype.uint32], self.name)
        validator.check_tensor_dtype_valid('charge_type', charge_type, [mstype.float32], self.name)
        validator.check_tensor_dtype_valid('excluded_list_start_type', excluded_list_start_type, [mstype.int32],
                                           self.name)
        validator.check_tensor_dtype_valid('excluded_list_type', excluded_list_type, [mstype.int32],
                                           self.name)
        validator.check_tensor_dtype_valid('excluded_atom_numbers_type', excluded_atom_numbers_type, [mstype.int32],
                                           self.name)
        return charge_type


class PMEEnergy(PrimitiveWithInfer):
    """
    PMEEnergy:

    Calculate the Coulumb energy of the system using PME method.

    .. math::

        E = sum_{ij} q_iq_j/r_{ij}

    Inputs:
        Same as that of operator PMEReciprocalForce(), PMEExcludedForce()
        and PMEDirectAtomEnergy().

    Outputs:
        - **reciprocal_ene** (float32) - the reciprocal term of PME energy.
        - **self_ene** (float32) - the self term of PME energy.
        - **direct_ene** (float32) - the direct term of PME energy.
        - **correction_ene** (float32) - the correction term of PME energy.

    Supported Platforms:
        ```GPU``

    Examples:
    """

    @prim_attr_register
    def __init__(self, atom_numbers, beta, fftx, ffty, fftz):
        self.atom_numbers = atom_numbers
        self.beta = beta
        self.fftx = fftx
        self.ffty = ffty
        self.fftz = fftz
        self.init_prim_io_names(
            inputs=['box_length', 'uint_crd', 'charge', 'nl_numbers', 'nl_serial', 'scaler', 'excluded_list_start',
                    'excluded_list', 'excluded_atom_numbers'],
            outputs=['reciprocal_ene', 'self_ene', 'direct_ene', 'correction_ene'])
        self.add_prim_attr('atom_numbers', self.atom_numbers)
        self.add_prim_attr('beta', self.beta)
        self.add_prim_attr('fftx', self.fftx)
        self.add_prim_attr('ffty', self.ffty)
        self.add_prim_attr('fftz', self.fftz)

    def infer_shape(self, box_length, uint_crd, charge, nl_numbers, nl_serial, scaler, excluded_list_start,
                    excluded_list, excluded_atom_numbers):
        return (1,), (1,), (1,), (1,)

    def infer_dtype(self, box_length, uint_crd, charge, nl_numbers, nl_serial, scaler, excluded_list_start,
                    excluded_list, excluded_atom_numbers):
        validator.check_tensor_dtype_valid('box_length', box_length, [mstype.float32], self.name)
        validator.check_tensor_dtype_valid('uint_crd', uint_crd, [mstype.uint32], self.name)
        validator.check_tensor_dtype_valid('charge', charge, [mstype.float32], self.name)
        validator.check_tensor_dtype_valid('nl_numbers', nl_numbers, [mstype.int32], self.name)
        validator.check_tensor_dtype_valid('nl_serial', nl_serial, [mstype.int32], self.name)
        validator.check_tensor_dtype_valid('scaler', scaler, [mstype.float32], self.name)
        validator.check_tensor_dtype_valid('excluded_list_start', excluded_list_start, [mstype.int32],
                                           self.name)
        validator.check_tensor_dtype_valid('excluded_list', excluded_list, [mstype.int32],
                                           self.name)
        validator.check_tensor_dtype_valid('excluded_atom_numbers', excluded_atom_numbers, [mstype.int32],
                                           self.name)
        return charge, charge, charge, charge


class LJEnergy(PrimitiveWithInfer):
    """
    LJEnergy:

    Calculate the Van der Waals interaction energy described by Lennard-Jones
    potential for each atom. Assume the number of atoms is N, and the number
    of Lennard-Jones types for all atoms is P, which means there will be
    Q = P*(P+1)/2 types of possible Lennard-Jones interactions for all kinds
    of atom pairs.


    .. math::

        dr = (x_a-x_b, y_a-y_b, z_a-z_b)
        E = A/|dr|^{12} - B/|dr|^{6}

    Inputs:
        - **atom_numbers** (int32) - the number of atoms, N.
        - **cutoff_square** (float32) - the square value of cutoff.
        - **uint_crd** (Tensor, uint32) - [N, 3], the unsigned int coordinate
        value of each atom.
        - **LJtype** (Tensor, int32) - [N,], the Lennard-Jones type of each
        atom.
        - **charge** (Tensor, float32) - [N,], the charge carried by each
        atom.
        - **scaler** (Tensor, float32) - [3,], the scale factor between real
        space coordinate and its unsigned int value.
        - **nl_numbers** - (Tensor, int32) - [N,], the each atom.
        - **nl_serial** - (Tensor, int32) - [N, 800], the neighbor list of each atom,
        the max number is 800.
        - **d_LJ_A** (Tensor, float32) - [Q,], the Lennard-Jones A coefficient
        of each kind of atom pair.
        - **d_LJ_B** (Tensor, float32) - [Q,], the Lennard-Jones B coefficient
        of each kind of atom pair.

    Outputs:
        - **d_LJ_energy_atom** (Tensor, float32) - [N,], the Lennard-Jones
        potential energy of each atom.
        - **d_LJ_energy_sum** (float32), the sum of Lennard-Jones potential
        energy of each atom.

    Supported Platforms:
        ```GPU```

    Examples:
    """

    @prim_attr_register
    def __init__(self, atom_numbers, cutoff_square):
        self.atom_numbers = atom_numbers
        self.cutoff_square = cutoff_square
        self.init_prim_io_names(
            inputs=['uint_crd', 'LJtype', 'charge', 'scaler', 'nl_numbers', 'nl_serial', 'd_LJ_A', 'd_LJ_B'],
            outputs=['d_LJ_energy_atom'])
        self.add_prim_attr('atom_numbers', self.atom_numbers)
        self.add_prim_attr('cutoff_square', self.cutoff_square)

    def infer_shape(self, uint_crd, LJtype, charge, scaler, nl_numbers, nl_serial, d_LJ_A, d_LJ_B):
        return charge

    def infer_dtype(self, uint_crd, LJtype, charge, scaler, nl_numbers, nl_serial, d_LJ_A, d_LJ_B):
        validator.check_tensor_dtype_valid('uint_crd', uint_crd, [mstype.uint32], self.name)
        validator.check_tensor_dtype_valid('LJtype', LJtype, [mstype.int32], self.name)
        validator.check_tensor_dtype_valid('charge', charge, [mstype.float32], self.name)
        validator.check_tensor_dtype_valid('scaler', scaler, [mstype.float32], self.name)
        validator.check_tensor_dtype_valid('nl_numbers', nl_numbers, [mstype.int32], self.name)
        validator.check_tensor_dtype_valid('nl_serial', nl_serial, [mstype.int32], self.name)
        validator.check_tensor_dtype_valid('d_LJ_A', d_LJ_A, [mstype.float32], self.name)
        validator.check_tensor_dtype_valid('d_LJ_B', d_LJ_B, [mstype.float32], self.name)
        return charge


class LJForce(PrimitiveWithInfer):
    """
    LJForce:

    Calculate the Van der Waals interaction force described by Lennard-Jones
    potential energy for each atom.

    .. math::

        dr = (x_a-x_b, y_a-y_b, z_a-z_b)
        F = (-12*A/|dr|^{14} + 6*B/|dr|^{8}) * dr

    Inputs:
        Same as operator LJEnergy().

    outputs:
        - **frc** (Tensor, float32) - [N, 3], the force felt by each atom.

    Supported Platforms:
        ```GPU```
    Examples:
    """

    @prim_attr_register
    def __init__(self, atom_numbers, cutoff_square):
        self.atom_numbers = atom_numbers
        self.cutoff_square = cutoff_square
        self.init_prim_io_names(
            inputs=['uint_crd', 'LJtype', 'charge', 'scaler', 'nl_numbers', 'nl_serial', 'd_LJ_A', 'd_LJ_B'],
            outputs=['frc'])
        self.add_prim_attr('atom_numbers', self.atom_numbers)
        self.add_prim_attr('cutoff_square', self.cutoff_square)

    def infer_shape(self, uint_crd, LJtype, charge, scaler, nl_numbers, nl_serial, d_LJ_A, d_LJ_B):
        return uint_crd

    def infer_dtype(self, uint_crd, LJtype, charge, scaler, nl_numbers, nl_serial, d_LJ_A, d_LJ_B):
        validator.check_tensor_dtype_valid('uint_crd', uint_crd, [mstype.uint32], self.name)
        validator.check_tensor_dtype_valid('LJtype', LJtype, [mstype.int32], self.name)
        validator.check_tensor_dtype_valid('charge', charge, [mstype.float32], self.name)
        validator.check_tensor_dtype_valid('scaler', scaler, [mstype.float32], self.name)
        validator.check_tensor_dtype_valid('nl_numbers', nl_numbers, [mstype.int32], self.name)
        validator.check_tensor_dtype_valid('nl_serial', nl_serial, [mstype.int32], self.name)
        validator.check_tensor_dtype_valid('d_LJ_A', d_LJ_A, [mstype.float32], self.name)
        validator.check_tensor_dtype_valid('d_LJ_B', d_LJ_B, [mstype.float32], self.name)
        return charge


class LJForceWithPMEDirectForce(PrimitiveWithInfer):
    """
    LJForceWithPMEDirectForce:

    Calculate the Lennard-Jones force and PME direct force together.

    The calculation formula of Lennard-Jones part is the same as operator
    LJForce(), and the PME direct part is within PME method.

    Inputs:
        - **pme_beta** (float32), PME beta parameter, same as operator
        PMEReciprocalForce().

        the rest of the input is the same as operator LJForce().

    Outputs:
        - **frc** (Tensor, float32), [N, 3], the force felt by each atom.

    Supported Platforms:
        ```GPU```

    Examples:
    """

    @prim_attr_register
    def __init__(self, atom_numbers, cutoff, pme_beta):
        self.atom_numbers = atom_numbers
        self.cutoff = cutoff
        self.pme_beta = pme_beta
        self.init_prim_io_names(
            inputs=['uint_crd', 'LJtype', 'charge', 'scaler', 'nl_numbers', 'nl_serial', 'd_LJ_A', 'd_LJ_B'],
            outputs=['frc'])
        self.add_prim_attr('atom_numbers', self.atom_numbers)
        self.add_prim_attr('cutoff', self.cutoff)
        self.add_prim_attr('pme_beta', self.pme_beta)

    def infer_shape(self, uint_crd, LJtype, charge, scaler, nl_numbers, nl_serial, d_LJ_A, d_LJ_B):
        return uint_crd

    def infer_dtype(self, uint_crd, LJtype, charge, scaler, nl_numbers, nl_serial, d_LJ_A, d_LJ_B):
        validator.check_tensor_dtype_valid('uint_crd', uint_crd, [mstype.uint32], self.name)
        validator.check_tensor_dtype_valid('LJtype', LJtype, [mstype.int32], self.name)
        validator.check_tensor_dtype_valid('charge', charge, [mstype.float32], self.name)
        validator.check_tensor_dtype_valid('scaler', scaler, [mstype.float32], self.name)
        validator.check_tensor_dtype_valid('nl_numbers', nl_numbers, [mstype.int32], self.name)
        validator.check_tensor_dtype_valid('nl_serial', nl_serial, [mstype.int32], self.name)
        validator.check_tensor_dtype_valid('d_LJ_A', d_LJ_A, [mstype.float32], self.name)
        validator.check_tensor_dtype_valid('d_LJ_B', d_LJ_B, [mstype.float32], self.name)
        return charge


class GetCenterOfGeometry(PrimitiveWithInfer):
    """
    GetCenterOfGeometry:

    Supported Platforms:
        ``GPU``
    Examples:
    """

    @prim_attr_register
    def __init__(self, center_numbers, center_numbers_inverse):
        self.center_numbers = center_numbers
        self.center_numbers_inverse = center_numbers_inverse
        self.add_prim_attr('center_numbers', self.center_numbers)
        self.add_prim_attr('center_numbers_inverse', self.center_numbers_inverse)
        self.init_prim_io_names(
            inputs=['center_atoms', 'crd_f'],
            outputs=['center_of_geometry_f'])

    def infer_shape(self, center_atoms_shape, crd_f_shape):
        cls_name = self.name
        N = self.center_numbers
        validator.check_int(center_atoms_shape[0], N, Rel.EQ, "center_atoms_shape", cls_name)
        validator.check_int(crd_f_shape[0], N, Rel.EQ, "crd_f_shape", cls_name)
        validator.check_int(crd_f_shape[1], 3, Rel.EQ, "crd_f_shape", cls_name)
        return [3,]

    def infer_dtype(self, center_atoms_dtype, crd_f_dtype):
        validator.check_tensor_dtype_valid('center_atoms_dtype', center_atoms_dtype, [mstype.int32], self.name)
        validator.check_tensor_dtype_valid('crd_f_dtype', crd_f_dtype, [mstype.float32], self.name)

        return crd_f_dtype


class MDTemperature(PrimitiveWithInfer):
    """
    MDTemperature:

    Supported Platforms:
        ``GPU``
    Examples:
    """

    @prim_attr_register
    def __init__(self, residue_numbers):
        self.residue_numbers = residue_numbers
        self.add_prim_attr('residue_numbers', self.residue_numbers)
        self.init_prim_io_names(
            inputs=['start', 'end', 'atom_vel_f', 'atom_mass'],
            outputs=['ek'])

    def infer_shape(self, start_shape, end_shape, atom_vel_f_shape, atom_mass_shape):
        cls_name = self.name
        N = self.residue_numbers
        validator.check_int(start_shape[0], N, Rel.EQ, "start_shape", cls_name)
        validator.check_int(end_shape[0], N, Rel.EQ, "end_shape", cls_name)
        validator.check_int(atom_vel_f_shape[0], N, Rel.EQ, "atom_vel_f_shape", cls_name)
        validator.check_int(atom_vel_f_shape[1], 3, Rel.EQ, "atom_vel_f_shape", cls_name)
        validator.check_int(atom_mass_shape[0], N, Rel.EQ, "atom_mass_shape", cls_name)
        return [N,]

    def infer_dtype(self, start_dtype, end_dtype, atom_vel_f_dtype, atom_mass_dtype):
        validator.check_tensor_dtype_valid('start_dtype', start_dtype, [mstype.int32], self.name)
        validator.check_tensor_dtype_valid('end_dtype', end_dtype, [mstype.int32], self.name)
        validator.check_tensor_dtype_valid('atom_vel_f_dtype', atom_vel_f_dtype, [mstype.float32], self.name)
        validator.check_tensor_dtype_valid('atom_mass_dtype', atom_mass_dtype, [mstype.float32], self.name)
        return atom_mass_dtype


class NeighborListUpdate(PrimitiveWithInfer):
    """
    NeighborListUpdate

    Update (or construct if first time) the Verlet neighbor list for the
    calculation of short-ranged force. Assume the number of atoms is N,
    the number of grids divided is G, the maximum number of atoms in one
    grid is M, the maximum number of atoms in single atom's neighbor list
    is L, and the number of total atom in excluded list is E.

    Inputs:
        - **grid_numbers** (int32) - the total number of grids divided.
        - **refresh_count** (int32) - the counter which counts how many
        iteration steps have passed since last update.
        - **not_first_time** (int32) - whether to construct the neighbor
        list first time or not.
        - **Nxy** (int32) - the total number of grids divided in xy plane.
        - **excluded_atom_numbers** (int32) - the total atom numbers in
        the excluded list.
        - **cutoff** (float32) - the cutoff distance for short-range force
        calculation.
        - **skin** (float32) - the overflow value of cutoff to maintain a
        neighbor list.
        - **cutoff_square** (float32) - the suqare value of cutoff.
        - **half_skin_square** (float32) - skin*skin/4, indicates the maximum
        square value of the distance atom allowed to move between two updates.
        - **cutoff_with_skin** (float32) - cutoff + skin, indicates the
        radius of the neighbor list for each atom.
        - **half_cutoff_with_skin** (float32) - cutoff_with_skin/2.
        - **cutoff_with_skin_square** (float32) - the square value of
        cutoff_with_skin.
        - **refresh_interval** (int32) - the number of iteration steps
        between two updates of neighbor list.
        - **max_atom_in_grid_numbers** (int32) - the maximum number of atoms
        in one grid.

        - **atom_numbers_in_grid_bucket** (Tensor, int32) - [G,], the number
        of atoms in each grid bucket.
        - **bucket** (Tensor, int32) - (Tensor,int32) - [G, M], the atom
        indices in each grid bucket.
        - **crd** (Tensor, float32) - [N,], the coordinates of each atom.
        - **box_length** (Tensor, float32) - [3,], the length of 3 dimensions
        of the simulation box.
        - **grid_N** (Tensor, int32) - [3,], the number of grids divided of
        3 dimensions of the simulation box.
        - **grid_length_inverse** (float32) - the inverse value of grid length.
        - **atom_in_grid_serial** (Tensor, int32) - [N,], the grid index for
        each atom.
        - **old_crd** (Tensor, float32) - [N, 3], the coordinates before update
        of each atom.
        - **crd_to_uint_crd_cof** (Tensor, float32) - [3,], the scale factor
        between the unsigned int value and the real space coordinates.
        - **uint_crd** (Tensor, uint32) - [N, 3], the unsigned int coordinates
        value fo each atom.
        - **gpointer** (Tensor, int32) - [G, 125], the 125 nearest neighbor grids
        (including self) of each grid.
        - **nl_atom_numbers** (Tensor, int32) - [N,], the number of atoms in
        neighbor list of each atom.
        - **nl_atom_serial** (Tensor, int32) - [N, L], the indices of atoms in
        neighbor list of each atom.
        - **uint_dr_to_dr_cof** (Tensor, float32) - [3,], the scale factor between
        the real space coordinates and the unsigned int value.
        - **excluded_list_start** (Tensor, int32) - [N,], the start excluded
        index in excluded list for each atom.
        - **excluded_numbers** (Tensor, int32) - [N,], the number of atom excluded
        in excluded list for each atom.
        - **excluded_list** (Tensor, int32) - [E,], the contiguous join of excluded
        list of each atom.
        - **need_refresh_flag** (Tensor, int32) - [N,], whether the neighbor list
        of each atom need update or not.

    Outputs:
        - **res** (float32)

    Supported Platforms:
        ```GPU```

    Examples:
    """

    @prim_attr_register
    def __init__(self, grid_numbers, atom_numbers, refresh_count, not_first_time, Nxy, excluded_atom_numbers,
                 cutoff_square, half_skin_square, cutoff_with_skin, half_cutoff_with_skin, cutoff_with_skin_square,
                 refresh_interval=20, cutoff=10.0, skin=2.0, max_atom_in_grid_numbers=64, max_neighbor_numbers=800):
        self.grid_numbers = grid_numbers
        self.atom_numbers = atom_numbers
        self.refresh_count = refresh_count
        self.refresh_interval = refresh_interval
        self.not_first_time = not_first_time
        self.cutoff = cutoff
        self.skin = skin
        self.max_atom_in_grid_numbers = max_atom_in_grid_numbers
        self.Nxy = Nxy
        self.excluded_atom_numbers = excluded_atom_numbers
        self.cutoff_square = cutoff_square
        self.half_skin_square = half_skin_square
        self.cutoff_with_skin = cutoff_with_skin
        self.half_cutoff_with_skin = half_cutoff_with_skin
        self.cutoff_with_skin_square = cutoff_with_skin_square
        self.max_neighbor_numbers = max_neighbor_numbers
        self.init_prim_io_names(
            inputs=['atom_numbers_in_grid_bucket', 'bucket', 'crd', 'box_length', 'grid_N', 'grid_length_inverse',
                    'atom_in_grid_serial', 'old_crd', 'crd_to_uint_crd_cof', 'uint_crd', 'gpointer', 'nl_atom_numbers',
                    'nl_atom_serial', 'uint_dr_to_dr_cof', 'excluded_list_start', 'excluded_list', 'excluded_numbers',
                    'need_refresh_flag'], outputs=['res'])

        self.add_prim_attr('grid_numbers', self.grid_numbers)
        self.add_prim_attr('atom_numbers', self.atom_numbers)
        self.add_prim_attr('refresh_count', self.refresh_count)
        self.add_prim_attr('refresh_interval', self.refresh_interval)
        self.add_prim_attr('not_first_time', self.not_first_time)
        self.add_prim_attr('cutoff', self.cutoff)
        self.add_prim_attr('skin', self.skin)
        self.add_prim_attr('max_atom_in_grid_numbers', self.max_atom_in_grid_numbers)
        self.add_prim_attr('Nxy', self.Nxy)
        self.add_prim_attr('excluded_atom_numbers', self.excluded_atom_numbers)
        self.add_prim_attr('cutoff_square', self.cutoff_square)
        self.add_prim_attr('half_skin_square', self.half_skin_square)
        self.add_prim_attr('cutoff_with_skin', self.cutoff_with_skin)
        self.add_prim_attr('half_cutoff_with_skin', self.half_cutoff_with_skin)
        self.add_prim_attr('cutoff_with_skin_square', self.cutoff_with_skin_square)

    def infer_shape(self, atom_numbers_in_grid_bucket_shape, bucket_shape, crd_shape, box_length_shape, grid_N_shape,
                    grid_length_inverse_shape, atom_in_grid_serial_shape, old_crd_shape, crd_to_uint_crd_cof_shape,
                    uint_crd_shape, gpointer_shape, nl_atom_numbers_shape, nl_atom_serial_shape,
                    uint_dr_to_dr_cof_shape, excluded_list_start_shape, excluded_list_shape, excluded_numbers_shape,
                    need_refresh_flag_shape):
        assert len(atom_numbers_in_grid_bucket_shape) == 1
        assert len(bucket_shape) == 2
        assert len(crd_shape) == 2
        assert len(box_length_shape) == 1
        assert len(grid_N_shape) == 1
        assert len(grid_length_inverse_shape) == 1
        assert len(atom_in_grid_serial_shape) == 1
        assert len(old_crd_shape) == 2
        assert len(crd_to_uint_crd_cof_shape) == 1
        assert len(uint_crd_shape) == 2
        assert len(gpointer_shape) == 2
        assert len(nl_atom_numbers_shape) == 1
        assert len(nl_atom_serial_shape) == 2
        assert len(uint_dr_to_dr_cof_shape) == 1
        assert len(excluded_list_start_shape) == 1
        assert len(excluded_list_shape) == 1
        assert len(excluded_numbers_shape) == 1
        assert len(need_refresh_flag_shape) == 1

        validator.check_int(atom_numbers_in_grid_bucket_shape[0], self.grid_numbers, Rel.EQ,
                            "atom_numbers_in_grid_bucket_shape", self.name)
        validator.check_int(bucket_shape[0], self.grid_numbers, Rel.EQ, "bucket_shape", self.name)
        validator.check_int(bucket_shape[1], self.max_atom_in_grid_numbers, Rel.EQ, "bucket_shape", self.name)
        validator.check_int(crd_shape[0], self.atom_numbers, Rel.EQ, "crd_shape", self.name)
        validator.check_int(crd_shape[1], 3, Rel.EQ, "crd_shape", self.name)
        validator.check_int(box_length_shape[0], 3, Rel.EQ, "box_length_shape", self.name)
        validator.check_int(grid_N_shape[0], 3, Rel.EQ, "grid_N_shape", self.name)
        validator.check_int(grid_length_inverse_shape[0], 3, Rel.EQ, "grid_length_inverse_shape", self.name)
        validator.check_int(atom_in_grid_serial_shape[0], self.atom_numbers, Rel.EQ, "atom_in_grid_serial_shape",
                            self.name)
        validator.check_int(old_crd_shape[0], self.atom_numbers, Rel.EQ, "old_crd_shape", self.name)
        validator.check_int(old_crd_shape[1], 3, Rel.EQ, "old_crd_shape", self.name)
        validator.check_int(crd_to_uint_crd_cof_shape[0], 3, Rel.EQ, "crd_to_uint_crd_cof_shape", self.name)
        validator.check_int(uint_crd_shape[0], self.atom_numbers, Rel.EQ, "uint_crd_shape", self.name)
        validator.check_int(uint_crd_shape[1], 3, Rel.EQ, "uint_crd_shape", self.name)
        validator.check_int(gpointer_shape[0], self.grid_numbers, Rel.EQ, "gpointer_shape", self.name)
        validator.check_int(gpointer_shape[1], 125, Rel.EQ, "gpointer_shape", self.name)
        validator.check_int(nl_atom_numbers_shape[0], self.atom_numbers, Rel.EQ, "nl_atom_numbers_shape", self.name)
        validator.check_int(nl_atom_serial_shape[0], self.atom_numbers, Rel.EQ, "nl_atom_serial_shape", self.name)
        validator.check_int(nl_atom_serial_shape[1], self.max_neighbor_numbers, Rel.EQ, "nl_atom_serial_shape",
                            self.name)
        validator.check_int(uint_dr_to_dr_cof_shape[0], 3, Rel.EQ, "uint_dr_to_dr_cof_shape", self.name)
        validator.check_int(excluded_list_start_shape[0], self.atom_numbers, Rel.EQ, "excluded_list_start_shape",
                            self.name)
        validator.check_int(excluded_list_shape[0], self.excluded_atom_numbers, Rel.EQ, "excluded_list_shape",
                            self.name)
        validator.check_int(excluded_numbers_shape[0], self.atom_numbers, Rel.EQ, "excluded_numbers_shape", self.name)
        validator.check_int(need_refresh_flag_shape[0], 1, Rel.EQ, "need_refresh_flag_shape", self.name)

        return [1,]

    def infer_dtype(self, atom_numbers_in_grid_bucket_dtype, bucket_dtype, crd_dtype, box_length_dtype, grid_N_dtype,
                    grid_length_inverse_dtype, atom_in_grid_serial_dtype, old_crd_dtype, crd_to_uint_crd_cof_dtype,
                    uint_crd_dtype, gpointer_dtype, nl_atom_numbers_dtype, nl_atom_serial_dtype,
                    uint_dr_to_dr_cof_dtype, excluded_list_start_dtype, excluded_list_dtype, excluded_numbers_dtype,
                    need_refresh_flag_dtype):
        validator.check_tensor_dtype_valid('atom_numbers_in_grid_bucket_dtype', atom_numbers_in_grid_bucket_dtype,
                                           [mstype.int32], self.name)
        validator.check_tensor_dtype_valid('bucket_dtype', bucket_dtype, [mstype.int32], self.name)
        validator.check_tensor_dtype_valid('crd_dtype', crd_dtype, [mstype.float32], self.name)
        validator.check_tensor_dtype_valid('box_length_dtype', box_length_dtype, [mstype.float32], self.name)
        validator.check_tensor_dtype_valid('grid_N_dtype', grid_N_dtype, [mstype.int32], self.name)
        validator.check_tensor_dtype_valid('grid_length_inverse_dtype', grid_length_inverse_dtype, [mstype.float32],
                                           self.name)
        validator.check_tensor_dtype_valid('atom_in_grid_serial_dtype', atom_in_grid_serial_dtype, [mstype.int32],
                                           self.name)
        validator.check_tensor_dtype_valid('old_crd_dtype', old_crd_dtype, [mstype.float32], self.name)
        validator.check_tensor_dtype_valid('crd_to_uint_crd_cof_dtype', crd_to_uint_crd_cof_dtype, [mstype.float32],
                                           self.name)
        validator.check_tensor_dtype_valid('uint_crd_dtype', uint_crd_dtype, [mstype.uint32], self.name)
        validator.check_tensor_dtype_valid('gpointer_dtype', gpointer_dtype, [mstype.int32], self.name)
        validator.check_tensor_dtype_valid('nl_atom_numbers_dtype', nl_atom_numbers_dtype, [mstype.int32], self.name)
        validator.check_tensor_dtype_valid('nl_atom_serial_dtype', nl_atom_serial_dtype, [mstype.int32], self.name)
        validator.check_tensor_dtype_valid('uint_dr_to_dr_cof_dtype', uint_dr_to_dr_cof_dtype, [mstype.float32],
                                           self.name)
        validator.check_tensor_dtype_valid('excluded_list_start_dtype', excluded_list_start_dtype, [mstype.int32],
                                           self.name)
        validator.check_tensor_dtype_valid('excluded_list_dtype', excluded_list_dtype, [mstype.int32], self.name)
        validator.check_tensor_dtype_valid('excluded_numbers_dtype', excluded_numbers_dtype, [mstype.int32], self.name)
        validator.check_tensor_dtype_valid('need_refresh_flag_dtype', need_refresh_flag_dtype, [mstype.int32],
                                           self.name)

        return mstype.float32
