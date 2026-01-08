"""Tests the features that fairyfly_therm adds to fairyfly_core Model."""
import pytest
import os

from fairyfly.model import Model

from fairyfly_therm.properties.model import ModelThermProperties
from fairyfly_therm.material import SolidMaterial, CavityMaterial, Gas
from fairyfly_therm.condition import SteadyState
from fairyfly_therm.lib.materials import concrete, air_cavity
from fairyfly_therm.lib.conditions import exterior, interior


def test_therm_properties():
    """Test the existence of the Model therm properties."""
    model = Model.from_layers([100, 200, 100], height=1000)
    aer_concrete = SolidMaterial(0.1, 0.9, None, 400, 0.81, 850, 7.9)
    model.shapes[0].properties.therm.material = concrete
    model.shapes[1].properties.therm.material = air_cavity
    model.shapes[2].properties.therm.material = aer_concrete
    model.boundaries[0].properties.therm.condition = exterior
    model.boundaries[1].properties.therm.condition = interior
    model.display_name = 'Roman Bath Wall'

    assert hasattr(model.properties, 'therm')
    assert isinstance(model.properties.therm, ModelThermProperties)
    assert isinstance(model.properties.host, Model)
    assert len(model.properties.therm.materials) == 3
    for mat in model.properties.therm.materials:
        assert isinstance(mat, (SolidMaterial, CavityMaterial))
    assert len(model.properties.therm.conditions) == 2
    for mat in model.properties.therm.conditions:
        assert isinstance(mat, SteadyState)
    assert len(model.properties.therm.gases) == 1
    for mat in model.properties.therm.gases:
        assert isinstance(mat, Gas)


def test_check_duplicate_material_identifiers():
    """Test the check_duplicate_material_identifiers method."""
    model = Model.from_layers([100, 200, 100], height=1000)
    aer_concrete = SolidMaterial(0.1, 0.9, None, 400, 0.81, 850, 7.9)
    model.shapes[0].properties.therm.material = concrete
    model.shapes[1].properties.therm.material = air_cavity
    model.shapes[2].properties.therm.material = aer_concrete
    model.boundaries[0].properties.therm.condition = exterior
    model.boundaries[1].properties.therm.condition = interior
    model.display_name = 'Roman Bath Wall'

    assert model.properties.therm.check_duplicate_material_identifiers(False) == ''
    aer_concrete.unlock()
    aer_concrete.identifier = concrete.identifier
    aer_concrete.lock()
    assert model.properties.therm.check_duplicate_material_identifiers(False) != ''
    with pytest.raises(ValueError):
        model.properties.therm.check_duplicate_material_identifiers(True)


def test_check_duplicate_condition_identifiers():
    """Test the check_duplicate_condition_identifiers method."""
    model = Model.from_layers([100, 200, 100], height=1000)
    interior_warm = SteadyState(26, 3.2)
    model.shapes[0].properties.therm.material = concrete
    model.shapes[1].properties.therm.material = air_cavity
    model.shapes[2].properties.therm.material = concrete
    model.boundaries[0].properties.therm.condition = exterior
    model.boundaries[1].properties.therm.condition = interior_warm
    model.display_name = 'Roman Bath Wall'

    assert model.properties.therm.check_duplicate_condition_identifiers(False) == ''
    interior_warm.unlock()
    interior_warm.identifier = exterior.identifier
    interior_warm.lock()
    assert model.properties.therm.check_duplicate_condition_identifiers(False) != ''
    with pytest.raises(ValueError):
        model.properties.therm.check_duplicate_condition_identifiers(True)


def test_to_dict():
    """Test the Model to_dict method ."""
    model = Model.from_layers([100, 200, 100], height=1000)
    aer_concrete = SolidMaterial(0.1, 0.9, None, 400, 0.81, 850, 7.9)
    interior_warm = SteadyState(26, 3.2)
    model.shapes[0].properties.therm.material = concrete
    model.shapes[1].properties.therm.material = air_cavity
    model.shapes[2].properties.therm.material = aer_concrete
    model.boundaries[0].properties.therm.condition = exterior
    model.boundaries[1].properties.therm.condition = interior_warm
    model.display_name = 'Roman Bath Wall'

    model_dict = model.to_dict()

    assert 'therm' in model_dict['properties']
    assert 'materials' in model_dict['properties']['therm']
    assert 'conditions' in model_dict['properties']['therm']
    assert 'gases' in model_dict['properties']['therm']
    assert 'pure_gases' in model_dict['properties']['therm']

    assert len(model_dict['properties']['therm']['materials']) == 3
    assert len(model_dict['properties']['therm']['conditions']) == 2
    assert len(model_dict['properties']['therm']['gases']) == 1
    assert len(model_dict['properties']['therm']['pure_gases']) == 1

    assert model_dict['shapes'][0]['properties']['therm']['material'] == \
        concrete.identifier
    assert model_dict['shapes'][1]['properties']['therm']['material'] == \
        air_cavity.identifier
    assert model_dict['shapes'][2]['properties']['therm']['material'] == \
        aer_concrete.identifier

    assert model_dict['boundaries'][0]['properties']['therm']['condition'] == \
        exterior.identifier
    assert model_dict['boundaries'][1]['properties']['therm']['condition'] == \
        interior_warm.identifier


