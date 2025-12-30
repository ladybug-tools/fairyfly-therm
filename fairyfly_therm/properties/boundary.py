# coding=utf-8
"""Boundary Therm Properties."""
from fairyfly.checkdup import is_equivalent

from ..condition.steadystate import SteadyState
from ..lib.conditions import exterior


class BoundaryThermProperties(object):
    """Therm Properties for Fairyfly Boundary.

    Args:
        host: A fairyfly_core Boundary object that hosts these properties.
        condition: An optional Condition object to set the conductive properties
            of the Boundary. The default is set to a generic concrete condition.

    Properties:
        * host
        * condition
    """
    __slots__ = ('_host', '_condition')

    def __init__(self, host, condition=None):
        """Initialize Boundary THERM properties."""
        self._host = host
        self.condition = condition

    @property
    def host(self):
        """Get the Boundary object hosting these properties."""
        return self._host

    @property
    def condition(self):
        """Get or set a THERM Condition for the boundary."""
        if self._condition:  # set by user
            return self._condition
        return exterior

    @condition.setter
    def condition(self, value):
        if value is not None:
            assert isinstance(value, SteadyState), \
                'Expected SteadyState. Got {}.'.format(type(value))
            value.lock()  # lock editing in case condition has multiple references
        self._condition = value

    @classmethod
    def from_dict(cls, data, host):
        """Create BoundaryThermProperties from a dictionary.

        Note that the dictionary must be a non-abridged version for this
        classmethod to work.

        Args:
            data: A dictionary representation of BoundaryThermProperties with the
                format below.
            host: A Boundary object that hosts these properties.

        .. code-block:: python

            {
            "type": 'BoundaryThermProperties',
            "condition": {},  # A SteadyState dictionary
            }
        """
        assert data['type'] == 'BoundaryThermProperties', \
            'Expected BoundaryThermProperties. Got {}.'.format(data['type'])
        new_prop = cls(host)
        if 'condition' in data and data['condition'] is not None:
            new_prop.condition = SteadyState.from_dict(data['condition'])
        return new_prop

    def apply_properties_from_dict(self, abridged_data, conditions):
        """Apply properties from a BoundaryThermPropertiesAbridged dictionary.

        Args:
            abridged_data: A BoundaryThermPropertiesAbridged dictionary (typically
                coming from a Model).
            conditions: A dictionary of conditions with condition identifiers
                as keys, which will be used to re-assign conditions.
        """
        if 'condition' in abridged_data and abridged_data['condition'] is not None:
            try:
                self.condition = conditions[abridged_data['condition']]
            except KeyError:
                raise ValueError('Boundary condition "{}" was not found in '
                                 'conditions.'.format(abridged_data['condition']))

    def to_dict(self, abridged=False):
        """Return therm properties as a dictionary.

        Args:
            abridged: Boolean to note whether the full dictionary describing the
                object should be returned (False) or just an abridged version (True).
                Default: False.
        """
        base = {'therm': {}}
        base['therm']['type'] = 'BoundaryThermProperties' if not \
            abridged else 'BoundaryThermPropertiesAbridged'
        if self._condition is not None:
            base['therm']['condition'] = \
                self._condition.identifier if abridged else self._condition.to_dict()
        return base

    def duplicate(self, new_host=None):
        """Get a copy of this object.

        Args:
            new_host: A new Boundary object that hosts these properties.
                If None, the properties will be duplicated with the same host.
        """
        _host = new_host or self._host
        return BoundaryThermProperties(_host, self._condition)

    def is_equivalent(self, other):
        """Check to see if these therm properties are equivalent to another object.

        This will only be True if all properties match (except for the host) and
        will otherwise be False.
        """
        if not is_equivalent(self._condition, other._condition):
            return False
        return True

    def ToString(self):
        return self.__repr__()

    def __repr__(self):
        return 'Boundary Therm Properties: [host: {}]'.format(self.host.display_name)
