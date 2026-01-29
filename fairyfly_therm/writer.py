# coding=utf-8
"""Methods to write Fairyfly core objects to THERM XML and THMZ."""
import os
import uuid
import random
import math
import datetime
import zipfile
import json
import tempfile
import xml.etree.ElementTree as ET

from ladybug_geometry.geometry2d import Polygon2D
from ladybug_geometry.geometry3d import Vector3D, Point3D, LineSegment3D, Plane, \
    Polyline3D, Face3D, Polyface3D
from ladybug_geometry.bounding import bounding_box
from fairyfly.typing import clean_string, therm_id_from_uuid
from fairyfly.shape import Shape
from fairyfly.boundary import Boundary

from fairyfly_therm.config import folders
from fairyfly_therm.material import CavityMaterial
from fairyfly_therm.simulation.parameter import SimulationParameter
from fairyfly_therm.lib.conditions import adiabatic, frame_cavity

HANDLE_COUNTER = 1  # counter used to generate unique handles when necessary


def shape_to_therm_xml(shape, plane=None, polygons_element=None, reset_counter=True):
    """Generate an THERM XML Polygon Element object from a fairyfly Shape.

    Args:
        shape: A fairyfly Shape for which an THERM XML Polygon Element object will
            be returned.
        plane: An optional ladybug-geometry Plane to set the 2D coordinate system
            into which the 3D Shape will be projected to THERM space. If None
            the Face3D.plane of the Shape's geometry will be used. (Default: None).
        polygons_element: An optional XML Element for the Polygons to which the
            generated Element will be added. If None, a new XML Element
            will be generated. (Default: None).
        reset_counter: A boolean to note whether the global counter for unique
            handles should be reset after the method is run. (Default: True).

    .. code-block:: xml

        <Polygon>
            <UUID>9320589a-2ee0-bab0-72c3f49441f3</UUID>
            <ID>1</ID>
            <MaterialUUID>8dd145d0-5f30-11ea-bc55-0242ac130003</MaterialUUID>
            <MaterialName>Laminated panel</MaterialName>
            <Origin>
                <x>0</x>
                <y>0</y>
            </Origin>
            <Points>
                <Point>
                    <x>181</x>
                    <y>-219</y>
                </Point>
                <Point>
                    <x>181</x>
                    <y>-371.4</y>
                </Point>
                <Point>
                    <x>200</x>
                    <y>-371.4</y>
                </Point>
                <Point>
                    <x>200</x>
                    <y>-219</y>
                </Point>
            </Points>
            <Type>Material</Type>
        </Polygon>
    """
    global HANDLE_COUNTER  # declare that we will edit the global variable
    # create a new Polygon element if one is not specified
    if polygons_element is not None:
        xml_poly = ET.SubElement(polygons_element, 'Polygon')
    else:
        xml_poly = ET.Element('Polygon')
    # add all of the required basic attributes
    xml_uuid = ET.SubElement(xml_poly, 'UUID')
    xml_uuid.text = shape.therm_uuid
    xml_id = ET.SubElement(xml_poly, 'ID')
    xml_id.text = str(HANDLE_COUNTER)
    HANDLE_COUNTER += 1
    xml_mat_id = ET.SubElement(xml_poly, 'MaterialUUID')
    shape_mat = shape.properties.therm.material
    xml_mat_id.text = shape_mat.therm_uuid \
        if isinstance(shape_mat, CavityMaterial) else shape_mat.identifier
    xml_mat_name = ET.SubElement(xml_poly, 'MaterialName')
    xml_mat_name.text = shape.properties.therm.material.display_name
    # add an origin
    xml_origin = ET.SubElement(xml_poly, 'Origin')
    for coord in ('x', 'y'):
        xml_oc = ET.SubElement(xml_origin, coord)
        xml_oc.text = '0'
    # add all of the geometry
    xml_points = ET.SubElement(xml_poly, 'Points')
    polygon = shape.geometry.polygon2d.vertices if plane is None else \
        [plane.xyz_to_xy(pt3) for pt3 in shape.geometry.vertices]
    for pt_2d in polygon:
        xml_point = ET.SubElement(xml_points, 'Point')
        xml_x = ET.SubElement(xml_point, 'x')
        xml_x.text = str(round(pt_2d.x, 1))
        xml_y = ET.SubElement(xml_point, 'y')
        xml_y.text = str(round(pt_2d.y, 1))
    # add the cavity ID if it exists
    if shape.user_data is not None and 'cavity_id' in shape.user_data:
        xml_cav_id = ET.SubElement(xml_poly, 'CavityUUID')
        xml_cav_id.text = str(shape.user_data['cavity_id'])
    # add the type of polygon
    xml_type = ET.SubElement(xml_poly, 'Type')
    xml_type.text = 'Material'
    if reset_counter:  # reset the counter back to 1 if requested
        HANDLE_COUNTER = 1
    return xml_poly


