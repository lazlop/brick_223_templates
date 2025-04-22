"""
Brick 223 Templates package for creating and managing ASHRAE 223 templates from Brick schema.
"""

from .ai_complete_yaml import process_brick_template, validate_result
from .create_yaml_brick import process_class_hierarchy, strip_namespace
from .utils import * 
from .namespaces import *
from .get_completion import get_completion
from .get_s223_data import get_s223_info
from .create_223_templates import process_yaml_file, process_directory, create_template_for_entity


def hello() -> str:
    return "Wow look at all these templates!"
