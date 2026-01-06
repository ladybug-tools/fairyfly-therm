# coding=utf-8
"""Tests the fairyfly_therm run module."""
import os

from ladybug.futil import nukedir
from fairyfly.model import Model
from fairyfly_therm.lib.materials import concrete, air_cavity
from fairyfly_therm.lib.conditions import exterior
from fairyfly_therm.condition import SteadyState
from fairyfly_therm.config import folders
from fairyfly_therm.run import run_model


def test_run_model():
    """Test the run_model method."""
    if folders.therm_exe is not None:
        model = Model.from_layers([100, 200, 100], height=200)
        interior_warm = SteadyState(26, 3.2)
        interior_warm.display_name = 'Warm Interior'
        model.shapes[0].properties.therm.material = concrete
        model.shapes[1].properties.therm.material = air_cavity
        model.shapes[2].properties.therm.material = concrete
        model.boundaries[0].properties.therm.condition = exterior
        model.boundaries[1].properties.therm.condition = interior_warm
        model.boundaries[1].properties.therm.u_factor_tag = 'Wall Assembly'

        sim_dir = './tests/assets/test_sim'
        result_file = run_model(model, sim_dir)

        assert os.path.isfile(result_file)
        nukedir(sim_dir)
