# coding=utf-8
"""Complete set of THERM Simulation Settings."""
from __future__ import division

from .mesh import MeshControl


class SimulationParameter(object):
    """Complete set of Therm Simulation Settings.

    Args:
        mesh: A MeshControl that lists the desired meshing procedure. If None,
            default meshing control will be automatically generated. (Default: None).

    Properties:
        * mesh
    """
    __slots__ = ('_mesh',)

    def __init__(self, mesh=None):
        """Initialize SimulationParameter."""
        self.mesh = mesh

    @property
    def mesh(self):
        """Get or set a MeshControl object for the simulation meshing procedure."""
        return self._mesh

    @mesh.setter
    def mesh(self, value):
        if value is not None:
            assert isinstance(value, MeshControl), 'Expected MeshControl ' \
                'for SimulationParameter output. Got {}.'.format(type(value))
            self._mesh = value
        else:
            self._mesh = MeshControl()

    @classmethod
    def from_dict(cls, data):
        """Create a SimulationParameter object from a dictionary.

        Args:
            data: A SimulationParameter dictionary in following the format below.

        .. code-block:: python

            {
            "type": "SimulationParameter",
            "mesh": {} # Fairyfly MeshControl dictionary
            }
        """
        assert data['type'] == 'SimulationParameter', \
            'Expected SimulationParameter dictionary. Got {}.'.format(data['type'])
        mesh = None
        if 'mesh' in data and data['mesh'] is not None:
            mesh = MeshControl.from_dict(data['mesh'])
        return cls(mesh)

    def to_dict(self):
        """SimulationParameter dictionary representation."""
        return {
            'type': 'SimulationParameter',
            'mesh': self.mesh.to_dict()
        }

    def duplicate(self):
        """Get a copy of this object."""
        return self.__copy__()

    def ToString(self):
        """Overwrite .NET ToString."""
        return self.__repr__()

    def __copy__(self):
        return SimulationParameter(self.mesh.duplicate())

    def __key(self):
        """A tuple based on the object properties, useful for hashing."""
        return (hash(self.mesh),)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        return isinstance(other, SimulationParameter) and self.__key() == other.__key()

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return 'Therm SimulationParameter:'