def boundary_to_therm_xml(boundary, plane=None, boundaries_element=None,
                          reset_counter=True):
    """Generate an THERM XML Boundary Element object from a fairyfly Boundary.

    Args:
        boundary: A fairyfly Boundary for which an THERM XML Boundary Element
            object will be returned.
        plane: An optional ladybug-geometry Plane to set the 2D coordinate
            system into which the 3D Boundary will be projected to THERM space.
            If None, it will be assumed that the Boundary lies in the World XY
            plane. (Default: None).
        boundaries_element: An optional XML Element for the Boundaries to which the
            generated objects will be added. If None, a new XML Element
            will be generated. (Default: None).
        reset_counter: A boolean to note whether the global counter for unique
            handles should be reset after the method is run. (Default: True).

    .. code-block:: xml

        <Boundary>
            <ID>45</ID>
            <UUID>14264c7e-1801-a3c1-0e115d8227ac</UUID>
            <Name>NFRC 100-2010 Exterior</Name>
            <FluxTag></FluxTag>
            <IsBlocking>true</IsBlocking>
            <NeighborPolygonUUID>5b9e5933-1080-4e9e-5c3b537d8230</NeighborPolygonUUID>
            <Origin>
                <x>0</x>
                <y>0</y>
            </Origin>
            <StartPoint>
                <x>235.670456</x>
                <y>-147.081726</y>
            </StartPoint>
            <EndPoint>
                <x>235.670456</x>
                <y>-297.081238</y>
            </EndPoint>
            <Side>0</Side>
            <ThermalEmissionProperties>
                <Emissivity>0.84</Emissivity>
                <Temperature>0</Temperature>
                <UseGlobalEmissivity>true</UseGlobalEmissivity>
            </ThermalEmissionProperties>
            <IsIlluminated>false</IsIlluminated>
            <EdgeID>0</EdgeID>
            <Type>Boundary Condition</Type>
            <Color>0x000000</Color>
            <Status>0</Status>
        </Boundary>
    """
    global HANDLE_COUNTER  # declare that we will edit the global variable
    # create a new Boundaries element if one is not specified
    if boundaries_element is None:
        boundaries_element = ET.Element('Boundaries')
    # determine an edge ID and color to be used for all segments in the boundary
    edge_id = str(random.randint(10000000, 99999999))
    color = boundary.properties.therm.condition.color.to_hex().replace('#', '0x')
    # loop through each of the line segments and add a Boundary element
    for i, seg in enumerate(boundary.geometry):
        # add all of the required basic attributes
        xml_bound = ET.SubElement(boundaries_element, 'Boundary')
        xml_id = ET.SubElement(xml_bound, 'ID')
        xml_id.text = str(HANDLE_COUNTER)
        HANDLE_COUNTER += 1
        xml_uuid = ET.SubElement(xml_bound, 'UUID')
        xml_uuid.text = boundary.therm_uuid[:-12] + str(uuid.uuid4())[-12:]
        xml_name = ET.SubElement(xml_bound, 'Name')
        xml_name.text = boundary.properties.therm.condition.display_name
        xml_flux = ET.SubElement(xml_bound, 'FluxTag')
        if boundary.properties.therm.u_factor_tag is not None:
            xml_flux.text = boundary.properties.therm.u_factor_tag
        xml_blocks = ET.SubElement(xml_bound, 'IsBlocking')
        xml_blocks.text = 'true'
        # add the UUIDs of the neighboring shapes
        if boundary.user_data is not None and 'adj_polys' in boundary.user_data:
            adj_ids = boundary.user_data['adj_polys'][i]
            for j, adj_id in enumerate(adj_ids):
                if j == 0:
                    xml_ajd_p = ET.SubElement(xml_bound, 'NeighborPolygonUUID')
                else:
                    xml_ajd_p = ET.SubElement(
                        xml_bound, 'NeighborPolygonUUID{}'.format(j + 1))
                xml_ajd_p.text = adj_id
        # add an origin
        xml_origin = ET.SubElement(xml_bound, 'Origin')
        for coord in ('x', 'y'):
            xml_oc = ET.SubElement(xml_origin, coord)
            xml_oc.text = '0'
        # add the boundary geometry
        pts_2d = seg.vertices if plane is None else \
            [plane.xyz_to_xy(pt3) for pt3 in seg.vertices]
        for k, pt_2d in enumerate(pts_2d):
            xml_point = ET.SubElement(xml_bound, 'StartPoint') if k == 0 else \
                ET.SubElement(xml_bound, 'EndPoint')
            xml_x = ET.SubElement(xml_point, 'x')
            xml_x.text = str(round(pt_2d.x, 1))
            xml_y = ET.SubElement(xml_point, 'y')
            xml_y.text = str(round(pt_2d.y, 1))
        # add the various thermal properties
        xml_side = ET.SubElement(xml_bound, 'Side')
        xml_side.text = '0'
        xml_e_prop = ET.SubElement(xml_bound, 'ThermalEmissionProperties')
        xml_emiss = ET.SubElement(xml_e_prop, 'Emissivity')
        if boundary.user_data is not None and 'emissivities' in boundary.user_data:
            xml_emiss.text = str(boundary.user_data['emissivities'][i])
        else:
            xml_emiss.text = '0.9'
        xml_temp = ET.SubElement(xml_e_prop, 'Temperature')
        xml_temp.text = '0'
        xml_g_emiss = ET.SubElement(xml_e_prop, 'UseGlobalEmissivity')
        xml_g_emiss.text = 'true'
        xml_is_ill = ET.SubElement(xml_bound, 'IsIlluminated')
        xml_is_ill.text = 'false'
        # add the final identifying properties
        xml_edge_id = ET.SubElement(xml_bound, 'EdgeID')
        xml_edge_id.text = edge_id
        if boundary.user_data is not None and 'enclosure_numbers' in boundary.user_data:
            xml_enclosure = ET.SubElement(xml_bound, 'EnclosureNumber')
            xml_enclosure.text = boundary.user_data['enclosure_numbers'][i]
            xml_type = ET.SubElement(xml_bound, 'Type')
            xml_type.text = 'Frame Cavity'
        else:
            xml_type = ET.SubElement(xml_bound, 'Type')
            xml_type.text = 'Boundary Condition'
        xml_color = ET.SubElement(xml_bound, 'Color')
        xml_color.text = color
        xml_status = ET.SubElement(xml_bound, 'Status')
        if boundary.user_data is not None and 'enclosure_numbers' in boundary.user_data:
            xml_status.text = '64'
        else:
            xml_status.text = '0'
    if reset_counter:  # reset the counter back to 1 if requested
        HANDLE_COUNTER = 1
    return boundaries_element