def test_to_from_dict():
    """Test the Model to_dict and from_dict method."""
    model = Model.from_layers([100, 200, 100], height=1000)
    aer_concrete = SolidMaterial(0.1, 0.9, None, 400, 0.81, 850, 7.9)
    interior_warm = SteadyState(26, 3.2)
    model.shapes[0].properties.therm.material = concrete
    model.shapes[1].properties.therm.material = air_cavity
    model.shapes[2].properties.therm.material = aer_concrete
    model.boundaries[0].properties.therm.condition = exterior
    model.boundaries[1].properties.therm.condition = interior_warm
    model.display_name = 'Roman Bath Wall'

    model_dict = model.to_dict(included_prop=['therm'])
    new_model = Model.from_dict(model_dict)
    assert model_dict == new_model.to_dict(included_prop=['therm'])

    assert new_model.display_name == 'Roman Bath Wall'
    assert aer_concrete in new_model.properties.therm.materials
    assert new_model.shapes[0].properties.therm.material == concrete
    assert new_model.shapes[1].properties.therm.material == air_cavity
    assert new_model.shapes[2].properties.therm.material == aer_concrete
    assert new_model.boundaries[0].properties.therm.condition == exterior
    assert new_model.boundaries[1].properties.therm.condition == interior_warm


def test_to_therm_xml():
    """Test the Model to_therm_xml method ."""
    model = Model.from_layers([100, 200, 100], height=1000)
    aer_concrete = SolidMaterial(0.1, 0.9, None, 400, 0.81, 850, 7.9)
    interior_warm = SteadyState(26, 3.2)
    interior_warm.display_name = 'Warm Interior'
    model.shapes[0].properties.therm.material = concrete
    model.shapes[1].properties.therm.material = air_cavity
    model.shapes[2].properties.therm.material = aer_concrete
    model.boundaries[0].properties.therm.condition = exterior
    model.boundaries[1].properties.therm.condition = interior_warm
    model.display_name = 'Roman Bath Wall'

    assert hasattr(model.to, 'therm_xml')
    assert hasattr(model, 'to_therm_xml')
    xml_str = model.to_therm_xml()
    assert len(xml_str) != 0


def test_to_thmz():
    """Test the Model to_thmz method with a basic model."""
    model = Model.from_layers([100, 200, 100], height=500)
    aer_concrete = SolidMaterial(0.1, 0.95, None, 400, 0.81, 850, 7.9)
    aer_concrete.display_name = 'Aerated Concrete'
    insulation = SolidMaterial(0.049, 0.9, None, None, None, None)
    insulation.display_name = 'Insulation'
    interior_warm = SteadyState(26, 3.2)
    interior_warm.display_name = 'Warm Interior'
    model.shapes[0].properties.therm.material = concrete
    model.shapes[1].properties.therm.material = insulation
    model.shapes[2].properties.therm.material = aer_concrete
    model.boundaries[0].properties.therm.condition = exterior
    model.boundaries[1].properties.therm.condition = interior_warm
    model.boundaries[1].properties.therm.u_factor_tag = 'Wall Assembly'
    model.display_name = 'Roman Bath Wall'

    assert hasattr(model.to, 'thmz')
    assert hasattr(model, 'to_thmz')
    output_file = './tests/assets/thmz/TestModel.thmz'
    model.to_thmz(output_file)
    assert os.path.isfile(output_file)
    os.remove(output_file)


def test_to_thmz_cavity():
    """Test the Model to_thmz method with an air cavity."""
    model = Model.from_layers([100, 200, 100], height=200)
    interior_warm = SteadyState(26, 3.2)
    interior_warm.display_name = 'Warm Interior'
    model.shapes[0].properties.therm.material = concrete
    model.shapes[1].properties.therm.material = air_cavity
    model.shapes[2].properties.therm.material = concrete
    model.boundaries[0].properties.therm.condition = exterior
    model.boundaries[1].properties.therm.condition = interior_warm

    output_file = './tests/assets/thmz/CavityModel.thmz'
    model.to_thmz(output_file)
    assert os.path.isfile(output_file)
    os.remove(output_file)


def test_to_thmz_stud_wall():
    """Test the Model to_thmz method with an stud wall."""
    input_file = './tests/assets/json/stud_wall.ffjson'
    model = Model.from_file(input_file)

    output_file = './tests/assets/thmz/stud_wall.thmz'
    model.to_thmz(output_file)
    assert os.path.isfile(output_file)
    os.remove(output_file)
