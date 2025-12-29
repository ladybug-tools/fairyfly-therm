# coding=utf-8
"""Methods to write Honeybee core objects to dsbXML."""
import os
import math
import datetime
import xml.etree.ElementTree as ET

from ladybug_geometry.geometry3d import Vector3D, Face3D

HANDLE_COUNTER = 1  # counter used to generate unique handles when necessary


def shade_to_therm_xml_element(shade, building_element=None):
    """Generate an dsbXML Plane Element object from a honeybee Shade.

    Args:
        shade: A honeybee Shade for which an dsbXML Plane Element object will
            be returned.
        building_element: An optional XML Element for the Building to which the
            generated plane object will be added. If None, a new XML Element
            will be generated. Note that this Building element should have a
            Planes tag already created within it.
    """
    # create the Plane element
    if building_element is not None:
        planes_element = building_element.find('Planes')
        xml_shade = ET.SubElement(planes_element, 'Plane', type='2')
    else:
        xml_shade = ET.Element('Plane', type='2')
    # add the vertices for the geometry
    xml_geo = ET.SubElement(xml_shade, 'Polygon', auxiliaryType='-1')
    _object_ids(xml_geo, shade.identifier, '0')
    xml_sub_pts = ET.SubElement(xml_geo, 'Vertices')
    for pt in shade.geometry.boundary:
        xml_point = ET.SubElement(xml_sub_pts, 'Point3D')
        xml_point.text = '{}; {}; {}'.format(pt.x, pt.y, pt.z)
    xml_holes = ET.SubElement(xml_geo, 'PolygonHoles')
    if shade.geometry.has_holes:
        flip_plane = shade.geometry.plane.flip()  # flip to make holes clockwise
        for hole in shade.geometry.holes:
            hole_face = Face3D(hole, plane=flip_plane)
            xml_sub_hole = ET.SubElement(xml_holes, 'PolygonHole')
            _object_ids(xml_geo, shade.identifier, '0')
            xml_sub_hole_pts = ET.SubElement(xml_sub_hole, 'Vertices')
            for pt in hole_face:
                xml_point = ET.SubElement(xml_sub_hole_pts, 'Point3D')
                xml_point.text = '{}; {}; {}'.format(pt.x, pt.y, pt.z)
    # add the name of the shade
    xml_shd_attr = ET.SubElement(xml_shade, 'Attributes')
    xml_shd_name = ET.SubElement(xml_shd_attr, 'Attribute', key='Title')
    xml_shd_name.text = str(shade.display_name)
    return xml_shade


def shade_mesh_to_therm_xml_element(shade_mesh, building_element=None, reset_counter=True):
    """Generate an dsbXML Planes Element object from a honeybee ShadeMesh.

    Args:
        shade_mesh: A honeybee ShadeMesh for which an dsbXML Planes Element
            object will be returned.
        building_element: An optional XML Element for the Building to which the
            generated objects will be added. If None, a new XML Element
            will be generated. Note that this Building element should have a
            Planes tag already created within it.
        reset_counter: A boolean to note whether the global counter for unique
            handles should be reset after the method is run. (Default: True).
    """
    global HANDLE_COUNTER  # declare that we will edit the global variable
    # create the Planes element
    xml_planes = building_element.find('Planes') \
        if building_element is not None else ET.Element('Planes')
    # add a plane element for each mesh face
    for i, face in enumerate(shade_mesh.geometry.face_vertices):
        xml_shade = ET.SubElement(xml_planes, 'Plane', type='2')
        xml_geo = ET.SubElement(xml_shade, 'Polygon', auxiliaryType='-1')
        _object_ids(xml_geo, str(HANDLE_COUNTER), '0')
        HANDLE_COUNTER += 1
        xml_sub_pts = ET.SubElement(xml_geo, 'Vertices')
        for pt in face:
            xml_point = ET.SubElement(xml_sub_pts, 'Point3D')
            xml_point.text = '{}; {}; {}'.format(pt.x, pt.y, pt.z)
        ET.SubElement(xml_geo, 'PolygonHoles')
        # add the name of the shade
        xml_shd_attr = ET.SubElement(xml_shade, 'Attributes')
        xml_shd_name = ET.SubElement(xml_shd_attr, 'Attribute', key='Title')
        xml_shd_name.text = '{} {}'.format(shade_mesh.display_name, i)
    if reset_counter:  # reset the counter back to 1 if requested
        HANDLE_COUNTER = 1
    return xml_planes


