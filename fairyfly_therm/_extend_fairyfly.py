# coding=utf-8
# import all of the modules for writing geometry to dsbXML
from fairyfly.properties import ModelProperties, ShapeProperties, BoundaryProperties
import fairyfly.writer.shape as shape_writer
import fairyfly.writer.boundary as boundary_writer
import fairyfly.writer.model as model_writer

from .properties.model import ModelThermProperties
from .properties.shape import ShapeThermProperties
from .properties.boundary import BoundaryThermProperties
from .writer import model_to_therm_xml, model_to_thmz

# set a hidden therm attribute on each core geometry Property class to None
# define methods to produce therm property instances on each Property instance
ModelProperties._therm = None
ShapeProperties._therm = None
BoundaryProperties._therm = None


def model_therm_properties(self):
    if self._therm is None:
        self._therm = ModelThermProperties(self.host)
    return self._therm


def shape_therm_properties(self):
    if self._therm is None:
        self._therm = ShapeThermProperties(self.host)
    return self._therm


def boundary_therm_properties(self):
    if self._therm is None:
        self._therm = BoundaryThermProperties(self.host)
    return self._therm

# add therm property methods to the Properties classes
ModelProperties.therm = property(model_therm_properties)
ShapeProperties.therm = property(shape_therm_properties)
BoundaryProperties.therm = property(boundary_therm_properties)

# add writers to the honeybee-core modules
model_writer.therm_xml = model_to_therm_xml
model_writer.thmz = model_to_thmz