def _cavity_to_therm_xml(properties, cavities_element=None):
    """Generate an THERM XML Cavity Element object from a list of properties.

    Args:
        properties: A list of cavity properties, including emissivities and cavity area.
        cavities_element: An optional XML Element for the Cavities to which the
            generated objects will be added. If None, a new XML Element
            will be generated. (Default: None).

    .. code-block:: xml

        <Cavity>
            <UUID>adfca13b-af61-a0d7-d29f0fbefbcc</UUID>
            <HeatFlowDirection>Unknown</HeatFlowDirection>
            <Emissivity1>0.9</Emissivity1>
            <Emissivity2>0.9</Emissivity2>
            <Temperature1>7</Temperature1>
            <Temperature2>-4</Temperature2>
            <MaxXDimension>-1</MaxXDimension>
            <MaxYDimension>-1</MaxYDimension>
            <ActualHeight>1000</ActualHeight>
            <Area>3.260304e-12</Area>
            <LocalEmissivities>false</LocalEmissivities>
            <Pressure>1.013e+05</Pressure>
            <WarmLocator>
                <x>0</x>
                <y>0</y>
            </WarmLocator>
            <ColdLocator>
                <x>0</x>
                <y>0</y>
            </ColdLocator>
        </Cavity>
    """
    # create a new Cavity element if one is not specified
    if cavities_element is not None:
        xml_cav = ET.SubElement(cavities_element, 'Cavity')
    else:
        xml_cav = ET.Element('Cavity')
    # add all of the required basic attributes
    xml_uuid = ET.SubElement(xml_cav, 'UUID')
    xml_uuid.text = str(properties[0])
    xml_hfd = ET.SubElement(xml_cav, 'HeatFlowDirection')
    xml_hfd.text = 'Unknown'
    xml_e1 = ET.SubElement(xml_cav, 'Emissivity1')
    xml_e1.text = str(properties[1])
    xml_e2 = ET.SubElement(xml_cav, 'Emissivity2')
    xml_e2.text = str(properties[2])
    xml_t1 = ET.SubElement(xml_cav, 'Temperature1')
    xml_t1.text = '7'
    xml_t2 = ET.SubElement(xml_cav, 'Temperature2')
    xml_t2.text = '-4'
    xml_mx = ET.SubElement(xml_cav, 'MaxXDimension')
    xml_mx.text = '-1'
    xml_my = ET.SubElement(xml_cav, 'MaxYDimension')
    xml_my.text = '-1'
    xml_ah = ET.SubElement(xml_cav, 'ActualHeight')
    xml_ah.text = '1000'
    xml_ar = ET.SubElement(xml_cav, 'Area')
    xml_ar.text = str(properties[3])
    xml_le = ET.SubElement(xml_cav, 'LocalEmissivities')
    xml_le.text = 'true'
    xml_pressure = ET.SubElement(xml_cav, 'Pressure')
    xml_pressure.text = '1.01e+05'
    # add a warm locator
    xml_warm = ET.SubElement(xml_cav, 'WarmLocator')
    for coord in ('x', 'y'):
        xml_oc = ET.SubElement(xml_warm, coord)
        xml_oc.text = '0'
    # add a cold locator
    xml_cold = ET.SubElement(xml_cav, 'ColdLocator')
    for coord in ('x', 'y'):
        xml_oc = ET.SubElement(xml_cold, coord)
        xml_oc.text = '0'
    return xml_cav


