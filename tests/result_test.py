# coding=utf-8
"""Tests the fairyfly_therm result module."""
from ladybug_geometry.geometry3d import Vector3D, Point3D, Plane, Mesh3D

from fairyfly_therm.result import THMZResult, UFactor


def test_thmz_load_mesh():
    """Test the loading of a Mesh3D from a THMZ result file."""
    result_file = './tests/assets/thmz/test_result.thmz'
    thmz_obj = THMZResult(result_file)

    assert isinstance(thmz_obj.plane, Plane)
    assert thmz_obj.plane.o == Point3D(-100, 300, 0)

    assert isinstance(thmz_obj.mesh, Mesh3D)
    assert len(thmz_obj.mesh.faces) == 32
    assert len(thmz_obj.mesh.vertices) == 45

    empty_file = './tests/assets/thmz/test_no_result.thmz'
    thmz_obj = THMZResult(empty_file)

    assert isinstance(thmz_obj.plane, Plane)
    assert thmz_obj.mesh is None


def test_thmz_load_mesh_results():
    """Test the loading of mesh results from a THMZ result file."""
    result_file = './tests/assets/thmz/test_result.thmz'
    thmz_obj = THMZResult(result_file)

    assert len(thmz_obj.temperatures) == 45
    for val in thmz_obj.temperatures:
        assert isinstance(val, float)
    assert len(thmz_obj.heat_fluxes) == 45
    for val in thmz_obj.heat_fluxes:
        assert isinstance(val, Vector3D)
    assert len(thmz_obj.heat_flux_magnitudes) == 45
    for val in thmz_obj.heat_flux_magnitudes:
        assert isinstance(val, float)

    empty_file = './tests/assets/thmz/test_no_result.thmz'
    thmz_obj = THMZResult(empty_file)
    assert thmz_obj.temperatures is None
    assert thmz_obj.heat_fluxes is None
    assert thmz_obj.heat_flux_magnitudes is None


def test_thmz_load_u_factor_results():
    """Test the loading of U-Factor results from a THMZ result file."""
    result_file = './tests/assets/thmz/test_result.thmz'
    thmz_obj = THMZResult(result_file)

    assert len(thmz_obj.u_factors) == 1
    for val in thmz_obj.u_factors:
        assert isinstance(val, UFactor)
    assert thmz_obj.u_factors[0].total_u_factor == 1.971534

    empty_file = './tests/assets/thmz/test_no_result.thmz'
    thmz_obj = THMZResult(empty_file)
    assert thmz_obj.u_factors is None
