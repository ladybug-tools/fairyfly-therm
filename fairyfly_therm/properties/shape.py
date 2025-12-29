# coding=utf-8
"""Shape Therm Properties."""
from honeybee.typing import clean_rad_string
from honeybee.checkdup import is_equivalent

from ..material.solid import SolidMaterial

from ..lib.materials import generic_concrete


class ShapeThermProperties(object):
    """Therm Properties for Honeybee Shape.

    Args:
        host: A honeybee_core Shape object that hosts these properties.
        material: An optional Material object to set the conductive properties
            of the Shape. The default is set to a generic concrete material.

    Properties:
        * host
        * material
    """

    __slots__ = ('_host', '_material')

    def __init__(self, host, material=None):
        """Initialize Shape THERM properties."""
        self._host = host
        self.material = material

    @property
    def host(self):
        """Get the Shape object hosting these properties."""
        return self._host

    @property
    def material(self):
        """Get or set a THERM Material for the shape."""
        if self._material:  # set by user
            return self._material
        return generic_concrete

    @material.setter
    def material(self, value):
        if value is not None:
            assert isinstance(value, SolidMaterial), \
                'Expected SolidMaterial. Got {}.'.format(type(value))
            value.lock()  # lock editing in case material has multiple references
        self._material = value

    @classmethod
    def from_dict(cls, data, host):
        """Create ShapeThermProperties from a dictionary.

        Note that the dictionary must be a non-abridged version for this
        classmethod to work.

        Args:
            data: A dictionary representation of ShapeThermProperties with the
                format below.
            host: A Shape object that hosts these properties.

        .. code-block:: python

            {
            "type": 'ShapeThermProperties',
            "construction": {},  # A ShapeConstruction dictionary
            "transmittance_schedule": {},  # A transmittance schedule dictionary
            "pv_properties": {}  # A PVProperties dictionary
            }
        """
        assert data['type'] == 'ShapeThermProperties', \
            'Expected ShapeThermProperties. Got {}.'.format(data['type'])

        new_prop = cls(host)
        if 'construction' in data and data['construction'] is not None:
            new_prop.construction = ShapeConstruction.from_dict(data['construction'])
        if 'transmittance_schedule' in data and \
                data['transmittance_schedule'] is not None:
            sch_dict = data['transmittance_schedule']
            if sch_dict['type'] == 'ScheduleRuleset':
                new_prop.transmittance_schedule = \
                    ScheduleRuleset.from_dict(data['transmittance_schedule'])
            elif sch_dict['type'] == 'ScheduleFixedInterval':
                new_prop.transmittance_schedule = \
                    ScheduleFixedInterval.from_dict(data['transmittance_schedule'])
            else:
                raise ValueError(
                    'Expected non-abridged Schedule dictionary for Shape '
                    'transmittance_schedule. Got {}.'.format(sch_dict['type']))
        if 'pv_properties' in data and data['pv_properties'] is not None:
            new_prop.pv_properties = PVProperties.from_dict(data['pv_properties'])
        return new_prop

    def apply_properties_from_dict(self, abridged_data, constructions, schedules):
        """Apply properties from a ShapeThermPropertiesAbridged dictionary.

        Args:
            abridged_data: A ShapeThermPropertiesAbridged dictionary (typically
                coming from a Model).
            constructions: A dictionary of constructions with constructions identifiers
                as keys, which will be used to re-assign constructions.
            schedules: A dictionary of schedules with schedule identifiers as keys,
                which will be used to re-assign schedules.
        """
        if 'construction' in abridged_data and abridged_data['construction'] is not None:
            try:
                self.construction = constructions[abridged_data['construction']]
            except KeyError:
                raise ValueError('Shape construction "{}" was not found in '
                                 'constructions.'.format(abridged_data['construction']))
        if 'transmittance_schedule' in abridged_data and \
                abridged_data['transmittance_schedule'] is not None:
            self.transmittance_schedule = \
                schedules[abridged_data['transmittance_schedule']]
        if 'pv_properties' in abridged_data and \
                abridged_data['pv_properties'] is not None:
            self.pv_properties = PVProperties.from_dict(abridged_data['pv_properties'])

    def to_dict(self, abridged=False):
        """Return therm properties as a dictionary.

        Args:
            abridged: Boolean to note whether the full dictionary describing the
                object should be returned (False) or just an abridged version (True).
                Default: False.
        """
        base = {'therm': {}}
        base['therm']['type'] = 'ShapeThermProperties' if not \
            abridged else 'ShapeThermPropertiesAbridged'
        if self._construction is not None:
            base['therm']['construction'] = \
                self._construction.identifier if abridged else \
                self._construction.to_dict()
        if self.transmittance_schedule is not None:
            base['therm']['transmittance_schedule'] = \
                self.transmittance_schedule.identifier if abridged else \
                self.transmittance_schedule.to_dict()
        if self.pv_properties is not None:
            base['therm']['pv_properties'] = self.pv_properties.to_dict()
        return base

    def duplicate(self, new_host=None):
        """Get a copy of this object.

        Args:
            new_host: A new Shape object that hosts these properties.
                If None, the properties will be duplicated with the same host.
        """
        _host = new_host or self._host
        return ShapeThermProperties(
            _host, self._construction, self._transmittance_schedule, self._pv_properties)

    def is_equivalent(self, other):
        """Check to see if these therm properties are equivalent to another object.

        This will only be True if all properties match (except for the host) and
        will otherwise be False.
        """
        if not is_equivalent(self._construction, other._construction):
            return False
        if not is_equivalent(
                self._transmittance_schedule, other._transmittance_schedule):
            return False
        if not is_equivalent(self._pv_properties, other._pv_properties):
            return False
        return True

    def _radiance_modifier(self, ref):
        """Get a Radiance modifier that respects the transmittance schedule.

        Args:
            ref: The reflectance to be used in the modifier.
        """
        # check to be sure that the honeybee-radiance installed
        try:
            from honeybee_radiance.modifier.material import Trans
        except ImportError as e:
            raise ImportError('honeybee_radiance library must be installed to use '
                              'Shape radiance_modifier methods. {}'.format(e))

        # create the modifier from the properties
        if self.transmittance_schedule is None:
            return self.construction._to_radiance(ref)
        else:
            mod_id = '{}_mod'.format(clean_rad_string(self.host.identifier))
            if isinstance(self.transmittance_schedule, ScheduleRuleset):
                trans = self.transmittance_schedule.default_day_schedule.values[0]
            else:
                trans = self.transmittance_schedule.values[0]
            avg_ref = (1 - trans) * ref
            return Trans.from_average_properties(
                mod_id, average_reflectance=avg_ref, average_transmittance=trans,
                is_specular=self.construction.is_specular, is_diffusing=False)

    @staticmethod
    def _parent_construction_set(host_parent):
        """Recursively search through host parents to find a ConstructionSet."""
        if hasattr(host_parent.properties.therm, 'construction_set'):
            # we found the room with the construction set
            return host_parent.properties.therm.construction_set
        elif host_parent.has_parent:
            # we found an aperture or face that could have a room with a construction set
            return ShapeThermProperties._parent_construction_set(host_parent.parent)
        else:
            # there is no parent room
            return None

    def ToString(self):
        return self.__repr__()

    def __repr__(self):
        return 'Shape Therm Properties: [host: {}]'.format(self.host.display_name)
