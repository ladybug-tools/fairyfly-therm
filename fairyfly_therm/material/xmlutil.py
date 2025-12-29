# coding=utf-8
"""Utilities to convert THERM XML files to Material objects."""
from __future__ import division
import xml.etree.ElementTree as ET

from .solid import SolidMaterial
from .cavity import CavityMaterial


def extract_all_materials_from_xml_file(xml_file, gases=None):
    """Extract all Material objects from a THERM XML file.

    Args:
        xml_file: A path to an XML file containing objects Material objects.
        gases: A dictionary with gas names as keys and Gas object instances
            as values. These will be used to reassign the gas that fills
            cavity materials. If None, only solid materials are extracted.

    Returns:
        A tuple with two elements

        -   solid_materials: A list of all SolidMaterial objects in the XML
            file as fairyfly_therm SolidMaterial objects.

        -   cavity_materials: A list of all CavityMaterial objects in the XML
            file as fairyfly_therm CavityMaterial objects.
    """
    # read the file and get the root
    tree = ET.parse(xml_file)
    root = tree.getroot()
    # extract all of the objects
    solid_materials, cavity_materials = [], []
    for mat_obj in root:
        if mat_obj.find('Solid') is not None:
            solid_materials.append(SolidMaterial.from_therm_xml(mat_obj))
            try:
                solid_materials.append(SolidMaterial.from_therm_xml(mat_obj))
            except Exception:  # not a valid solid material
                pass
        elif mat_obj.find('Cavity') is not None and gases is not None:
            try:
                cavity_materials.append(CavityMaterial.from_therm_xml(mat_obj, gases))
            except Exception:  # not a valid cavity material
                pass
    return solid_materials, cavity_materials
