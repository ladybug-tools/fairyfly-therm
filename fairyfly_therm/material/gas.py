# coding=utf-8
"""Gas materials representing gaps within window constructions.

They can only exist within window constructions bounded by glazing materials
(they cannot be in the interior or exterior layer).
"""
from __future__ import division

from fairyfly._lockable import lockable
from fairyfly.typing import float_positive, float_in_range

from ._base import _ThermMaterialBase


@lockable
class PureGas(_ThermMaterialBase):
    """Custom gas gap layer.

    This object allows you to specify specific values for conductivity,
    viscosity and specific heat through the following formula:

    property = A + (B * T) + (C * T ** 2)

    where:

    * A, B, and C = regression coefficients for the gas
    * T = temperature [K]

    Note that setting properties B and C to 0 will mean the property will be
    equal to the A coefficient.

    Args:
        conductivity_coeff_a: First conductivity coefficient.
            Or conductivity in [W/m-K] if b and c coefficients are 0.
        viscosity_coeff_a: First viscosity coefficient.
            Or viscosity in [kg/m-s] if b and c coefficients are 0.
        specific_heat_coeff_a: First specific heat coefficient.
            Or specific heat in [J/kg-K] if b and c coefficients are 0.
        conductivity_coeff_b: Second conductivity coefficient. Default = 0.
        viscosity_coeff_b: Second viscosity coefficient. Default = 0.
        specific_heat_coeff_b: Second specific heat coefficient. Default = 0.
        conductivity_coeff_c: Third conductivity coefficient. Default = 0.
        viscosity_coeff_c: Third viscosity coefficient. Default = 0.
        specific_heat_coeff_c: Third specific heat coefficient. Default = 0.
        specific_heat_ratio: A number for the the ratio of the specific heat at
            constant pressure, to the specific heat at constant volume.
            Default is 1.0 for Air.
        molecular_weight: Number between 20 and 200 for the mass of 1 mol of
            the substance in grams. Default is 20.0.
        identifier: Text string for a unique object ID. Must be a UUID in the
            format xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx. If None, a UUID will
            automatically be generated. (Default: None).

    Properties:
        * identifier
        * display_name
        * conductivity_coeff_a
        * viscosity_coeff_a
        * specific_heat_coeff_a
        * conductivity_coeff_b
        * viscosity_coeff_b
        * specific_heat_coeff_b
        * conductivity_coeff_c
        * viscosity_coeff_c
        * specific_heat_coeff_c
        * specific_heat_ratio
        * molecular_weight
        * color
        * protected
        * user_data

    Usage:

    .. code-block:: python

        co2_mat = PureGas(0.0146, 0.000014, 827.73)
        co2_mat.display_name = 'CO2'
        co2_gap.specific_heat_ratio = 1.4
        co2_gap.molecular_weight = 44
        print(co2_gap)
    """
    __slots__ = ('_conductivity_coeff_a', '_viscosity_coeff_a', '_specific_heat_coeff_a',
                 '_conductivity_coeff_b', '_viscosity_coeff_b', '_specific_heat_coeff_b',
                 '_conductivity_coeff_c', '_viscosity_coeff_c', '_specific_heat_coeff_c',
                 '_specific_heat_ratio', '_molecular_weight')

    def __init__(self, identifier, thickness,
                 conductivity_coeff_a, viscosity_coeff_a, specific_heat_coeff_a,
                 conductivity_coeff_b=0, viscosity_coeff_b=0, specific_heat_coeff_b=0,
                 conductivity_coeff_c=0, viscosity_coeff_c=0, specific_heat_coeff_c=0,
                 specific_heat_ratio=1.0, molecular_weight=20.0):
        """Initialize custom gas energy material."""
        _ThermMaterialBase.__init__(self, identifier)
        self.conductivity_coeff_a = conductivity_coeff_a
        self.viscosity_coeff_a = viscosity_coeff_a
        self.specific_heat_coeff_a = specific_heat_coeff_a
        self.conductivity_coeff_b = conductivity_coeff_b
        self.viscosity_coeff_b = viscosity_coeff_b
        self.specific_heat_coeff_b = specific_heat_coeff_b
        self.conductivity_coeff_c = conductivity_coeff_c
        self.viscosity_coeff_c = viscosity_coeff_c
        self.specific_heat_coeff_c = specific_heat_coeff_c
        self.specific_heat_ratio = specific_heat_ratio
        self.molecular_weight = molecular_weight

    @property
    def conductivity_coeff_a(self):
        """Get or set the first conductivity coefficient."""
        return self._conductivity_coeff_a

    @conductivity_coeff_a.setter
    def conductivity_coeff_a(self, coeff):
        self._conductivity_coeff_a = float(coeff)

    @property
    def viscosity_coeff_a(self):
        """Get or set the first viscosity coefficient."""
        return self._viscosity_coeff_a

    @viscosity_coeff_a.setter
    def viscosity_coeff_a(self, coeff):
        self._viscosity_coeff_a = float_positive(coeff)

    @property
    def specific_heat_coeff_a(self):
        """Get or set the first specific heat coefficient."""
        return self._specific_heat_coeff_a

    @specific_heat_coeff_a.setter
    def specific_heat_coeff_a(self, coeff):
        self._specific_heat_coeff_a = float_positive(coeff)

    @property
    def conductivity_coeff_b(self):
        """Get or set the second conductivity coefficient."""
        return self._conductivity_coeff_b

    @conductivity_coeff_b.setter
    def conductivity_coeff_b(self, coeff):
        self._conductivity_coeff_b = float(coeff)

    @property
    def viscosity_coeff_b(self):
        """Get or set the second viscosity coefficient."""
        return self._viscosity_coeff_b

    @viscosity_coeff_b.setter
    def viscosity_coeff_b(self, coeff):
        self._viscosity_coeff_b = float(coeff)

    @property
    def specific_heat_coeff_b(self):
        """Get or set the second specific heat coefficient."""
        return self._specific_heat_coeff_b

    @specific_heat_coeff_b.setter
    def specific_heat_coeff_b(self, coeff):
        self._specific_heat_coeff_b = float(coeff)

    @property
    def conductivity_coeff_c(self):
        """Get or set the third conductivity coefficient."""
        return self._conductivity_coeff_c

    @conductivity_coeff_c.setter
    def conductivity_coeff_c(self, coeff):
        self._conductivity_coeff_c = float(coeff)

    @property
    def viscosity_coeff_c(self):
        """Get or set the third viscosity coefficient."""
        return self._viscosity_coeff_c

    @viscosity_coeff_c.setter
    def viscosity_coeff_c(self, coeff):
        self._viscosity_coeff_c = float(coeff)

    @property
    def specific_heat_coeff_c(self):
        """Get or set the third specific heat coefficient."""
        return self._specific_heat_coeff_c

    @specific_heat_coeff_c.setter
    def specific_heat_coeff_c(self, coeff):
        self._specific_heat_coeff_c = float(coeff)

    @property
    def specific_heat_ratio(self):
        """Get or set the specific heat ratio."""
        return self._specific_heat_ratio

    @specific_heat_ratio.setter
    def specific_heat_ratio(self, number):
        number = float(number)
        assert 1 <= number, 'Input specific_heat_ratio ({}) must be > 1.'.format(number)
        self._specific_heat_ratio = number

    @property
    def molecular_weight(self):
        """Get or set the molecular weight."""
        return self._molecular_weight

    @molecular_weight.setter
    def molecular_weight(self, number):
        self._molecular_weight = float_in_range(
            number, 20.0, 200.0, 'gas material molecular weight')

    def conductivity_at_temperature(self, t_kelvin):
        """Get the conductivity of the gas [W/m-K] at a given Kelvin temperature."""
        return self.conductivity_coeff_a + self.conductivity_coeff_b * t_kelvin + \
            self.conductivity_coeff_c * t_kelvin ** 2

    def viscosity_at_temperature(self, t_kelvin):
        """Get the viscosity of the gas [kg/m-s] at a given Kelvin temperature."""
        return self.viscosity_coeff_a + self.viscosity_coeff_b * t_kelvin + \
            self.viscosity_coeff_c * t_kelvin ** 2

    def specific_heat_at_temperature(self, t_kelvin):
        """Get the specific heat of the gas [J/kg-K] at a given Kelvin temperature."""
        return self.specific_heat_coeff_a + self.specific_heat_coeff_b * t_kelvin + \
            self.specific_heat_coeff_c * t_kelvin ** 2

    @classmethod
    def from_idf(cls, idf_string):
        """Create EnergyWindowMaterialGasCustom from an EnergyPlus text string.

        Args:
            idf_string: A text string fully describing an EnergyPlus material.
        """
        # check that the gas is, in fact custom
        ep_s = parse_idf_string(idf_string, 'WindowMaterial:Gas,')
        assert ep_s[1].title() == 'Custom', 'Exected Custom Gas. Got a specific one.'
        assert len(ep_s) == 14, 'Not enough fields present for Custom Gas ' \
            'IDF description. Expected 14 properties. Got {}.'.format(len(ep_s))
        ep_s.pop(1)
        # reorder the coefficients
        start = [ep_s[0], ep_s[1]]
        a_coef = [ep_s[2], ep_s[5], ep_s[8]]
        b_coef = [ep_s[3], ep_s[6], ep_s[9]]
        c_coef = [ep_s[4], ep_s[7], ep_s[10]]
        end = [ep_s[12], ep_s[11]]
        eps_cl = start + a_coef + b_coef + c_coef + end
        # assume that any blank strings are just coefficients of 0
        for i, val in enumerate(eps_cl[2:11]):
            clean_val = val if val != '' else 0
            eps_cl[i + 2] = clean_val
        return cls(*eps_cl)

    @classmethod
    def from_dict(cls, data):
        """Create a EnergyWindowMaterialGasCustom from a dictionary.

        Args:
            data: A python dictionary in the following format

        .. code-block:: python

            {
            "type": 'EnergyWindowMaterialGasCustom',
            "identifier": 'CO2_0010_00146_0000014_82773_140_44',
            "display_name": 'CO2'
            "thickness": 0.01,
            "conductivity_coeff_a": 0.0146,
            "viscosity_coeff_a": 0.000014,
            "specific_heat_coeff_a": 827.73,
            "specific_heat_ratio": 1.4
            "molecular_weight": 44
            }
        """
        assert data['type'] == 'EnergyWindowMaterialGasCustom', \
            'Expected EnergyWindowMaterialGasCustom. Got {}.'.format(data['type'])
        con_b = 0 if 'conductivity_coeff_b' not in data else data['conductivity_coeff_b']
        vis_b = 0 if 'viscosity_coeff_b' not in data else data['viscosity_coeff_b']
        sph_b = 0 if 'specific_heat_coeff_b' not in data \
            else data['specific_heat_coeff_b']
        con_c = 0 if 'conductivity_coeff_c' not in data else data['conductivity_coeff_c']
        vis_c = 0 if 'viscosity_coeff_c' not in data else data['viscosity_coeff_c']
        sph_c = 0 if 'specific_heat_coeff_c' not in data \
            else data['specific_heat_coeff_c']
        sphr = 1.0 if 'specific_heat_ratio' not in data else data['specific_heat_ratio']
        mw = 20.0 if 'molecular_weight' not in data else data['molecular_weight']
        new_obj = cls(data['identifier'], data['thickness'],
                      data['conductivity_coeff_a'],
                      data['viscosity_coeff_a'],
                      data['specific_heat_coeff_a'],
                      con_b, vis_b, sph_b, con_c, vis_c, sph_c, sphr, mw)
        if 'display_name' in data and data['display_name'] is not None:
            new_obj.display_name = data['display_name']
        if 'user_data' in data and data['user_data'] is not None:
            new_obj.user_data = data['user_data']
        if 'properties' in data and data['properties'] is not None:
            new_obj._properties._load_extension_attr_from_dict(data['properties'])
        return new_obj

    def to_idf(self):
        """Get an EnergyPlus string representation of the material.

        .. code-block:: shell

            WindowMaterial:Gas,
                Gas_16_W_0_0003,    !- gap name
                Custom,             !- type
                0.0003,             !- thickness
                2.873000e-003,      !- Conductivity Coefficient A
                7.760000e-005,      !- Conductivity Coefficient B
                0.000000e+000,      !- Conductivity Coefficient C
                3.723000e-006,      !- Conductivity Viscosity A
                4.940000e-008,      !- Conductivity Viscosity B
                0.000000e+000,      !- Conductivity Viscosity C
                1002.737000,        !- Specific Heat Coefficient A
                0.012324,           !- Specific Heat Coefficient B
                0.000000,           !- Specific Heat Coefficient C
                28.969999,          !- Molecular Weight
                1.400000;           !- Specific Heat Ratio
        """
        values = (self.identifier, 'Custom', self.thickness, self.conductivity_coeff_a,
                  self.conductivity_coeff_b, self.conductivity_coeff_c,
                  self.viscosity_coeff_a, self.viscosity_coeff_b,
                  self.viscosity_coeff_c, self.specific_heat_coeff_a,
                  self.specific_heat_coeff_b, self.specific_heat_coeff_c,
                  self.molecular_weight, self.specific_heat_ratio)
        comments = ('name', 'gas type', 'thickness', 'conductivity coeff a',
                    'conductivity coeff b', 'conductivity coeff c', 'viscosity coeff a',
                    'viscosity coeff b', 'viscosity coeff c', 'specific heat coeff a',
                    'specific heat coeff b', 'specific heat coeff c',
                    'molecular weight', 'specific heat ratio')
        return generate_idf_string('WindowMaterial:Gas', values, comments)

    def to_dict(self):
        """Energy Material Gas Custom dictionary representation."""
        base = {
            'type': 'EnergyWindowMaterialGasCustom',
            'identifier': self.identifier,
            'thickness': self.thickness,
            'conductivity_coeff_a': self.conductivity_coeff_a,
            'viscosity_coeff_a': self.viscosity_coeff_a,
            'specific_heat_coeff_a': self.specific_heat_coeff_a,
            'conductivity_coeff_b': self.conductivity_coeff_b,
            'viscosity_coeff_b': self.viscosity_coeff_b,
            'specific_heat_coeff_b': self.specific_heat_coeff_b,
            'conductivity_coeff_c': self.conductivity_coeff_c,
            'viscosity_coeff_c': self.viscosity_coeff_c,
            'specific_heat_coeff_c': self.specific_heat_coeff_c,
            'specific_heat_ratio': self.specific_heat_ratio,
            'molecular_weight': self.molecular_weight
        }
        if self._display_name is not None:
            base['display_name'] = self.display_name
        if self._user_data is not None:
            base['user_data'] = self.user_data
        prop_dict = self._properties.to_dict()
        if prop_dict is not None:
            base['properties'] = prop_dict
        return base

    def __key(self):
        """A tuple based on the object properties, useful for hashing."""
        return (self.identifier, self.thickness, self.conductivity_coeff_a,
                self.viscosity_coeff_a, self.specific_heat_coeff_a,
                self.conductivity_coeff_b, self.viscosity_coeff_b,
                self.specific_heat_coeff_b, self.conductivity_coeff_c,
                self.viscosity_coeff_c, self.specific_heat_coeff_c,
                self.specific_heat_ratio, self.molecular_weight)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        return isinstance(other, EnergyWindowMaterialGasCustom) and \
            self.__key() == other.__key()

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return self.to_idf()

    def __copy__(self):
        new_obj = EnergyWindowMaterialGasCustom(
            self.identifier, self.thickness, self.conductivity_coeff_a,
            self.viscosity_coeff_a, self.specific_heat_coeff_a,
            self.conductivity_coeff_b, self.viscosity_coeff_b,
            self.specific_heat_coeff_b, self.conductivity_coeff_c,
            self.viscosity_coeff_c, self.specific_heat_coeff_c,
            self.specific_heat_ratio, self.molecular_weight)
        new_obj._display_name = self._display_name
        new_obj._user_data = None if self._user_data is None else self._user_data.copy()
        new_obj._properties._duplicate_extension_attr(self._properties)
        return new_obj
