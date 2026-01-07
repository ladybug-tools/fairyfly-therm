"""Test cli modules."""
from click.testing import CliRunner
import os

from ladybug.futil import nukedir
from fairyfly.config import folders as ff_folders
from fairyfly_therm.config import folders
from fairyfly_therm.cli.translate import model_to_thmz_cli
from fairyfly_therm.cli.simulate import simulate_model_cli


def test_model_to_thmz():
    """Test the CLI translation to THMZ."""
    runner = CliRunner()
    input_model = './tests/assets/json/TestModel.ffjson'

    result = runner.invoke(model_to_thmz_cli, [input_model])
    assert result.exit_code == 0

    output_model = './tests/assets/json/TestModel.thmz'
    result = runner.invoke(
        model_to_thmz_cli, [input_model, '--output-file', output_model])
    assert result.exit_code == 0
    assert os.path.isfile(output_model)
    os.remove(output_model)


def test_simulate_model():
    """Test the CLI simulation in THERM."""
    if folders.therm_exe is not None:
        runner = CliRunner()
        input_model = './tests/assets/json/TestModel.ffjson'

        folder = os.path.join(ff_folders.default_simulation_folder, 'test_wall_assembly')
        result = runner.invoke(simulate_model_cli, [input_model, '--folder', folder])
        assert result.exit_code == 0

        output_thmz = os.path.join(folder, 'model.thmz')
        assert os.path.isfile(output_thmz)
        nukedir(folder)
