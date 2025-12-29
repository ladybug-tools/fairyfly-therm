# coding=utf-8
import pytest
import uuid

from fairyfly.typing import therm_id_from_uuid

from fairyfly_therm.material.cavity import CavityMaterial
from fairyfly_therm.material.gas import Gas, PureGas
from fairyfly_therm.lib.gases import air


def test_cavity_material_init():
    """Test the initialization of CavityMaterialMaterial objects and basic properties."""
    mat_id = uuid.uuid4()
    air_gap = CavityMaterial(air, 'ISO15099', 0.95, None, identifier=mat_id)
    air_gap.display_name = 'ISO Air Gap'
    str(air_gap)  # test the string representation of the material
    air_gap_dup = air_gap.duplicate()

    assert air_gap.identifier == air_gap_dup.identifier == str(mat_id)
    assert air_gap.display_name == air_gap_dup.display_name == 'ISO Air Gap'
    assert air_gap.gas == air_gap_dup.gas == air
    assert air_gap.emissivity == air_gap_dup.emissivity == 0.95
    assert air_gap.emissivity_back == air_gap_dup.emissivity_back == 0.95

    with pytest.raises(AssertionError):
        air_gap.gas = 'Air'


def test_cavity_material_equivalency():
    """Test the equality of a material to another CavityMaterial."""
    air_gap_1 = CavityMaterial(air, 'ISO15099', 0.95, None)
    air_gap_1.display_name = 'ISO Air Gap'
    air_gap_2 = air_gap_1.duplicate()
    gas_id = uuid.uuid4()
    co2_pure = PureGas(0.0146, 0.000014, 827.73)
    co2_pure.specific_heat_ratio = 1.4
    co2_pure.molecular_weight = 44
    co2 = Gas([co2_pure], [1], identifier=gas_id)
    co2.display_name = 'CO2'
    co2_gap = CavityMaterial(co2, 'ISO15099', 0.95, None)
    co2_gap.display_name = 'ISO CO2 Gap'

    assert air_gap_1 == air_gap_2
    assert air_gap_1 != co2_gap
    collection = [air_gap_1, air_gap_2, co2_gap]
    assert len(set(collection)) == 2

    air_gap_2.cavity_model = 'CEN'
    assert air_gap_1 != air_gap_2
    assert len(set(collection)) == 3


def test_cavity_material_lockability():
    """Test the lockability of the CavityMaterial."""
    air_gap = CavityMaterial(air, 'ISO15099', 0.95, None)
    air_gap.cavity_model = 'CEN'
    air_gap.lock()
    with pytest.raises(AttributeError):
        air_gap.cavity_model = 'NFRC'
    air_gap.unlock()
    air_gap.cavity_model = 'NFRC'


def test_cavity_material_to_from_xml():
    """Test the initialization of CavityMaterial objects from XML elements."""
    gas_id = uuid.uuid4()
    co2_pure = PureGas(0.0146, 0.000014, 827.73)
    co2_pure.specific_heat_ratio = 1.4
    co2_pure.molecular_weight = 44
    co2 = Gas([co2_pure], [1], identifier=gas_id)
    co2.display_name = 'CO2'
    mat_id = uuid.uuid4()
    co2_gap = CavityMaterial(co2, 'ISO15099', 0.95, None, identifier=mat_id)
    co2_gap.display_name = 'ISO CO2 Gap'
    xml_mat = co2_gap.to_therm_xml_str()
    co2_gap_dup = CavityMaterial.from_therm_xml_str(xml_mat, {'CO2': co2})

    assert co2_gap == co2_gap_dup
    assert co2_gap.therm_uuid == co2_gap_dup.therm_uuid == therm_id_from_uuid(str(mat_id))
    assert co2_gap.display_name == co2_gap_dup.display_name == 'ISO CO2 Gap'
    assert co2_gap.cavity_model == co2_gap_dup.cavity_model == 'ISO15099'
    assert co2_gap.gas == co2_gap_dup.gas == co2
    assert co2_gap.emissivity == co2_gap_dup.emissivity == 0.95
    assert co2_gap.emissivity_back == co2_gap_dup.emissivity_back == 0.95


def test_cavity_material_dict_methods():
    """Test the to/from dict methods."""
    gas_id = uuid.uuid4()
    co2_pure = PureGas(0.0146, 0.000014, 827.73)
    co2_pure.specific_heat_ratio = 1.4
    co2_pure.molecular_weight = 44
    co2 = Gas([co2_pure], [1], identifier=gas_id)
    co2.display_name = 'CO2'
    mat_id = uuid.uuid4()
    co2_gap = CavityMaterial(co2, 'ISO15099', 0.95, None, identifier=mat_id)
    co2_gap.display_name = 'ISO CO2 Gap'

    material_dict = co2_gap.to_dict()
    co2_gap_dup = CavityMaterial.from_dict(material_dict)

    mat_dict_abridged = co2_gap.to_dict(abridged=True)
    co2_gap_dup2 = CavityMaterial.from_dict_abridged(mat_dict_abridged, {str(gas_id): co2})

    assert material_dict == co2_gap_dup.to_dict()
    assert mat_dict_abridged == co2_gap_dup2.to_dict(abridged=True)
    assert co2_gap == co2_gap_dup == co2_gap_dup2
    assert co2_gap.identifier == co2_gap_dup.identifier == co2_gap_dup2.identifier == str(mat_id)
    assert co2_gap.display_name == co2_gap_dup.display_name == co2_gap_dup2.display_name == 'ISO CO2 Gap'
    assert co2_gap.cavity_model == co2_gap_dup.cavity_model == co2_gap_dup2.cavity_model == 'ISO15099'
    assert co2_gap.emissivity == co2_gap_dup.emissivity == co2_gap_dup2.emissivity == 0.95
    assert co2_gap.emissivity_back == co2_gap_dup.emissivity_back == co2_gap_dup2.emissivity_back == 0.95
