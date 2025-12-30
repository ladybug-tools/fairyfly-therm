# coding=utf-8
"""Methods to write Fairyfly core objects to THERM XML and THMZ."""
import os
import xml.etree.ElementTree as ET

HANDLE_COUNTER = 1  # counter used to generate unique handles when necessary


def shape_to_therm_xml(shape, polygons_element=None, reset_counter=True):
    """Generate an THERM XML Polygon Element object from a fairyfly Shape.

    Args:
        shape: A fairyfly Shape for which an THERM XML Polygon Element object will
            be returned.
        polygons_element: An optional XML Element for the Polygons to which the
            generated Element will be added. If None, a new XML Element
            will be generated.
        reset_counter: A boolean to note whether the global counter for unique
            handles should be reset after the method is run. (Default: True).
    """
    return None


def boundary_to_therm_xml(boundary, polygons_element=None, reset_counter=True):
    """Generate an THERM XML Boundary Element object from a fairyfly Boundary.

    Args:
        boundary: A fairyfly Boundary for which an THERM XML Boundary Element
            object will be returned.
        building_element: An optional XML Element for the Boundaries to which the
            generated objects will be added. If None, a new XML Element
            will be generated.
        reset_counter: A boolean to note whether the global counter for unique
            handles should be reset after the method is run. (Default: True).
    """
    return None


def model_to_therm_xml(model):
    """Generate an THERM XML Element object for a fairyfly Model.

    The resulting Element has all geometry (Shapes and Boundaries).

    Args:
        model: A fairyfly Model for which a THERM XML ElementTree object will
            be returned.
    """
    return None


def model_to_therm_xml_str(model):
    """Generate a THERM XML string for a Model.

    The resulting Element has all geometry (Shapes and Boundaries).

    Args:
        model: A fairyfly Model for which an THERM XML text string will be returned.

    Usage:

    .. code-block:: python

        import os
        from fairyfly.model import Model
        from fairyfly.config import folders
        from fairyfly_therm.lib.materials import concrete, air_cavity
        from fairyfly_therm.lib.conditions import exterior, interior

        # Crate an input Model
        model = Model.from_layers([100, 200, 100], height=1000)
        model.shapes[0].properties.therm.material = concrete
        model.shapes[1].properties.therm.material = air_cavity
        model.shapes[2].properties.therm.material = concrete
        model.boundaries[0].properties.therm.condition = exterior
        model.boundaries[1].properties.therm.condition = interior
        model.display_name = 'Roman Bath Wall'

        # create the THERM XML string for the model
        xml_str = model.to.therm_xml(model)

        # write the final string into an XML file using DesignBuilder encoding
        therm_xml = os.path.join(folders.default_simulation_folder, 'model.xml')
        with open(therm_xml, 'wb') as fp:
            fp.write(xml_str.encode('utf-8'))
    """
    # create the XML string
    xml_root = model_to_therm_xml(model)
    try:  # try to indent the XML to make it read-able
        ET.indent(xml_root)
        return ET.tostring(xml_root, encoding='unicode')
    except AttributeError:  # we are in Python 2 and no indent is available
        return ET.tostring(xml_root)


def model_to_thmz(model, output_file):
    """Write a THERM Zip (.thmz) file from a Fairyfly Model.

    Args:
        model: A fairyfly Model for which an THERM XML file will be written.
        output_file: The path to the THMZ file that will be written from the model.
    """
    # make sure the directory exists where the file will be written
    dir_name = os.path.dirname(os.path.abspath(output_file))
    if not os.path.isdir(dir_name):
        os.makedirs(dir_name)
    # get the string of the THERM XML file
    xml_str = model_to_therm_xml_str(model)
    # write the string into file file
    with open(output_file, 'wb') as fp:
        fp.write(xml_str.encode('utf-8'))
    # write the model materials, gases, and conditions to a file
    # zip everything together
    return output_file


def shape_to_therm_xml_str(shape):
    """Generate an THERM XML string from a fairyfly Shape.

    Args:
        shape: A fairyfly Shape for which an THERM XML Polygon string will
            be returned.
    """
    xml_root = shape_to_therm_xml(shape)
    try:  # try to indent the XML to make it read-able
        ET.indent(xml_root)
        return ET.tostring(xml_root, encoding='unicode')
    except AttributeError:  # we are in Python 2 and no indent is available
        return ET.tostring(xml_root)


def boundary_to_therm_xml_str(boundary):
    """Generate an THERM XML string from a fairyfly Boundary.

    Args:
        shape_mesh: A fairyfly Boundary for which an THERM XML Boundary string
            will be returned.
    """
    xml_root = boundary_to_therm_xml(boundary)
    try:  # try to indent the XML to make it read-able
        ET.indent(xml_root)
        return ET.tostring(xml_root, encoding='unicode')
    except AttributeError:  # we are in Python 2 and no indent is available
        return ET.tostring(xml_root)
