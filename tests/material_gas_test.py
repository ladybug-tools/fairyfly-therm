# coding=utf-8
import pytest
import uuid

from fairyfly_therm.material.gas import PureGas, Gas


def test_pure_gas_init():
    """Test the initialization of a custom gas."""
    mat_id = uuid.uuid4()
    co2_gap = PureGas(0.0146, 0.000014, 827.73, identifier=mat_id)
    co2_gap.display_name = 'CO2'
    co2_gap.specific_heat_ratio = 1.4
    co2_gap.molecular_weight = 44
    str(co2_gap)  # test the string representation of the material
    co2_dup = co2_gap.duplicate()

    assert co2_gap.identifier == co2_dup.identifier == str(mat_id)
    assert co2_gap.display_name == co2_dup.display_name == 'CO2'
    assert co2_gap.conductivity == co2_dup.conductivity == pytest.approx(0.0146, rel=1e-2)
    assert co2_gap.viscosity == co2_dup.viscosity == pytest.approx(0.000014, rel=1e-2)
    assert co2_gap.specific_heat == co2_dup.specific_heat == pytest.approx(827.73, rel=1e-2)
    assert co2_gap.density == co2_dup.density == pytest.approx(1.9631, rel=1e-2)
    assert co2_gap.prandtl == co2_dup.prandtl == pytest.approx(0.7937, rel=1e-2)

    assert co2_gap.conductivity_coeff_b == 0
    assert co2_gap.conductivity_coeff_c == 0
    assert co2_gap.viscosity_coeff_b == 0
    assert co2_gap.viscosity_coeff_c == 0
    assert co2_gap.specific_heat_coeff_b == 0
    assert co2_gap.specific_heat_coeff_c == 0
    assert co2_gap.specific_heat_ratio == 1.4
    assert co2_gap.molecular_weight == 44


def test_pure_gas_properties_at_temperature():
    """Test the initialization of gas material objects and basic properties."""
    mat_id = uuid.uuid4()
    co2_gap = PureGas(0.0146, 0.000014, 827.73, identifier=mat_id)
    co2_gap.display_name = 'CO2'
    co2_gap.specific_heat_ratio = 1.4
    co2_gap.molecular_weight = 44

    assert co2_gap.conductivity_at_temperature(223) == pytest.approx(0.0146, rel=1e-2)
    assert co2_gap.viscosity_at_temperature(223) == pytest.approx(1.4e-05, rel=1e-2)
    assert co2_gap.specific_heat_at_temperature(223) == pytest.approx(827.73, rel=1e-2)
    assert co2_gap.density_at_temperature(223) == pytest.approx(2.40466, rel=1e-2)
    assert co2_gap.prandtl_at_temperature(223) == pytest.approx(0.7937, rel=1e-2)


def test_pure_gas_to_from_xml():
    """Test the initialization of PureGas objects from XML elements."""
    mat_id = uuid.uuid4()
    co2_gap = PureGas(0.0146, 0.000014, 827.73, identifier=mat_id)
    co2_gap.display_name = 'CO2'
    co2_gap.specific_heat_ratio = 1.4
    co2_gap.molecular_weight = 44
    xml_mat = co2_gap.to_therm_xml_str()
    co2_dup = PureGas.from_therm_xml_str(xml_mat)

    assert co2_gap == co2_dup
    assert co2_gap.identifier == co2_dup.identifier == str(mat_id)
    assert co2_gap.display_name == co2_dup.display_name == 'CO2'
    assert co2_gap.conductivity == co2_dup.conductivity == pytest.approx(0.0146, rel=1e-2)
    assert co2_gap.viscosity == co2_dup.viscosity == pytest.approx(0.000014, rel=1e-2)
    assert co2_gap.specific_heat == co2_dup.specific_heat == pytest.approx(827.73, rel=1e-2)
    assert co2_gap.density == co2_dup.density == pytest.approx(1.9631, rel=1e-2)
    assert co2_gap.prandtl == co2_dup.prandtl == pytest.approx(0.7937, rel=1e-2)


