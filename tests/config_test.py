# coding=utf-8
from fairyfly_therm.config import folders


def test_config_init():
    """Test the initialization of the config module and basic properties."""
    assert hasattr(folders, 'therm_path')
    assert folders.therm_path is None or isinstance(folders.therm_path, str)
    assert hasattr(folders, 'therm_exe')
    assert folders.therm_exe is None or isinstance(folders.therm_exe, str)
    assert hasattr(folders, 'therm_version')
    assert folders.therm_version is None or isinstance(folders.therm_version, tuple)

    assert hasattr(folders, 'lbnl_data_path')
    assert folders.lbnl_data_path is None or isinstance(folders.lbnl_data_path, str)
    assert hasattr(folders, 'therm_settings_path')
    assert folders.therm_settings_path is None or isinstance(folders.therm_settings_path, str)
    assert hasattr(folders, 'therm_lib_path')
    assert folders.therm_lib_path is None or isinstance(folders.therm_lib_path, str)
    assert hasattr(folders, 'material_lib_file')
    assert folders.material_lib_file is None or isinstance(folders.material_lib_file, str)
    assert hasattr(folders, 'bc_steady_state_lib_file')
    assert folders.bc_steady_state_lib_file is None or isinstance(folders.bc_steady_state_lib_file, str)

    assert isinstance(folders.config_file, str)
