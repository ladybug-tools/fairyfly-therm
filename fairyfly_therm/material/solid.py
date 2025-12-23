# coding=utf-8
"""Solid THERM materials."""
from __future__ import division
import xml.etree.ElementTree as ET

from fairyfly._lockable import lockable
from fairyfly.typing import float_in_range, float_positive

from ._base import _ThermMaterialBase


@lockable
class SolidMaterial(_ThermMaterialBase):
    """Typical conductive material.

    Args:
        conductivity: Number for the thermal conductivity of the material [W/m-K].
        emissivity: Number between 0 and 1 for the infrared hemispherical
            emissivity of the front side of the glass. (Default: 0.9).
        emissivity_back: Number between 0 and 1 for the infrared hemispherical
            emissivity of the back side of the glass. If None, this will
            default to the same value specified for emissivity. (Default: None)
        density: Optional number for the density of the material [kg/m3]. (Default: None).
        porosity: Optional number between zero and one for the porosity of
            the material. (Default: None).
        specific_heat: Optional number for the specific heat of the material [J/kg-K].
            If None, it is not included in the export. (Default: None).
        vapor_diffusion_resistance: Optional number for the water vapor diffusion
            resistance factor [Dimensionless]. (Default: None).
        identifier: Text string for a unique object ID. Must be a UUID in the
            format xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx. If None, a UUID will
            automatically be generated. (Default: None).

    Properties:
        * identifier
        * display_name
        * conductivity
        * emissivity
        * emissivity_back
        * density
        * porosity
        * specific_heat
        * vapor_diffusion_resistance
        * resistivity
        * color
        * protected
        * user_data
    """
    __slots__ = ('_conductivity', '_emissivity', '_emissivity_back',
                 '_density', '_porosity', '_specific_heat',
                 '_vapor_diffusion_resistance')

    def __init__(
        self, conductivity, emissivity=0.9, emissivity_back=None,
        density=None, porosity=None, specific_heat=None,
        vapor_diffusion_resistance=None, identifier=None
    ):
        """Initialize therm material."""
        _ThermMaterialBase.__init__(self, identifier)
        self.conductivity = conductivity
        self.emissivity = emissivity
        self.emissivity_back = emissivity_back
        self.density = density
        self.porosity = porosity
        self.specific_heat = specific_heat
        self.vapor_diffusion_resistance = vapor_diffusion_resistance

    @property
    def conductivity(self):
        """Get or set the conductivity of the material layer [W/m-K]."""
        return self._conductivity

    @conductivity.setter
    def conductivity(self, cond):
        self._conductivity = float_positive(cond, 'material conductivity')
        assert self._conductivity != 0, 'Conductivity cannot be equal to zero.'

    @property
    def emissivity(self):
        """Get or set the hemispherical emissivity of the front side of the material."""
        return self._emissivity

    @emissivity.setter
    def emissivity(self, ir_e):
        ir_e = float_in_range(ir_e, 0.0, 1.0, 'material emissivity')
        self._emissivity = ir_e

    @property
    def emissivity_back(self):
        """Get or set the hemispherical emissivity of the back side of the material."""
        return self._emissivity_back if self._emissivity_back is not None \
            else self._emissivity

    @emissivity_back.setter
    def emissivity_back(self, ir_e):
        if ir_e is not None:
            ir_e = float_in_range(ir_e, 0.0, 1.0, 'material emissivity')
        self._emissivity_back = ir_e

    @property
    def density(self):
        """Get or set the density of the material layer [kg/m3]."""
        return self._density

    @density.setter
    def density(self, value):
        if value is not None:
            value = float_positive(value, 'material density')
        self._density = value

    @property
    def porosity(self):
        """Get or set a number between zero and one for the porosity."""
        return self._porosity

    @porosity.setter
    def porosity(self, value):
        if value is not None:
            value = float_in_range(value, 0.0, 1.0, 'material porosity')
        self._porosity = value

    @property
    def specific_heat(self):
        """Get or set the specific heat of the material layer [J/kg-K]."""
        return self._specific_heat

    @specific_heat.setter
    def specific_heat(self, value):
        if value is not None:
            value = float_positive(value, 'material specific heat')
        self._specific_heat = value

    @property
    def vapor_diffusion_resistance(self):
        """Get or set the vapor diffusion resistance of the material."""
        return self._vapor_diffusion_resistance

    @vapor_diffusion_resistance.setter
    def vapor_diffusion_resistance(self, value):
        if value is not None:
            value = float_positive(value, 'vapor diffusion resistance')
        self._vapor_diffusion_resistance = value

    @property
    def resistivity(self):
        """Get or set the resistivity of the material layer [m-K/W]."""
        return 1 / self._conductivity

    @resistivity.setter
    def resistivity(self, resis):
        self._conductivity = 1 / float_positive(resis, 'material resistivity')

    @classmethod
    def from_therm_xml(cls, xml_element):
        """Create a SolidMaterial from an XML element of a THERM Material.

        Args:
            xml_element: An XML element of a THERM material.
        """
        # create the base material from the UUID and conductivity
        xml_uuid = xml_element.find('UUID')
        identifier = xml_uuid.text
        xml_solid = xml_element.find('Solid')
        xml_hyt = xml_solid.find('HygroThermal')
        xml_cond = xml_hyt.find('ThermalConductivityDry')
        conductivity = xml_cond.text
        mat = SolidMaterial(conductivity, identifier=identifier)
        # assign the other hygrothermal attributes if specified
        xml_dens = xml_hyt.find('BulkDensity')
        if xml_dens is not None:
            mat.density = xml_dens.text
        xml_por = xml_hyt.find('Porosity')
        if xml_por is not None:
            mat.porosity = xml_por.text
        xml_shc = xml_hyt.find('SpecificHeatCapacityDry')
        if xml_shc is not None:
            mat.specific_heat = xml_shc.text
        xml_vdr = xml_hyt.find('WaterVaporDiffusionResistanceFactor')
        if xml_vdr is not None:
            mat.vapor_diffusion_resistance = xml_vdr.text
        # assign the optical properties if specified
        xml_optical = xml_solid.find('Optical')
        if xml_optical is not None:
            xml_int = xml_optical.find('Integrated')
            if xml_int is not None:
                xml_inf = xml_int.find('Infrared')
                if xml_inf is not None:
                    xml_emiss = xml_inf.find('Emissivity-Front')
                    if xml_emiss is not None:
                        mat.emissivity = xml_emiss.text
                    xml_emiss_b = xml_inf.find('Emissivity-Back')
                    if xml_emiss_b is not None:
                        mat.emissivity_back = xml_emiss_b.text
        # assign the name and color if they are specified
        xml_name = xml_element.find('Name')
        if xml_name is not None:
            mat.display_name = xml_name.text
        xml_col = xml_element.find('Color')
        if xml_col is not None:
            mat.color = xml_col.text
        xml_protect = xml_element.find('Protected')
        if xml_protect is not None:
            mat.protected = True if xml_protect.text == 'true' else False
        return mat

    @classmethod
    def from_therm_xml_str(cls, xml_str):
        """Create a SolidMaterial from an XML text string of a THERM Material.

        Args:
            xml_str: An XML text string of a THERM material.
        """
        root = ET.fromstring(xml_str)
        return cls.from_therm_xml(root)

    @classmethod
    def from_dict(cls, data):
        """Create a SolidMaterial from a dictionary.

        Args:
            data: A python dictionary in the following format

        .. code-block:: python

            {
            "type": 'SolidMaterial',
            "identifier": 'f26f3597-e3ee-43fe-a0b3-ec673f993d86',
            "display_name": 'Concrete',
            "conductivity": 2.31,
            "emissivity": 0.9,
            "emissivity_back": 0.9,
            "density": 2322,
            "porosity": 0.24,
            "specific_heat": 832,
            "vapor_diffusion_resistance": 19
            }
        """
        assert data['type'] == 'SolidMaterial', \
            'Expected SolidMaterial. Got {}.'.format(data['type'])

        emiss = data['emissivity'] if 'emissivity' in data and \
            data['emissivity'] is not None else 0.9
        emiss_b = data['emissivity_back'] if 'emissivity_back' in data else None
        dens = data['density'] if 'density' in data else None
        poro = data['porosity'] if 'porosity' in data else None
        s_heat = data['specific_heat'] if 'specific_heat' in data else None
        vdr = data['vapor_diffusion_resistance'] \
            if 'vapor_diffusion_resistance' in data else None

        new_mat = cls(
            data['conductivity'], emiss, emiss_b, dens, poro, s_heat, vdr,
            data['identifier'])
        if 'display_name' in data and data['display_name'] is not None:
            new_mat.display_name = data['display_name']
        if 'color' in data and data['color'] is not None:
            new_mat.color = data['color']
        if 'protected' in data and data['protected'] is not None:
            new_mat.protected = data['protected']
        if 'user_data' in data and data['user_data'] is not None:
            new_mat.user_data = data['user_data']
        return new_mat

    def to_therm_xml(self, materials_element=None):
        """Get an THERM XML element of the material.

        Args:
            materials_element: An optional XML Element for the Materials to
                which the generated objects will be added. If None, a new XML
                Element will be generated.

        .. code-block:: xml

            <Material>
                <UUID>1543f77f-e4aa-47d4-b7bf-2365d7bc0b9d</UUID>
                <Name>Polyurethane Foam</Name>
                <Protected>false</Protected>
                <Color>0xFFFFC1</Color>
                <Solid>
                    <HygroThermal>
                        <ThermalConductivityDry>0.05</ThermalConductivityDry>
                    </HygroThermal>
                    <Optical>
                        <Integrated>
                            <Infrared>
                                <Emissivity-Front>0.9</Emissivity-Front>
                                <Emissivity-Back>0.9</Emissivity-Back>
                            </Infrared>
                        </Integrated>
                    </Optical>
                </Solid>
            </Material>
        """
        # create a new Materials element if one is not specified
        if materials_element is not None:
            xml_mat = ET.SubElement(materials_element, 'Material')
        else:
            xml_mat = ET.Element('Material')
        # add all of the required basic attributes
        xml_id = ET.SubElement(xml_mat, 'UUID')
        xml_id.text = self.identifier
        xml_name = ET.SubElement(xml_mat, 'Name')
        xml_name.text = self.display_name
        xml_protect = ET.SubElement(xml_mat, 'Protected')
        xml_protect.text = 'true' if self.protected else 'false'
        xml_color = ET.SubElement(xml_mat, 'Color')
        xml_color.text = self.color.to_hex()
        xml_solid = ET.SubElement(xml_mat, 'Solid')
        # add all of the required hygrothermal and optical attributes
        xml_hyt = ET.SubElement(xml_solid, 'HygroThermal')
        xml_cond = ET.SubElement(xml_hyt, 'ThermalConductivityDry')
        xml_cond.text = str(self.conductivity)
        xml_optical = ET.SubElement(xml_solid, 'Optical')
        xml_int = ET.SubElement(xml_optical, 'Integrated')
        xml_inf = ET.SubElement(xml_int, 'Infrared')
        xml_emiss = ET.SubElement(xml_inf, 'Emissivity-Front')
        xml_emiss.text = str(self.emissivity)
        xml_emiss_b = ET.SubElement(xml_inf, 'Emissivity-Back')
        xml_emiss_b.text = str(self.emissivity_back)
        # add any of the optional hygrothermal attributes
        if self.density is not None:
            xml_dens = ET.SubElement(xml_hyt, 'BulkDensity')
            xml_dens.text = str(self.density)
        if self.porosity is not None:
            xml_por = ET.SubElement(xml_hyt, 'Porosity')
            xml_por.text = str(self.porosity)
        if self.specific_heat is not None:
            xml_shc = ET.SubElement(xml_hyt, 'SpecificHeatCapacityDry')
            xml_shc.text = str(self.specific_heat)
        if self.vapor_diffusion_resistance is not None:
            xml_vdr = ET.SubElement(xml_hyt, 'WaterVaporDiffusionResistanceFactor')
            xml_vdr.text = str(self.vapor_diffusion_resistance)
        return xml_mat

    def to_therm_xml_str(self):
        """Get an THERM XML string of the material."""
        xml_root = self.to_therm_xml()
        try:  # try to indent the XML to make it read-able
            ET.indent(xml_root)
            return ET.tostring(xml_root, encoding='unicode')
        except AttributeError:  # we are in Python 2 and no indent is available
            return ET.tostring(xml_root)

    def to_dict(self):
        """SolidMaterial dictionary representation."""
        base = {
            'type': 'SolidMaterial',
            'identifier': self.identifier,
            'conductivity': self.conductivity,
            'emissivity': self.emissivity
        }
        if self._emissivity_back is not None:
            base['emissivity_back'] = self._emissivity_back
        if self._density is not None:
            base['density'] = self._density
        if self._porosity is not None:
            base['porosity'] = self.porosity
        if self._specific_heat is not None:
            base['specific_heat'] = self.specific_heat
        if self._vapor_diffusion_resistance is not None:
            base['vapor_diffusion_resistance'] = self.vapor_diffusion_resistance
        if self._display_name is not None:
            base['display_name'] = self.display_name
        base['protected'] = self._protected
        base['color'] = self.color.to_hex()
        if self._user_data is not None:
            base['user_data'] = self.user_data
        return base

    def __key(self):
        """A tuple based on the object properties, useful for hashing."""
        return (self.identifier, self.conductivity, self.emissivity,
                self.emissivity_back, self.density, self.porosity,
                self.specific_heat, self.vapor_diffusion_resistance)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        return isinstance(other, SolidMaterial) and self.__key() == other.__key()

    def __ne__(self, other):
        return not self.__eq__(other)

    def __copy__(self):
        new_material = self.__class__(
            self.conductivity, self._emissivity, self._emissivity_back,
            self._density, self._porosity, self._specific_heat,
            self._vapor_diffusion_resistance, self.identifier)
        new_material._display_name = self._display_name
        new_material._color = self._color
        new_material._protected = self._protected
        new_material._user_data = None if self._user_data is None \
            else self._user_data.copy()
        return new_material

    def __repr__(self):
        return 'Solid THERM Material:\n{}'.format(self.display_name)