def model_to_therm_xml(model, simulation_par=None):
    """Generate an THERM XML Element object for a fairyfly Model.

    The resulting Element has all geometry (Shapes and Boundaries).

    Args:
        model: A fairyfly Model for which a THERM XML ElementTree object will
            be returned.
        simulation_par: A fairyfly-therm SimulationParameter object to specify
            how the THERM simulation should be run. If None, default simulation
            parameters will be generated. (Default: None).
    """
    global HANDLE_COUNTER  # declare that we will edit the global variable
    # check that we have at least one shape to translate
    assert len(model.shapes) > 0, \
        'Model must have at least one Shape to translate to THERM.'
    # duplicate model to avoid mutating it as we edit it for THERM export
    original_model = model
    model = model.duplicate()
    # scale the model if the units are not millimeters
    if model.units != 'Millimeters':
        model.convert_to_units('Millimeters')
    # remove degenerate geometry within THERM native tolerance
    try:
        model.remove_duplicate_vertices(0.1)
    except ValueError:
        error = 'Failed to remove degenerate Shapes.\nYour Model units system is: {}. ' \
            'Is this correct?'.format(original_model.units)
        raise ValueError(error)

    # determine the plane and the scale to be used for all geometry translation
    ang_tol = model.angle_tolerance
    min_pt, max_pt = bounding_box([s.geometry for s in model.shapes])
    origin = Point3D(min_pt.x, max_pt.y, max_pt.z)
    normal = model.shapes[0].geometry.normal
    up_vec = math.degrees(Vector3D(0, 0, 1).angle(normal))
    if up_vec < ang_tol or up_vec > 180 - ang_tol:
        bp = Plane(o=origin)
    else:
        if normal.z < 0:
            normal = normal.reverse()
        bp = Plane(n=normal, o=origin)
    t_vec = (bp.x * -100) + (bp.y * 100)
    offset_origin = origin.move(t_vec)
    plane = Plane(n=bp.n, o=offset_origin)
    max_dim = max((max_pt.x - min_pt.x, max_pt.y - min_pt.y, max_pt.z - min_pt.z))
    scale = 1.0 if max_dim < 100 else 100 / max_dim

    # check that all geometries lie within the tolerance of the plane
    for shape in model.shapes:
        for pt in shape.vertices:
            if plane.distance_to_point(pt) > 0.1:
                msg = 'Not all of the model shapes lie in the same plane as ' \
                    'each other. Shape "{}" is out of plane by {} ' \
                    'millimeters.'.format(shape.full_id, plane.distance_to_point(pt))
                raise ValueError(msg)
    for bound in model.boundaries:
        for pt in bound.vertices:
            if plane.distance_to_point(pt) > 0.1:
                msg = 'Not all of the model boundaries lie in the same plane as ' \
                    'the shapes. Boundary "{}" is out of plane by {} ' \
                    'millimeters.'.format(bound.full_id, plane.distance_to_point(pt))
                raise ValueError(msg)

    # split any shapes that have holes in them
    split_shapes = []
    for shape in model.shapes:
        if shape.geometry.has_holes:
            for geo in shape.geometry.split_through_holes():
                new_shp = shape.duplicate()
                new_shp._geometry = geo
                new_shp.identifier = str(uuid.uuid4())
                split_shapes.append(new_shp)
        else:
            split_shapes.append(shape)
    if len(model.shapes) != split_shapes:
        model.shapes = split_shapes

    # ensure that all shapes are counterclockwise
    for shape in model.shapes:
        poly = Polygon2D(plane.xyz_to_xy(pt) for pt in shape.geometry)
        if poly.is_clockwise:
            shape._geometry = shape.geometry.flip()

    # intersect the shape geometries with one another
    Shape.intersect_adjacency(model.shapes, 0.1, plane)

    # determine if there are any Boundary points that do not share a Shape vertex
    boundary_pts = []
    for bound in model.boundaries:
        for seg in bound.geometry:
            for pt in seg.vertices:
                for o_pt in boundary_pts:
                    if pt.is_equivalent(o_pt, tolerance=0.1):
                        break
                else:  # the point is unique
                    boundary_pts.append(pt)
    orphaned_points = []
    for bpt in boundary_pts:
        matched = False
        for shape in model.shapes:
            if matched:
                break
            for spt in shape.vertices:
                if bpt.is_equivalent(spt, tolerance=0.1):
                    matched = True
                    break
        if not matched:  # a boundary point with no Shape
            orphaned_points.append(bpt)

    # insert extra vertices to the shapes if they do not align with boundary end points
    for or_pt in orphaned_points:
        for shape in model.shapes:
            shape.insert_vertex(or_pt, tolerance=0.1)

    # ensure that there is only one contiguous shape without holes
    shape_geos = [shape.geometry for shape in model.shapes]
    polyface = Polyface3D.from_faces(shape_geos, tolerance=0.1)
    outer_edges = polyface.naked_edges
    joined_boundary = Polyline3D.join_segments(outer_edges, tolerance=0.1)
    if len(joined_boundary) != 1:
        b_msg = 'The Shapes of the input model do not form a contiguous region ' \
            'without any holes.'
        join_faces = [Face3D(poly.vertices) for poly in joined_boundary]
        merged_faces = Face3D.merge_faces_to_holes(join_faces, 0.1)
        region_count = len(merged_faces)
        plural = 's' if region_count != 1 else ''
        hole_count = 0
        for mf in merged_faces:
            if mf.has_holes:
                hole_count += len(mf.holes)
        d_msg = '{} distinct region{} with {} total holes were found.'.format(
            region_count, plural, hole_count)
        raise ValueError('{}\n{}'.format(b_msg, d_msg))

    # gather all of the extra edges to be written as adiabatic
    adiabatic_geo, adiabatic_adj = [], []
    for edge in outer_edges:
        bnd_matched = False
        for bound in model.boundaries:
            for si, seg in enumerate(bound.geometry):
                if seg.distance_to_point(edge.p1) < 0.1 and \
                        seg.distance_to_point(edge.p2) < 0.1:
                    if seg.length - edge.length > 0.1:  # split the boundary geo
                        cpt_1 = seg.closest_point(edge.p1)
                        cpt_2 = seg.closest_point(edge.p2)
                        all_pts = [seg.p1, cpt_1, cpt_2, seg.p2]
                        pt_dists = [seg.p1.distance_to_point(pt) for pt in all_pts]
                        s_pts = [p for _, p in sorted(zip(pt_dists, all_pts),
                                                      key=lambda pair: pair[0])]
                        new_geo = list(bound.geometry)
                        new_geo.pop(si)
                        for p in range(3):
                            if s_pts[p].distance_to_point(s_pts[p + 1]) > 0.1:
                                nl = LineSegment3D.from_end_points(s_pts[p], s_pts[p + 1])
                                new_geo.append(nl)
                        bound._geometry = tuple(new_geo)
                    bnd_matched = True
                    break
            if bnd_matched:
                break
        else:  # adiabatic segment to be added at the end
            shape_matched = False
            for shape in model.shapes:
                for seg in shape.geometry.segments:
                    if edge.p1.is_equivalent(seg.p1, 0.1) or \
                            edge.p1.is_equivalent(seg.p2, 0.1):
                        if edge.p2.is_equivalent(seg.p1, 0.1) or \
                                edge.p2.is_equivalent(seg.p2, 0.1):
                            adiabatic_adj.append([shape.therm_uuid])
                            if edge.p1.is_equivalent(seg.p2, 0.1):
                                edge = edge.flip()
                            shape_matched = True
                            break
                if shape_matched:
                    break
            adiabatic_geo.append(edge)
            if not shape_matched:
                adiabatic_adj.append([])

    # gather any edges to be written with a frame cavity boundary
    frame_cavity_geo, cavity_props, enclosure_numbers = [], [], []
    enclosure_count = 1
    solid_shapes, cavity_shapes = [], []
    for shape in model.shapes:
        c_mat = shape.properties.therm.material
        if isinstance(c_mat, CavityMaterial) and c_mat.cavity_model != 'CEN':
            cavity_shapes.append(shape)
            cav_id = therm_id_from_uuid(str(uuid.uuid4()))
            cav_number = str(enclosure_count)
            enclosure_count += 1
            if shape.user_data is None:
                shape.user_data = {'cavity_id': cav_id}
            else:
                shape.user_data['cavity_id'] = cav_id
            cavity_prop = [cav_id, c_mat.emissivity, c_mat.emissivity_back,
                           shape.area * 1e-6]
            cavity_props.append(cavity_prop)
            for edge in shape.geometry.segments:
                frame_cavity_geo.append(edge)
                enclosure_numbers.append(cav_number)
        else:
            solid_shapes.append(shape)
    if len(frame_cavity_geo) == 0:
        cavity_boundary = None
        all_boundaries = model.boundaries
    else:
        cavity_boundary = Boundary(frame_cavity_geo)
        cavity_boundary.properties.therm.condition = frame_cavity
        cavity_boundary.user_data = {'enclosure_numbers': enclosure_numbers}
        all_boundaries = model.boundaries + (cavity_boundary,)

    # add the UUIDs of the polygons next to the edges to the Boundary.user_data
    ordered_shapes = cavity_shapes + solid_shapes
    for bound in all_boundaries:
        oriented_geo, bound_adj_shapes, bound_emissivity = [], [], []
        for edge in bound.geometry:
            adj_shapes, bnd_e = [], 0.9
            for shape in ordered_shapes:
                for seg in shape.geometry.segments:
                    if edge.p1.is_equivalent(seg.p1, 0.1) or \
                            edge.p1.is_equivalent(seg.p2, 0.1):
                        if edge.p2.is_equivalent(seg.p1, 0.1) or \
                                edge.p2.is_equivalent(seg.p2, 0.1):
                            adj_shapes.append(shape.therm_uuid)
                            if edge.p1.is_equivalent(seg.p2, 0.1):
                                edge = edge.flip()
                            shape_mat = shape.properties.therm.material
                            if not isinstance(shape_mat, CavityMaterial):
                                bnd_e = shape_mat.emissivity
                            break
            bound_adj_shapes.append(adj_shapes)
            bound_emissivity.append(bnd_e)
            oriented_geo.append(edge)
        bound._geometry = tuple(oriented_geo)
        if bound.user_data is None:
            bound.user_data = {
                'adj_polys': bound_adj_shapes,
                'emissivities': bound_emissivity
            }
        else:
            bound.user_data['adj_polys'] = bound_adj_shapes
            bound.user_data['emissivities'] = bound_emissivity

    # load up the template XML file for the model
    package_dir = os.path.dirname(os.path.abspath(__file__))
    template_file = os.path.join(package_dir, '_templates', 'Default.xml')
    xml_tree = ET.parse(template_file)
    xml_root = xml_tree.getroot()
    model_name = clean_string(model.display_name)

    # assign the property for the scale so it looks good in THERM
    xml_preferences = xml_root.find('Preferences')
    xml_settings = xml_preferences.find('Settings')
    xml_scale = xml_settings.find('Scale')
    xml_scale.text = str(scale)

    # set the properties for the document
    xml_props = xml_root.find('Properties')
    xml_gen = xml_props.find('General')
    therm_ver = '.'.join(str(i) for i in folders.THERM_VERSION)
    therm_ver = 'Version {}'.format(therm_ver)
    xml_calc_ver = xml_gen.find('CalculationVersion')
    xml_calc_ver.text = therm_ver
    xml_cre_ver = xml_gen.find('CreationVersion')
    xml_cre_ver.text = therm_ver
    xml_mod_ver = xml_gen.find('LastModifiedVersion')
    xml_mod_ver.text = therm_ver
    xml_cre_date = xml_gen.find('CreationDate')
    xml_cre_date.text = str(datetime.datetime.now().replace(microsecond=0))
    xml_cre_date = xml_gen.find('LastModified')
    xml_cre_date.text = str(datetime.datetime.now().replace(microsecond=0))
    xml_model_name = xml_gen.find('Title')
    xml_model_name.text = model_name

    # write the 3D plane into the notes section
    xml_notes = xml_gen.find('Notes')
    xml_notes.text = 'Plane: {}'.format(json.dumps(plane.to_dict()))

    # add the calculation options
    sim_par = simulation_par if simulation_par is not None else SimulationParameter()
    xml_calc_opt = xml_props.find('CalculationOptions')
    sim_par.mesh.to_therm_xml(xml_calc_opt)

    # write all of the cavity definitions into the model
    if len(cavity_props) != 0:
        xml_cavities = ET.SubElement(xml_root, 'Cavities')
        for cp in cavity_props:
            _cavity_to_therm_xml(cp, xml_cavities)

    # translate all Shapes to polygons
    xml_polygons = ET.SubElement(xml_root, 'Polygons')
    for shape in model.shapes:
        shape_to_therm_xml(shape, plane, xml_polygons, reset_counter=False)

    # translate all Boundaries
    xml_boundaries = ET.SubElement(xml_root, 'Boundaries')
    for bound in model.boundaries:
        # remove any boundary geometries that are not assigned to shapes
        adj_polys, seg_es = bound.user_data['adj_polys'], bound.user_data['emissivities']
        new_segs, new_adj_polys, new_seg_es = [], [], []
        for seg, adj_poly, seg_e in zip(bound.geometry, adj_polys, seg_es):
            if len(adj_poly) != 0:
                new_segs.append(seg)
                new_adj_polys.append(adj_poly)
                new_seg_es.append(seg_e)
        # write the boundary into the XML
        if len(new_segs) != 0:
            bound._geometry = tuple(new_segs)
            bound.user_data['adj_polys'] = new_adj_polys
            bound.user_data['emissivities'] = new_seg_es
            boundary_to_therm_xml(bound, plane, xml_boundaries, reset_counter=False)

    # add the extra adiabatic boundaries
    ad_bnd = Boundary(adiabatic_geo)
    ad_bnd.properties.therm.condition = adiabatic
    ad_bnd.user_data = {'adj_polys': adiabatic_adj}
    boundary_to_therm_xml(ad_bnd, plane, xml_boundaries, reset_counter=False)

    # add the cavity boundaries if they exist
    if cavity_boundary is not None:
        boundary_to_therm_xml(cavity_boundary, plane, xml_boundaries, reset_counter=False)

    # reset the handle counter back to 1 and return the root XML element
    HANDLE_COUNTER = 1
    return xml_root


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


