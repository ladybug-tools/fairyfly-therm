"""fairyfly-therm library."""
from fairyfly.logutil import get_logger

# load all functions that extends fairyfly core library
import fairyfly_therm._extend_fairyfly

# use the same logger settings across fairyfly extensions
# this does NOT mean that the logs will be written to the same file but they will have
# the same formatting, level, etc.
logger = get_logger(name=__name__)
