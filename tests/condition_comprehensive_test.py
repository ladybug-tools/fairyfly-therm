# coding=utf-8
import pytest
import uuid

from fairyfly_therm.condition.comprehensive import ComprehensiveCondition


def test_condition_init():
    """Test the initialization of ComprehensiveCondition objects and basic properties."""
    cond_id = uuid.uuid4()
    nfrc_ext = ComprehensiveCondition(-18, 26, identifier=cond_id)
    nfrc_ext.display_name = 'NFRC 100-2010 Exterior'
    str(nfrc_ext)  # test the string representation of the condition
    nfrc_ext_dup = nfrc_ext.duplicate()

    assert nfrc_ext.identifier == nfrc_ext_dup.identifier == str(cond_id)
    assert nfrc_ext.display_name == nfrc_ext_dup.display_name == 'NFRC 100-2010 Exterior'
    assert nfrc_ext.temperature == nfrc_ext_dup.temperature == -18
    assert nfrc_ext.film_coefficient == nfrc_ext_dup.film_coefficient == 26
    assert nfrc_ext.emissivity == nfrc_ext_dup.emissivity == 1
    assert nfrc_ext.radiant_temperature == nfrc_ext_dup.radiant_temperature == -18
    assert nfrc_ext.heat_flux == nfrc_ext_dup.heat_flux == 0
    assert nfrc_ext.relative_humidity == nfrc_ext_dup.relative_humidity == 0.5


def test_condition_equivalency():
    """Test the equality of a condition to another ComprehensiveCondition."""
    nfrc_ext_1 = ComprehensiveCondition(-18, 26)
    nfrc_ext_1.display_name = 'NFRC 100-2010 Exterior'
    nfrc_ext_2 = nfrc_ext_1.duplicate()
    interior = ComprehensiveCondition(21, 2.44)
    interior.display_name = 'Inerior Wood/Vinyl Frame'

    assert nfrc_ext_1 == nfrc_ext_2
    assert nfrc_ext_1 != interior
    collection = [nfrc_ext_1, nfrc_ext_2, interior]
    assert len(set(collection)) == 2

    nfrc_ext_2.temperature = 36
    assert nfrc_ext_1 != nfrc_ext_2
    assert len(set(collection)) == 3


def test_condition_lockability():
    """Test the lockability of the ComprehensiveCondition."""
    nfrc_ext = ComprehensiveCondition(-18, 26)
    nfrc_ext.temperature = 36
    nfrc_ext.lock()
    with pytest.raises(AttributeError):
        nfrc_ext.temperature = 0
    nfrc_ext.unlock()
    nfrc_ext.temperature = -12


def test_condition_to_from_xml():
    """Test the initialization of ComprehensiveCondition objects from XML elements."""
    cond_id = uuid.uuid4()
    nfrc_ext = ComprehensiveCondition(-18, 26, identifier=cond_id)
    nfrc_ext.display_name = 'NFRC 100-2010 Exterior'
    xml_cond = nfrc_ext.to_therm_xml_str()
    nfrc_ext_dup = ComprehensiveCondition.from_therm_xml_str(xml_cond)

    assert nfrc_ext == nfrc_ext_dup
    assert nfrc_ext.identifier == nfrc_ext_dup.identifier == str(cond_id)
    assert nfrc_ext.display_name == nfrc_ext_dup.display_name == 'NFRC 100-2010 Exterior'
    assert nfrc_ext.temperature == nfrc_ext_dup.temperature == -18
    assert nfrc_ext.film_coefficient == nfrc_ext_dup.film_coefficient == 26
    assert nfrc_ext.emissivity == nfrc_ext_dup.emissivity == 1
    assert nfrc_ext.radiant_temperature == nfrc_ext_dup.radiant_temperature == -18
    assert nfrc_ext.heat_flux == nfrc_ext_dup.heat_flux == 0
    assert nfrc_ext.relative_humidity == nfrc_ext_dup.relative_humidity == 0.5


def test_condition_dict_methods():
    """Test the to/from dict methods."""
    cond_id = uuid.uuid4()
    nfrc_ext = ComprehensiveCondition(-18, 26, identifier=cond_id)
    nfrc_ext.display_name = 'NFRC 100-2010 Exterior'

    condition_dict = nfrc_ext.to_dict()
    nfrc_ext_dup = ComprehensiveCondition.from_dict(condition_dict)

    assert condition_dict == nfrc_ext_dup.to_dict()
    assert nfrc_ext == nfrc_ext_dup
    assert nfrc_ext.identifier == nfrc_ext_dup.identifier == str(cond_id)
    assert nfrc_ext.display_name == nfrc_ext_dup.display_name == 'NFRC 100-2010 Exterior'
    assert nfrc_ext.temperature == nfrc_ext_dup.temperature == -18
    assert nfrc_ext.film_coefficient == nfrc_ext_dup.film_coefficient == 26
    assert nfrc_ext.emissivity == nfrc_ext_dup.emissivity == 1
    assert nfrc_ext.radiant_temperature == nfrc_ext_dup.radiant_temperature == -18
    assert nfrc_ext.heat_flux == nfrc_ext_dup.heat_flux == 0
    assert nfrc_ext.relative_humidity == nfrc_ext_dup.relative_humidity == 0.5


def test_extract_all_from_xml_file():
    """Test the initialization of conditions from a file."""
    lbnl_con_file = './tests/assets/xml/BoundaryConditionsSteadyState.xml'
    conditions = ComprehensiveCondition.extract_all_from_xml_file(lbnl_con_file)

    assert len(conditions) == 9
    for con in conditions:
        assert isinstance(con, ComprehensiveCondition)
