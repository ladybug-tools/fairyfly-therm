# coding=utf-8
import pytest
import uuid

from fairyfly_therm.material.solid import SolidMaterial


def test_material_init():
    """Test the initialization of SolidMaterial objects and basic properties."""
    mat_id = uuid.uuid4()
    concrete = SolidMaterial(0.5, 0.95, None, 800, 0.81, 1200, 7.9, identifier=mat_id)
    concrete.display_name = 'Concrete'
    str(concrete)  # test the string representation of the material
    concrete_dup = concrete.duplicate()

    assert concrete.identifier == concrete_dup.identifier == str(mat_id)
    assert concrete.display_name == concrete_dup.display_name == 'Concrete'
    assert concrete.conductivity == concrete_dup.conductivity == 0.5
    assert concrete.emissivity == concrete_dup.emissivity == 0.95
    assert concrete.emissivity_back == concrete_dup.emissivity_back == 0.95
    assert concrete.density == concrete_dup.density == 800
    assert concrete.porosity == concrete_dup.porosity == 0.81
    assert concrete.specific_heat == concrete_dup.specific_heat == 1200
    assert concrete.vapor_diffusion_resistance == concrete_dup.vapor_diffusion_resistance == 7.9
    assert concrete.resistivity == 1 / 0.5

    with pytest.raises(AssertionError):
        concrete.conductivity = 0


def test_material_equivalency():
    """Test the equality of a material to another SolidMaterial."""
    concrete_1 = SolidMaterial(0.5, 0.95, None, 800, 0.81, 1200, 7.9)
    concrete_1.display_name = 'Concrete'
    concrete_2 = concrete_1.duplicate()
    insulation = SolidMaterial(0.049, 0.9, None, 265, None, 836)
    insulation.display_name = 'Insulation'

    assert concrete_1 == concrete_2
    assert concrete_1 != insulation
    collection = [concrete_1, concrete_2, insulation]
    assert len(set(collection)) == 2

    concrete_2.density = 600
    assert concrete_1 != concrete_2
    assert len(set(collection)) == 3


def test_material_lockability():
    """Test the lockability of the SolidMaterial."""
    concrete = SolidMaterial(0.5, 0.95, None, 800, 0.81, 1200, 7.9)
    concrete.density = 600
    concrete.lock()
    with pytest.raises(AttributeError):
        concrete.density = 700
    concrete.unlock()
    concrete.density = 700


def test_material_invalid():
    """Test the initialization of SolidMaterial objects with invalid properties."""
    concrete = SolidMaterial(0.5, 0.95, None, 800, 0.81, 1200, 7.9)

    with pytest.raises(ValueError):
        concrete.identifier = 'test_identifier'
    with pytest.raises(AssertionError):
        concrete.conductivity = -1
    with pytest.raises(AssertionError):
        concrete.emissivity = 2
    with pytest.raises(AssertionError):
        concrete.emissivity_back = 2
    with pytest.raises(AssertionError):
        concrete.density = -1
    with pytest.raises(AssertionError):
        concrete.specific_heat = -1


def test_material_to_from_xml():
    """Test the initialization of SolidMaterial objects from XML elements."""
    mat_id = uuid.uuid4()
    concrete = SolidMaterial(0.5, 0.95, None, 800, 0.81, 1200, 7.9, identifier=mat_id)
    concrete.display_name = 'Concrete'
    xml_mat = concrete.to_therm_xml_str()
    concrete_dup = SolidMaterial.from_therm_xml_str(xml_mat)

    assert concrete == concrete_dup
    assert concrete.identifier == concrete_dup.identifier == str(mat_id)
    assert concrete.display_name == concrete_dup.display_name == 'Concrete'
    assert concrete.conductivity == concrete_dup.conductivity == 0.5
    assert concrete.emissivity == concrete_dup.emissivity == 0.95
    assert concrete.emissivity_back == concrete_dup.emissivity_back == 0.95
    assert concrete.density == concrete_dup.density == 800
    assert concrete.porosity == concrete_dup.porosity == 0.81
    assert concrete.specific_heat == concrete_dup.specific_heat == 1200
    assert concrete.vapor_diffusion_resistance == concrete_dup.vapor_diffusion_resistance == 7.9


def test_material_dict_methods():
    """Test the to/from dict methods."""
    mat_id = uuid.uuid4()
    concrete = SolidMaterial(0.5, 0.95, None, 800, 0.81, 1200, 7.9, identifier=mat_id)
    concrete.display_name = 'Concrete'

    material_dict = concrete.to_dict()
    concrete_dup = SolidMaterial.from_dict(material_dict)

    assert material_dict == concrete_dup.to_dict()
    assert concrete == concrete_dup
    assert concrete.identifier == concrete_dup.identifier == str(mat_id)
    assert concrete.display_name == concrete_dup.display_name == 'Concrete'
    assert concrete.conductivity == concrete_dup.conductivity == 0.5
    assert concrete.emissivity == concrete_dup.emissivity == 0.95
    assert concrete.emissivity_back == concrete_dup.emissivity_back == 0.95
    assert concrete.density == concrete_dup.density == 800
    assert concrete.porosity == concrete_dup.porosity == 0.81
    assert concrete.specific_heat == concrete_dup.specific_heat == 1200
    assert concrete.vapor_diffusion_resistance == concrete_dup.vapor_diffusion_resistance == 7.9