def model_to_therm_xml(model, xml_template='Default'):
    """Generate an dsbXML Element object for a honeybee Model.

    The resulting Element has all geometry (Rooms, Faces, Apertures, Doors, Shades).

    Args:
        model: A honeybee Model for which an dsbXML ElementTree object will be returned.
        xml_template: Text for the type of template file to be used to write the
            dsbXML. Different templates contain different amounts of default
            assembly library data, which may be needed in order to import the
            dsbXML into older versions of DesignBuilder. However, this data can
            greatly increase the size of the resulting dsbXML file. Choose from
            the following options.

            * Default - a minimal file that imports into the latest versions
            * Assembly - the Default plus an AssemblyLibrary with typical objects
            * Full - a large file with all libraries that can be imported to version 7.3
    """
    global HANDLE_COUNTER  # declare that we will edit the global variable
    # duplicate model to avoid mutating it as we edit it for INP export
    original_model = model
    model = model.duplicate()
    # scale the model if the units are not feet
    if model.units != 'Meters':
        model.convert_to_units('Meters')
    # remove degenerate geometry within DesignBuilder native tolerance
    try:
        model.remove_degenerate_geometry(0.01)
    except ValueError:
        error = 'Failed to remove degenerate Rooms.\nYour Model units system is: {}. ' \
            'Is this correct?'.format(original_model.units)
        raise ValueError(error)
    # auto-assign stories if there are none since these are needed for blocks
    if len(model.stories) == 0 and len(model.rooms) != 0:
        model.assign_stories_by_floor_height(min_difference=2.0)
    # erase room user data and use it to store attributes for later
    for room in model.rooms:
        room.user_data = {'__identifier__': room.identifier}
    # reassign types for horizontal faces; remove any AirBoundaries that are not walls
    z_axis = Vector3D(0, 0, 1)
    for face in model.faces:
        angle = math.degrees(z_axis.angle(face.normal))
        if angle < 60:
            face.type = face_types.roof_ceiling
        elif angle >= 130:
            face.type = face_types.floor

    # set up the ElementTree for the XML
    package_dir = os.path.dirname(os.path.abspath(__file__))
    template_file = os.path.join(package_dir, '_templates', '{}.xml'.format(xml_template))
    xml_tree = ET.parse(template_file)
    xml_root = xml_tree.getroot()
    model_name = clean_string(model.display_name)
    xml_root.set('name', '~{}'.format(model_name))
    xml_root.set('date', str(datetime.date.today()))
    xml_root.set('version', DESIGNBUILDER_VERSION)

    # add the site and the building
    xml_site = xml_root.find('Site')
    xml_bldgs = xml_site.find('Buildings')
    xml_bldg = xml_bldgs.find('Building')

    # group the model rooms by story and connected volume so they translate to blocks
    block_rooms, block_names = [], []
    story_rooms, story_names, _ = Room.group_by_story(model.rooms)
    for flr_rooms, flr_name in zip(story_rooms, story_names):
        adj_rooms = Room.group_by_adjacency(flr_rooms)
        if len(adj_rooms) == 1:
            block_rooms.append(flr_rooms)
            block_names.append(flr_name)
        else:
            for i, adj_group in enumerate(adj_rooms):
                block_rooms.append(adj_group)
                block_names.append('{} {}'.format(flr_name, i + 1))

    # give unique integers to each of the building blocks and faces
    HANDLE_COUNTER = len(block_rooms) + 2
    # convert identifiers to integers as this is the only ID format used by DesignBuilder
    HANDLE_COUNTER = model.reset_ids_to_integers(start_integer=HANDLE_COUNTER)
    HANDLE_COUNTER += 1

    # translate each block to dsbXML; including all geometry
    f_index_map = {}  # create a map between the face handle the face index
    xml_blocks = ET.SubElement(xml_bldg, 'BuildingBlocks')
    for i, (room_group, block_name) in enumerate(zip(block_rooms, block_names)):
        room_group_to_therm_xml_block(
            room_group, i + 2, xml_bldg, block_name, reset_counter=False
        )
        for room in room_group:
            for f in room:
                f_index_map[f.identifier] = f.user_data['dsb_face_i']

    # replace the face handle in the zone XML with the face index
    for xml_block in xml_blocks:
        xml_zones = xml_block.find('Zones')
        for xml_zone in xml_zones:
            xml_zone_body = xml_zone.find('Body')
            for xml_srf in xml_zone_body.find('Surfaces'):
                xml_adjs = xml_srf.find('Adjacencies')
                for xml_adj in xml_adjs:
                    xml_adj_obj_ids = xml_adj.find('ObjectIDs')
                    xml_adj_face_id = xml_adj_obj_ids.get('surfaceIndex')
                    if xml_adj_face_id != '-1':
                        try:
                            xml_adj_obj_ids.set(
                                'surfaceIndex', f_index_map[xml_adj_face_id])
                        except KeyError:  # invalid adjacency; remove the adjacency
                            xml_adj_obj_ids.set('surfaceIndex', '-1')
                            xml_adj_obj_ids.set('zoneHandle', '-1')

    # translate all of the shade geometries into the Planes section
    for shade in model.shades:
        shade_to_therm_xml_element(shade, xml_bldg)
    for shade_mesh in model.shade_meshes:
        shade_mesh.triangulate_and_remove_degenerate_faces(model.tolerance)
        shade_mesh_to_therm_xml_element(shade_mesh, xml_bldg, reset_counter=False)

    # set the handle of the site to the last index and reset the counter
    xml_site.set('handle', '1')
    HANDLE_COUNTER = 1

    return xml_root


