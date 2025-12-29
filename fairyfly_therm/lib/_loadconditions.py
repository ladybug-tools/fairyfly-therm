"""Load all conditions from the LBNL XML files and JSON libraries."""
import os
import json

from fairyfly_therm.config import folders
from fairyfly_therm.condition.comprehensive import ComprehensiveCondition

# empty dictionaries to hold loaded conditions
_conditions = {}

# ensure that there is always a generic indoor and outdoor conditions
exterior_dict = {
    'type': 'ComprehensiveCondition',
    'identifier': 'de5cfad3-8a58-48b7-8583-b31a2650bc80',
    'temperature': -18.0,
    'film_coefficient': 26.0,
    'display_name': 'Generic Exterior',
    'protected': True,
    'color': '#0080c0'
}
exterior = ComprehensiveCondition.from_dict(exterior_dict)
exterior.lock()
_conditions[exterior.display_name] = exterior

interior_dict = {
    'type': 'ComprehensiveCondition',
    'identifier': '7eba559e-ebbc-4dc4-82a7-266a888fe5a5',
    'temperature': 21.0,
    'film_coefficient': 3.12,
    'display_name': 'Generic Interior',
    'protected': True,
    'color': '#ff8040'
}
interior = ComprehensiveCondition.from_dict(interior_dict)
interior.lock()
_conditions[interior.display_name] = interior


# load the conditions from the LBNL library if they exist
if folders.bc_steady_state_lib_file is not None:
    conds = ComprehensiveCondition.extract_all_from_xml_file(folders.bc_steady_state_lib_file)
    for con in conds:
        con.lock()
        _conditions[con.display_name] = con


def check_and_add_condition(con):
    """Check that a condition is not overwriting a default and add it."""
    con.lock()
    if con.display_name not in ('Generic Exterior', 'Generic Interior'):
        if isinstance(con, ComprehensiveCondition):
            _conditions[con.display_name] = con


def load_conditions_from_folder(lib_folder):
    """Load all of the condition objects from a therm standards folder.

    Args:
        lib_folder: Path to a sub-folder within a honeybee standards folder.
    """
    for f in os.listdir(lib_folder):
        f_path = os.path.join(lib_folder, f)
        if os.path.isfile(f_path):
            if f_path.endswith('.xml'):
                conds = ComprehensiveCondition.extract_all_from_xml_file(f_path)
                for c in conds:
                    check_and_add_condition(c)
            elif f_path.endswith('.json'):
                with open(f_path) as json_file:
                    data = json.load(json_file)
                if 'type' in data:  # single object
                    if data['type'] == 'ComprehensiveCondition':
                        check_and_add_condition(ComprehensiveCondition.from_dict(data))
                else:  # a collection of several objects
                    for m_id in data:
                        try:
                            m_dict = data[m_id]
                            if m_dict['type'] == 'ComprehensiveCondition':
                                check_and_add_condition(
                                    ComprehensiveCondition.from_dict(m_dict))
                        except (TypeError, KeyError):
                            pass  # not an acceptable JSON; possibly a comment


# load therm gases from a user folder if we are not using the official THERM lib
if folders.therm_lib_path is not None:
    load_conditions_from_folder(folders.therm_lib_path)