def test_pure_gas_dict_methods():
    """Test the to/from dict methods."""
    mat_id = uuid.uuid4()
    co2_gap = PureGas(0.0146, 0.000014, 827.73, identifier=mat_id)
    co2_gap.display_name = 'CO2'
    co2_gap.specific_heat_ratio = 1.4
    co2_gap.molecular_weight = 44

    material_dict = co2_gap.to_dict()
    co2_dup = PureGas.from_dict(material_dict)
    assert material_dict == co2_dup.to_dict()
    assert co2_gap == co2_dup
    assert co2_gap.identifier == co2_dup.identifier == str(mat_id)
    assert co2_gap.display_name == co2_dup.display_name == 'CO2'
    assert co2_gap.identifier == co2_dup.identifier == str(mat_id)
    assert co2_gap.display_name == co2_dup.display_name == 'CO2'
    assert co2_gap.conductivity == co2_dup.conductivity == pytest.approx(0.0146, rel=1e-2)
    assert co2_gap.viscosity == co2_dup.viscosity == pytest.approx(0.000014, rel=1e-2)
    assert co2_gap.specific_heat == co2_dup.specific_heat == pytest.approx(827.73, rel=1e-2)
    assert co2_gap.density == co2_dup.density == pytest.approx(1.9631, rel=1e-2)
    assert co2_gap.prandtl == co2_dup.prandtl == pytest.approx(0.7937, rel=1e-2)


def test_gas_init():
    """Test the initialization of a gas mixture."""
    gas_id = uuid.uuid4()
    co2_gap = PureGas(0.0146, 0.000014, 827.73)
    co2_gap.specific_heat_ratio = 1.4
    co2_gap.molecular_weight = 44
    co2 = Gas([co2_gap], [1], identifier=gas_id)
    co2.display_name = 'CO2'
    str(co2)  # test the string representation of the material
    co2_dup = co2.duplicate()

    assert co2.identifier == co2_dup.identifier == str(gas_id)
    assert co2.display_name == co2_dup.display_name == 'CO2'
    assert co2.conductivity == co2_dup.conductivity == pytest.approx(0.0146, rel=1e-2)
    assert co2.viscosity == co2_dup.viscosity == pytest.approx(0.000014, rel=1e-2)
    assert co2.specific_heat == co2_dup.specific_heat == pytest.approx(827.73, rel=1e-2)
    assert co2.density == co2_dup.density == pytest.approx(1.9631, rel=1e-2)
    assert co2.prandtl == co2_dup.prandtl == pytest.approx(0.7937, rel=1e-2)


def test_gas_mixture_init():
    """Test the initialization of a gas mixture."""
    air_dict = {
        "type": "PureGas",
        "identifier": "8d33196f-f052-46e6-8353-bccb9a779f9c",
        "conductivity_coeff_a": 0.002873,
        "viscosity_coeff_a": 3.723e-06,
        "specific_heat_coeff_a": 1002.737,
        "conductivity_coeff_b": 7.76e-05,
        "viscosity_coeff_b": 4.94e-08,
        "specific_heat_coeff_b": 0.012324,
        "conductivity_coeff_c": 0.0,
        "viscosity_coeff_c": 0.0,
        "specific_heat_coeff_c": 0.0,
        "specific_heat_ratio": 1.4,
        "molecular_weight": 28.97,
        "display_name": "Air",
        "protected": True,
        "color": "#556d11"
    }
    argon_dict = {
        "type": "PureGas",
        "identifier": "444d94e4-326e-4c1c-aef1-666771b569cd",
        "conductivity_coeff_a": 0.002285,
        "viscosity_coeff_a": 3.379e-06,
        "specific_heat_coeff_a": 521.9285,
        "conductivity_coeff_b": 5.149e-05,
        "viscosity_coeff_b": 6.451e-08,
        "specific_heat_coeff_b": 0.0,
        "conductivity_coeff_c": 0.0,
        "viscosity_coeff_c": 0.0,
        "specific_heat_coeff_c": 0.0,
        "specific_heat_ratio": 1.67,
        "molecular_weight": 39.948,
        "display_name": "Argon",
        "protected": True,
        "color": "#4a6eed"
    }
    air = PureGas.from_dict(air_dict)
    argon = PureGas.from_dict(argon_dict)
    gas_id = uuid.uuid4()
    air_argon = Gas([argon, air], (0.9, 0.1), identifier=gas_id)
    air_argon.display_name = 'Air/Argon Mixture'
    aa_dup = air_argon.duplicate()

    assert air_argon.pure_gases == (argon, air)
    assert air_argon.gas_fractions == (0.9, 0.1)
    assert air_argon.display_name == aa_dup.display_name == 'Air/Argon Mixture'
    assert air_argon.conductivity == aa_dup.conductivity == pytest.approx(0.0171, rel=1e-2)
    assert air_argon.viscosity == aa_dup.viscosity == pytest.approx(2.062157685e-05, rel=1e-2)
    assert air_argon.specific_heat == aa_dup.specific_heat == pytest.approx(570.346, rel=1e-2)
    assert air_argon.density == aa_dup.density == pytest.approx(1.733399, rel=1e-2)
    assert air_argon.prandtl == aa_dup.prandtl == pytest.approx(0.6869399, rel=1e-2)

    with pytest.raises(AssertionError):
        air_argon.gas_fractions = (0.5, 0.7)