def model_to_therm_xml_str(model, simulation_par=None):
    """Generate a THERM XML string for a Model.

    The resulting Element has all geometry (Shapes and Boundaries).

    Args:
        model: A fairyfly Model for which an THERM XML text string will be returned.
        simulation_par: A fairyfly-therm SimulationParameter object to specify
            how the THERM simulation should be run. If None, default simulation
            parameters will be generated. (Default: None).
    """
    # create the XML string
    xml_root = model_to_therm_xml(model, simulation_par)
    try:  # try to indent the XML to make it read-able
        ET.indent(xml_root, '\t')
        return ET.tostring(xml_root, encoding='unicode')
    except AttributeError:  # we are in Python 2 and no indent is available
        return ET.tostring(xml_root)


def model_to_thmz(model, output_file, simulation_par=None):
    """Write a THERM Zip (.thmz) file from a Fairyfly Model.

    Args:
        model: A fairyfly Model for which an THMZ file will be written.
        output_file: The path to the THMZ file that will be written from the model.
        simulation_par: A fairyfly-therm SimulationParameter object to specify
            how the THERM simulation should be run. If None, default simulation
            parameters will be generated. (Default: None).

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

        # create the THERM Zip file for the model
        thmz = os.path.join(folders.default_simulation_folder, 'model.thmz')
        xml_str = model.to_thmz(thmz)
    """
    # make sure the directory exists where the file will be written
    dir_name = os.path.dirname(os.path.abspath(output_file))
    if not os.path.isdir(dir_name):
        os.makedirs(dir_name)
    # create a temporary directory where everything will be zipped
    therm_trans_dir = tempfile.gettempdir()
    files_to_zip = []

    # prepare the files for materials and gases
    mat_file = os.path.join(therm_trans_dir, 'Materials.xml')
    gas_file = os.path.join(therm_trans_dir, 'Gases.xml')
    gases, pure_gases = [], []
    xml_materials = ET.Element('Materials')
    xml_gases = ET.Element('Gases')
    for xml_rt in (xml_materials, xml_gases):
        xml_ver = ET.SubElement(xml_rt, 'Version')
        xml_ver.text = '1'
    # rename any materials with duplicate display names
    model_mats = model.properties.therm.materials
    mat_names, reset_dict = {}, {}
    for mat in model_mats:
        if mat.display_name in mat_names:
            mat_names[mat.display_name] += 1
            reset_dict[mat.display_name] = mat
            mat.unlock()
            mat.display_name = mat.display_name + '_' + str(mat_names[mat.display_name])
            mat.lock()
        else:
            mat_names[mat.display_name] = 1
    # write the materials and gases to a file
    for mat in model_mats:
        mat.to_therm_xml(xml_materials)
        if isinstance(mat, CavityMaterial):
            gases.append(mat.gas)
            for pg in mat.gas.pure_gases:
                pure_gases.append(pg)
    _xml_element_to_file(xml_materials, mat_file)
    files_to_zip.append(mat_file)
    for pg in pure_gases:
        pg.to_therm_xml(xml_gases)
    for g in gases:
        g.to_therm_xml(xml_gases)
    _xml_element_to_file(xml_gases, gas_file)
    files_to_zip.append(gas_file)

    # write the Model into the temporary directory
    model_file = os.path.join(therm_trans_dir, 'Model.xml')
    xml_model = model_to_therm_xml(model, simulation_par)
    xml_props = xml_model.find('Properties')
    xml_gen = xml_props.find('General')
    xml_direct = xml_gen.find('Directory')
    xml_direct.text = dir_name
    xml_file_name = xml_gen.find('FileName')
    xml_file_name.text = os.path.basename(output_file.replace('.thmz', ''))
    _xml_element_to_file(xml_model, model_file)
    files_to_zip.append(model_file)

    # write the boundary conditions to a file
    bc_file = os.path.join(therm_trans_dir, 'SteadyStateBC.xml')
    xml_bcs = ET.Element('BoundaryConditions')
    xml_ver = ET.SubElement(xml_bcs, 'Version')
    xml_ver.text = '1'
    for bc in [adiabatic] + model.properties.therm.conditions:
        bc.to_therm_xml(xml_bcs)
    _xml_element_to_file(xml_bcs, bc_file)
    files_to_zip.append(bc_file)

    # put back any materials that were edited
    for mat_name, mat in reset_dict.items():
        mat.unlock()
        mat.display_name = mat_name
        mat.lock()

    # zip everything together
    with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in files_to_zip:
            # Add the file to the zip archive
            # arcname=os.path.basename(file) ensures only the filename is used
            # inside the zip, avoiding unwanted directory structures
            zipf.write(file, arcname=os.path.basename(file))

    return output_file


def _xml_element_to_file(xml_root, file_path):
    """Write an XML element to a file."""
    try:  # try to indent the XML to make it read-able
        ET.indent(xml_root, '\t')
        xml_str = ET.tostring(xml_root, encoding='unicode', short_empty_elements=False)
    except AttributeError:  # we are in Python 2 and no indent is available
        xml_str = ET.tostring(xml_root)
    with open(file_path, 'wb') as fp:
        fp.write(xml_str.encode('utf-8'))
