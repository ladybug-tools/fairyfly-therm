"""Fairyfly_therm configurations.

Import this into every module where access configurations are needed.

Usage:

.. code-block:: python

    from fairyfly_therm.config import folders
    print(folders.lbnl_data_path)
    folders.lbnl_data_path = "C:/Users/Person/LBNL"
"""
import os
import json
import ladybug.config as lb_config


class Folders(object):
    """Fairyfly_therm folders.

    Args:
        config_file: The path to the config.json file from which folders are loaded.
            If None, the config.json module included in this package will be used.
            Default: None.
        mute: If False, the paths to the various folders will be printed as they
            are found. If True, no printing will occur upon initialization of this
            class. Default: True.

    Properties:
        * therm_path
        * therm_exe
        * therm_version
        * therm_version_str
        * lbnl_data_path
        * therm_settings_path
        * therm_lib_path
        * material_lib_file
        * gas_lib_file
        * bc_steady_state_lib_file
        * config_file
        * mute
    """
    THERM_VERSION = (8, 1, 30)

    def __init__(self, config_file=None, mute=True):
        self.mute = bool(mute)  # set the mute value
        self.config_file = config_file  # load paths from the config JSON file

    @property
    def therm_path(self):
        """Get or set the path to Therm installation folder.

        This is typically the folder within the lbnl program files directory
        that starts with THERM and contains executables and dlls.
        """
        return self._therm_path

    @therm_path.setter
    def therm_path(self, t_path):
        exe_name = 'THERM{}.exe'.format(self.THERM_VERSION[0])
        if not t_path:  # check the default installation location
            t_path = self._find_therm_folder()
        therm_exe_file = os.path.join(t_path, exe_name) if t_path is not None else None

        # if the executable exists, set the variables
        if t_path and os.path.isfile(therm_exe_file):
            self._therm_path = t_path
            self._therm_exe = therm_exe_file
            self._therm_version = self.THERM_VERSION
            self._therm_version_str = '.'.join(str(i) for i in self.THERM_VERSION)
            if not self.mute:
                print("Path to Therm is set to: %s" % self._therm_path)
        else:
            if t_path:
                msg = '{} is not a valid path to a Therm installation.'.format(t_path)
                print(msg)
            self._therm_path = None
            self._therm_exe = None
            self._therm_version = None
            self._therm_version_str = None

    @property
    def therm_exe(self):
        """Get the path to Therm executable.

        Will be none if no Therm installation was found.
        """
        return self._therm_exe

    @property
    def therm_version(self):
        """Get a tuple for the version of therm (eg. (8, 1, 30)).

        This will be None if the version could not be sensed or if no Therm
        installation was found.
        """
        return self._therm_version

    @property
    def therm_version_str(self):
        """Get text for the full version of therm (eg."8.1.30").

        This will be None if the version could not be sensed or if no Therm
        installation was found.
        """
        return self._therm_version_str

    @property
    def lbnl_data_path(self):
        """Get or set the path to the folder containing the LBNL data.

        This folder typically exists under the User profile and contains sub-folders
        for all installed versions of LBNL THERM and WINDOW. The THERM sub-folder
        contains a lib sub-folder with XML files for all materials, boundary
        conditions, etc.
        """
        return self._lbnl_data_path

    @lbnl_data_path.setter
    def lbnl_data_path(self, path):
        if not path:  # check the default locations of the template library
            path = self._find_lbnl_data_folder()

        # gather all of the sub folders underneath the master folder
        if path and os.path.isdir(path):
            self._lbnl_data_path = path
            self._therm_settings_path = self._check_therm_settings(path)
            if not self.mute:
                print('Path to LBNL data is set to: {}'.format(self._lbnl_data_path))
        else:
            if path:
                msg = '{} is not a valid path to a LBNL data folder.'.format(path)
                print(msg)
            self._lbnl_data_path = None
            self._therm_settings_path = None

    @property
    def therm_settings_path(self):
        """Get the path to the .ini file with THERM settings.

        Will be None if no LBNL data folder was found.
        """
        return self._therm_settings_path

    @property
    def therm_lib_path(self):
        """Get or set the path to the folder from which therm materials are loaded.

        This might be either the official library folder within the LBNL data
        folder or a user standards within the user's standards folder.
        """
        return self._therm_lib_path

    @therm_lib_path.setter
    def therm_lib_path(self, path):
        if not path:  # check the default locations of the template library
            path = self._find_therm_lib()

        # gather all of the sub folders underneath the master folder
        if path and os.path.isdir(path):
            self._therm_lib_path = path
            self._material_lib_file = self._check_therm_lib_file(path, 'Materials.xml')
            self._gas_lib_file = self._check_therm_lib_file(path, 'Gases.xml')
            self._bc_steady_state_lib_file = self._check_therm_lib_file(
                path, 'BoundaryConditionsSteadyState')
            if not self.mute:
                print('Path to LBNL data is set to: {}'.format(self._lbnl_data_path))
        else:
            if path:
                msg = '{} is not a valid path to a LBNL data folder.'.format(path)
                print(msg)
            self._therm_lib_path = None
            self._material_lib_file = None
            self._gas_lib_file = None
            self._bc_steady_state_lib_file = None

    @property
    def material_lib_file(self):
        """Get the path to the material library file."""
        return self._material_lib_file

    @property
    def gas_lib_file(self):
        """Get the path to the gas library file."""
        return self._gas_lib_file

    @property
    def bc_steady_state_lib_file(self):
        """Get the path to the modifierset library in the standards_data_folder."""
        return self._bc_steady_state_lib_file

    @property
    def config_file(self):
        """Get or set the path to the config.json file from which folders are loaded.

        Setting this to None will result in using the config.json module included
        in this package.
        """
        return self._config_file

    @config_file.setter
    def config_file(self, cfg):
        if cfg is None:
            cfg = os.path.join(os.path.dirname(__file__), 'config.json')
        self._load_from_file(cfg)
        self._config_file = cfg

    def _load_from_file(self, file_path):
        """Set all of the the properties of this object from a config JSON file.

        Args:
            file_path: Path to a JSON file containing the file paths. A sample of this
                JSON is the config.json file within this package.
        """
        # check the default file path
        assert os.path.isfile(str(file_path)), \
            ValueError('No file found at {}'.format(file_path))

        # set the default paths to be all blank
        default_path = {
            "therm_path": r'',
            "lbnl_data_path": r'',
            "therm_lib_path": r''
        }

        with open(file_path, 'r') as cfg:
            try:
                paths = json.load(cfg)
            except Exception as e:
                print('Failed to load paths from {}.\n{}'.format(file_path, e))
            else:
                for key, p in paths.items():
                    if not key.startswith('__') and p.strip():
                        default_path[key] = p.strip()

        # set paths for therm installations
        self.therm_path = default_path["therm_path"]
        self.lbnl_data_path = default_path["lbnl_data_path"]
        self.therm_lib_path = default_path["therm_lib_path"]

    @staticmethod
    def _find_therm_folder():
        """Find the Therm installation in its default location.

        This method will first attempt to return the path of a standalone Therm
        installation.

        Returns:
            File directory and full path to executable in case of success.
            None, None in case of failure.
        """
        # first check if there's a version installed in the ladybug_tools folder
        # note that this option is not likely to be used because of the THERM license
        lb_install = lb_config.folders.ladybug_tools_folder
        thm_path = None
        if os.path.isdir(lb_install):
            test_path = os.path.join(lb_install, 'THERM')
            thm_path = test_path if os.path.isdir(test_path) else None

        # then check for the default location where standalone Therm is installed
        if thm_path is not None:
            pass  # we found a version of therm in the ladybug_tools folder
        elif os.name == 'nt':  # search the C:/ drive on Windows
            major, minor, _ = Folders.THERM_VERSION
            test_path = 'C:/Program Files (x86)/lbnl/THERM{}.{}'.format(major, minor)
            thm_path = test_path if os.path.isdir(test_path) else None

        return thm_path

    @staticmethod
    def _find_lbnl_data_folder():
        """Find the the LBNL data folder in its default location."""
        # then check the default location where the LBNL installer puts it
        lib_folder = None
        if os.name == 'nt':  # search the C:/ drive on Windows
            test_path = 'C:/Users/Public/LBNL/'
            if os.path.isdir(test_path):
                lib_folder = test_path
        return lib_folder

    @staticmethod
    def _check_therm_settings(path):
        """Check that a settings file exists within the LBNL data folder."""
        if not path:  # first check that a path exists
            return None
        major, minor, _ = Folders.THERM_VERSION
        settings_dir = os.path.join(path, 'Settings')
        set_file = os.path.join(settings_dir, 'therm{}.{}.ini'.format(major, minor))
        if os.path.isfile(set_file):
            return set_file

    @staticmethod
    def _find_therm_lib():
        """Find the the LBNL data folder in its default location."""
        # first check if there's a user-defined folder in AppData
        app_folder = os.getenv('APPDATA')
        if app_folder is not None:
            lib_folder = os.path.join(app_folder, 'ladybug_tools', 'standards', 'therm')
            if os.path.isdir(lib_folder):
                return lib_folder

        # then check the default location where the LBNL installer puts it
        lib_folder = None
        if os.name == 'nt':  # search the C:/ drive on Windows
            major, minor, _ = Folders.THERM_VERSION
            test_path = 'C:/Users/Public/LBNL/THERM{}.{}/lib'.format(major, minor)
            if os.path.isdir(test_path):
                lib_folder = test_path
        return lib_folder

    @staticmethod
    def _check_therm_lib_file(path, lib_file):
        """Check that a boundary conditions XML file exists within the therm library."""
        if not path:  # first check that a path exists
            return None
        lib_path = os.path.join(path, lib_file)
        if os.path.isfile(lib_path):
            return lib_path


"""Object possesing all key folders within the configuration."""
folders = Folders(mute=True)