def test_gas_dict_methods():
    """Test the to/from dict methods."""
    gas_id = uuid.uuid4()
    co2_gap = PureGas(0.0146, 0.000014, 827.73)
    co2_gap.specific_heat_ratio = 1.4
    co2_gap.molecular_weight = 44
    co2 = Gas([co2_gap], [1], identifier=gas_id)
    co2.display_name = 'CO2'

    material_dict = co2.to_dict()
    co2_dup = Gas.from_dict(material_dict)
    assert material_dict == co2_dup.to_dict()

    assert co2 == co2_dup
    assert co2.identifier == co2_dup.identifier == str(gas_id)
    assert co2.display_name == co2_dup.display_name == 'CO2'
    assert co2.conductivity == co2_dup.conductivity == pytest.approx(0.0146, rel=1e-2)
    assert co2.viscosity == co2_dup.viscosity == pytest.approx(0.000014, rel=1e-2)
    assert co2.specific_heat == co2_dup.specific_heat == pytest.approx(827.73, rel=1e-2)
    assert co2.density == co2_dup.density == pytest.approx(1.9631, rel=1e-2)
    assert co2.prandtl == co2_dup.prandtl == pytest.approx(0.7937, rel=1e-2)


def test_gas_to_from_xml():
    """Test the initialization of Gas objects from XML elements."""
    mat_id = uuid.uuid4()
    co2_gap = PureGas(0.0146, 0.000014, 827.73, identifier=mat_id)
    co2_gap.display_name = 'Pure CO2'
    co2_gap.specific_heat_ratio = 1.4
    co2_gap.molecular_weight = 44
    gas_id = uuid.uuid4()
    co2 = Gas([co2_gap], [1], identifier=gas_id)
    co2.display_name = 'CO2'
    xml_mat = co2.to_therm_xml_str()
    co2_dup = Gas.from_therm_xml_str(xml_mat, {co2_gap.display_name: co2_gap})

    assert co2 == co2_dup
    assert co2.identifier == co2_dup.identifier == str(gas_id)
    assert co2.display_name == co2_dup.display_name == 'CO2'
    assert co2.conductivity == co2_dup.conductivity == pytest.approx(0.0146, rel=1e-2)
    assert co2.viscosity == co2_dup.viscosity == pytest.approx(0.000014, rel=1e-2)
    assert co2.specific_heat == co2_dup.specific_heat == pytest.approx(827.73, rel=1e-2)
    assert co2.density == co2_dup.density == pytest.approx(1.9631, rel=1e-2)
    assert co2.prandtl == co2_dup.prandtl == pytest.approx(0.7937, rel=1e-2)


def test_gas_mixture_init_from_xml_file():
    """Test the initialization of Gas materials from a file."""
    lbnl_gas_file = './tests/assets/xml/Gases.xml'
    gases, pure_gases = Gas.extract_all_from_xml_file(lbnl_gas_file)

    assert len(pure_gases) == 4
    for gas in pure_gases:
        assert isinstance(gas, PureGas)
    assert len(gases) == 5
    for gas in gases:
        assert isinstance(gas, Gas)