def model_to_therm_xml(model, xml_template='Default', program_name=None):
    """Generate an dsbXML string for a Model.

    The resulting string will include all geometry (Rooms, Faces, Apertures,
    Doors, Shades), all fully-detailed constructions + materials, all fully-detailed
    schedules, and the room properties. It will also include the simulation
    parameters. Essentially, the string includes everything needed to simulate
    the model.

    Args:
        model: A honeybee Model for which an dsbXML text string will be returned.
        xml_template: Text for the type of template file to be used to write the
            dsbXML. Different templates contain different amounts of default
            assembly library data, which may be needed in order to import the
            dsbXML into older versions of DesignBuilder. However, this data can
            greatly increase the size of the resulting dsbXML file. Choose from
            the following options.

            * Default - a minimal file that imports into the latest versions
            * Assembly - the Default plus an AssemblyLibrary with typical objects
            * Full - a large file with all libraries that can be imported to version 7.3

        program_name: Optional text to set the name of the software that will
            appear under a comment in the XML to identify where it is being exported
            from. This can be set things like "Ladybug Tools" or "Pollination"
            or some other software in which this dsbXML export capability is being
            run. If None, no comment will appear. (Default: None).

    Usage:

    .. code-block:: python

        import os
        from honeybee.model import Model
        from honeybee.room import Room
        from honeybee.config import folders

        # Crate an input Model
        room = Room.from_box('Tiny House Zone', 5, 10, 3)
        room.properties.energy.program_type = office_program
        room.properties.energy.add_default_ideal_air()
        model = Model('Tiny House', [room])

        # create the dsbXML string for the model
        xml_str = model.to.therm_xml(model)

        # write the final string into an XML file using DesignBuilder encoding
        therm_xml = os.path.join(folders.default_simulation_folder, 'in_dsb.xml')
        with open(therm_xml, 'wb') as fp:
            fp.write(xml_str.encode('iso-8859-15'))
    """
    # create the XML string
    xml_root = model_to_therm_xml_element(model, xml_template)
    ET.indent(xml_root, '\t')
    therm_xml_str = ET.tostring(
        xml_root, encoding='unicode', xml_declaration=False
    )

    # add the declaration and a comment about the authoring program
    prog_comment = ''
    if program_name is not None:
        prog_comment = '<!--File generated by {}-->\n'.format(program_name)
    base_template = \
        '<?xml version="1.0" encoding="ISO-8859-15" standalone="yes"?>' \
        '\n{}'.format(prog_comment)
    therm_xml_str = base_template + therm_xml_str
    return therm_xml_str


def model_to_thmz(model, output_file, xml_template='Default', program_name=None):
    """Write an dsbXML file from a Honeybee Model.

    Note that this method also ensures that the resulting dsbXML file uses the
    ISO-8859-15 encoding that is used by DesignBuilder.

    Args:
        model: A honeybee Model for which an dsbXML file will be written.
        output_file: The path to the XML file that will be written from the model.
        xml_template: Text for the type of template file to be used to write the
            dsbXML. Different templates contain different amounts of default
            assembly library data, which may be needed in order to import the
            dsbXML into older versions of DesignBuilder. However, this data can
            greatly increase the size of the resulting dsbXML file. Choose from
            the following options.

            * Default - a minimal file that imports into the latest versions
            * Assembly - the Default plus an AssemblyLibrary with typical objects
            * Full - a large file with all libraries that can be imported to version 7.3

        program_name: Optional text to set the name of the software that will
            appear under a comment in the XML to identify where it is being exported
            from. This can be set things like "Ladybug Tools" or "Pollination"
            or some other software in which this dsbXML export capability is being
            run. If None, no comment will appear. (Default: None).
    """
    # make sure the directory exists where the file will be written
    dir_name = os.path.dirname(os.path.abspath(output_file))
    if not os.path.isdir(dir_name):
        os.makedirs(dir_name)
    # get the string of the dsbXML file
    xml_str = model_to_therm_xml(model, xml_template, program_name)
    # write the string into the file and encode it in ISO-8859-15
    with open(output_file, 'wb') as fp:
        fp.write(xml_str.encode('iso-8859-15'))
    return output_file


def shape_to_therm_xml(shade):
    """Generate an dsbXML Plane string from a honeybee Shade.

    Args:
        shade: A honeybee Shade for which an dsbXML Plane XML string will
            be returned.
    """
    xml_root = shade_to_therm_xml_element(shade)
    ET.indent(xml_root)
    return ET.tostring(xml_root, encoding='unicode')


def boundary_to_therm_xml(shade_mesh):
    """Generate an dsbXML Planes string from a honeybee ShadeMesh.

    Args:
        shade_mesh: A honeybee ShadeMesh for which an dsbXML Planes XML string
            will be returned.
    """
    xml_root = shade_mesh_to_therm_xml_element(shade_mesh)
    ET.indent(xml_root)
    return ET.tostring(xml_root, encoding='unicode')
