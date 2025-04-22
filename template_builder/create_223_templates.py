# %%
"""
Script to generate S223 templates from Brick YAML files.
"""

import os
import yaml
from pathlib import Path
import rdflib
from rdflib import Graph, Literal, URIRef
import sys
from .namespaces import (
    BRICK, S223, QUDT, PARAM, QK, UNIT, RDF, RDFS, XSD, OWL, SKOS, SH, 
    TAG, BSH, REF, BACNET, BM, CONSTRAINT, HPF, HPFS, bind_prefixes, get_prefixes
)
from importlib.resources import files

notes_file = str(files('template_builder').joinpath('data/notes.yml'))

# TODO: correct namespace handling
def create_template_for_entity(entity_name, entity_data):
    """
    Create an S223 template for a given entity based on its Brick YAML data.
    
    Args:
        entity_name: The name of the entity (e.g., 'Temperature_Sensor')
        entity_data: Dictionary containing the entity's properties from the YAML file
    
    Returns:
        A string containing the template in Turtle format, the optional parameters, and the dependencies
    """
    g = Graph()
    bind_prefixes(g)
    
    # Create the main entity
    entity = PARAM.name
    
    # Add the type based on s223_class
    s223_class = entity_data.get('s223_class')
    if entity_data.get('s223_class'):
        s223_class_uri = S223[s223_class.split(':')[-1]]
        g.add((entity, RDF.type, s223_class_uri))
    
    # prefix_map = {prefix: namespace for prefix, namespace in g.namespace_manager.namespaces()}
    
    # For quantifiable properties, add the quantity kind
    # TODO: correct namespacing issues 
    if entity_data.get('quantitykind'):
        # Create a property for the quantity kind
        quantitykind = entity_data.get('quantitykind').split(':')[-1]
        g.add((entity, QUDT.hasQuantityKind, QK[quantitykind]))
    
    # if enumerationkind present add it
    if entity_data.get('enumerationkind'):
        # Create a property for the enumeration kind
        enumerationkind = entity_data.get('enumerationkind').split(':')[-1]
        g.add((entity, S223.hasEnumerationKind, S223[enumerationkind]))

    # Add medium if present
    if entity_data.get('medium') and entity_data.get('medium') != 'None':
        medium = entity_data.get('medium').split(':')[-1]
        g.add((entity, S223.ofMedium, S223[medium]))
    
    # Add aspects if present
    if entity_data.get('aspects') and entity_data.get('aspects') != 'None':
        aspects = entity_data.get('aspects').split(',')
        for i, aspect in enumerate(aspects):
            aspect = aspect.strip().split(':')[-1]
            if aspect:
                g.add((entity, S223.hasAspect, S223[aspect]))

    # add property of if present
    if entity_data.get('property_of') and entity_data.get('property_of') != 'None':
        property_of = entity_data.get('property_of').split(':')[-1]
        print('ADDING PROP OF: ', property_of)
        g.add((PARAM[property_of], S223.hasProperty, entity))

        # TODO: Decide how to handle optional and dependencies 
        optional = [property_of]
        dependencies = [ {'template': property_of, "args": {"name": property_of}} ]
    else:
        optional = None
        dependencies = None

    return g.serialize(), optional, dependencies

# Define a custom class for folded style text
class FoldedString(str):
    pass

# Create a custom representer for the folded style
def folded_str_representer(dumper, data):
    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='>')

# Register the representer
yaml.add_representer(FoldedString, folded_str_representer)


def process_yaml_file(yaml_path, output_path):
    """
    Process a YAML file and create templates for each entity in it.
    
    Args:
        yaml_path: Path to the YAML file
        output_dir: Directory to write the templates to
    """
    with open(yaml_path, 'r') as f:
        data = yaml.safe_load(f)
    # print(data)
    if not data:
        return
    
    # Process each entity in the YAML file
    template_dict = {}
    for entity_name, entity_data in data.items():
        # Generate the S223 template
        template, optional, dependencies = create_template_for_entity(entity_name, entity_data)
        # Create the YAML template file in the format requested
        template_dict[entity_name] = {
                'body': FoldedString(template),  # Use the custom class for folded style template
            }
        if optional:
            template_dict[entity_name]['optional'] = optional
        if dependencies:
            template_dict[entity_name]['dependencies'] = dependencies
    with open(output_path, 'w') as f:
        yaml.dump(
            template_dict,
            f,
            default_flow_style=False,
            sort_keys=False
)
        
def save_notes(yaml_path):
    with open(yaml_path, 'r') as f:
        data = yaml.safe_load(f)

    with open(notes_file, 'r') as f:
        notes_dict = yaml.safe_load(f)

    for entity_name, entity_data in data.items():
        if entity_data.get('note'):
            notes_dict[entity_name] = {'note':entity_data['note']}
    
        
    with open(notes_file, 'w') as f:
        yaml.safe_dump(
            notes_dict,
            f,
            default_flow_style=False,
            sort_keys=False
        )
    

def process_directory(input_dir, output_dir):
    """
    Recursively process all YAML files in a directory.
    
    Args:
        dir_path: Path to the directory containing YAML files
        output_dir: Directory to write the templates to
    """
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.yml'):
                yaml_path = os.path.join(root, file)
                save_notes(yaml_path)

    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.yml'):
                yaml_path = os.path.join(root, file)
                # Create the output directory structure
                rel_path = os.path.relpath(yaml_path, start=os.path.join('brick_yaml_reviewed', 'brick_yaml'))
                template_dir = os.path.join(output_dir, os.path.dirname(rel_path))
                # print(template_dir)
                os.makedirs(template_dir, exist_ok=True)
                output_path = os.path.join(template_dir, file)
                # print(output_path)
                process_yaml_file(yaml_path, output_path)

