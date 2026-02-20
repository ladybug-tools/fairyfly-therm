# coding=utf-8
"""Complete set of THERM Simulation Settings."""
from __future__ import division

from .mesh import MeshControl
from .exposure import ModelExposure


class SimulationParameter(object):
    """Complete set of Therm Simulation Settings.

    Args:
        mesh: A MeshControl that lists the desired meshing procedure. If None,
            default meshing control will be automatically generated. (Default: None).
        exposure: A ModelExposure that describes the model location in a building.
            If None, default exposure will be automatically generated. (Default: None).

    Properties:
        * mesh
        * exposure
    """
    __slots__ = ('_mesh', '_exposure')

    def __init__(self, mesh=None, exposure=None):
        """Initialize SimulationParameter."""
        self.mesh = mesh
        self.exposure = exposure

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

    @property
    def exposure(self):
        """Get or set a ModelExposure object that describes the model location in a building.
        """
        return self._exposure

    @exposure.setter
    def exposure(self, value):
        if value is not None:
            assert isinstance(value, ModelExposure), 'Expected ModelExposure ' \
                'for SimulationParameter output. Got {}.'.format(type(value))
            self._exposure = value
        else:
            self._exposure = ModelExposure()

    @classmethod
    def from_dict(cls, data):
        """Create a SimulationParameter object from a dictionary.

        Args:
            data: A SimulationParameter dictionary in following the format below.

        .. code-block:: python

            {
            "type": "SimulationParameter",
            "mesh": {} # Fairyfly MeshControl dictionary
            "exposure": {}  # Fairyfly ModelExposure dictionary
            }
        """
        assert data['type'] == 'SimulationParameter', \
            'Expected SimulationParameter dictionary. Got {}.'.format(data['type'])
        mesh = None
        if 'mesh' in data and data['mesh'] is not None:
            mesh = MeshControl.from_dict(data['mesh'])
        exposure = None
        if 'exposure' in data and data['exposure'] is not None:
            exposure = ModelExposure.from_dict(data['exposure'])
        return cls(mesh, exposure)

    def to_dict(self):
        """SimulationParameter dictionary representation."""
        return {
            'type': 'SimulationParameter',
            'mesh': self.mesh.to_dict(),
            'exposure': self.exposure.to_dict()
        }

    def duplicate(self):
        """Get a copy of this object."""
        return self.__copy__()

    def ToString(self):
        """Overwrite .NET ToString."""
        return self.__repr__()

    def __copy__(self):
        return SimulationParameter(self.mesh.duplicate(), self.exposure.duplicate())

    def __key(self):
        """A tuple based on the object properties, useful for hashing."""
        return (hash(self.mesh), hash(self.exposure))

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        return isinstance(other, SimulationParameter) and self.__key() == other.__key()

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return 'Therm SimulationParameter:'
