# coding=utf-8
"""Module for running files through THERM CLI."""
from __future__ import division

import os
import subprocess

from ladybug.futil import write_to_file
from fairyfly.typing import clean_string
from fairyfly.config import folders as ff_folders
from fairyfly.model import Model
from .config import folders


def run_model(model, directory=None, silent=False, simulation_par=None):
    """Run a fairyfly Model through THERM CLI.

    Args:
        model: Path to a THMZ file to be run using THERM CLI.
        directory: The directory in which the simulation files will be written.
            If None, this will default to the fairyfly-core default_simulation_folder.
        silent: Boolean to note whether the THERM simulation should be run silently.
        simulation_par: A fairyfly-therm SimulationParameter object to specify
            how the THERM simulation should be run. If None, default simulation
            parameters will be generated. (Default: None).

    Returns:
        The path to the input thmz_file with results inside of it.
    """
    assert isinstance(model, Model), \
        'Expected Fairyfly Model. Got {}.'.format(type(model))
    # get a default directory if none was specified
    model_name = clean_string(model.display_name)
    if directory is None:
        directory = os.path.join(ff_folders.default_simulation_folder, model_name)
    thmz_file = os.path.join(directory, '{}.thmz'.format(model_name))
    log_file = os.path.join(directory, 'therm.log')
    if os.path.isdir(directory):
        for exist_file in (thmz_file, log_file):
            if os.path.isfile(exist_file):
                try:
                    os.remove(exist_file)
                except Exception:
                    print("Failed to remove %s" % exist_file)
    else:
        os.makedirs(directory)
    # write the Model to a .thmz file
    model.to_thmz(thmz_file, simulation_par)
    # run the thmz_file through THERM
    thmz_file = run_thmz(thmz_file, silent)
    # parse the log file to check if there were any failures
    with open(log_file, 'r') as lf:
        sim_log = lf.read()
    if 'Calculation complete.' not in sim_log:
        msg = 'THERM simulation failed. Open the thmz file in the THERM interface ' \
            'for more info.\n{}'.format(sim_log)
        raise ValueError(msg)
    return thmz_file


def run_thmz(thmz_file, silent=False):
    """Run a .thmz file using the THERM CLI.

    Args:
        thmz_file: Path to a THMZ file to be run using THERM CLI.
        silent: Boolean to note whether the THERM simulation should be run silently.

    Returns:
        The path to the input thmz_file with results inside of it.
    """
    # check that THERM is installed on the machine
    assert folders.therm_exe is not None, \
        'No usable THERM executable was found on the machine.'
    # check that the THMZ file exists
    thmz_file = os.path.abspath(thmz_file)
    assert os.path.isfile(thmz_file), 'No THMZ file found at {}.'.format(thmz_file)
    directory = os.path.split(thmz_file)[0]
    log_file = os.path.join(directory, 'therm.log')

    # write a batch file to call THERM CLI; useful for manually re-running the sim
    if not silent:
        working_drive = directory[:2]
        batch = '{}\n"{}" -pw thmCLA -thmz "{}" -log "{}" -calc -exit'.format(
            working_drive, folders.therm_exe, thmz_file, log_file)
        if all(ord(c) < 128 for c in batch):  # just run the batch file as it is
            batch_file = os.path.join(directory, 'run_therm.bat')
            write_to_file(batch_file, batch, True)
            os.system('"{}"'.format(batch_file))  # run the batch file
            return thmz_file

    # given .bat file restrictions with non-ASCII characters, run the sim with subprocess
    cmds = [folders.therm_exe, '-pw', 'thmCLA', '-thmz', thmz_file,
            '-log', log_file, '-calc', '-exit']
    process = subprocess.Popen(cmds, shell=silent)
    process.communicate()  # prevents the script from running before command is done

    return thmz_file
