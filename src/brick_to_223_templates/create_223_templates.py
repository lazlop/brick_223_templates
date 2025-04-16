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

# Add the parent directory to the path so we can import namespaces
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from namespaces import (
    BRICK, S223, QUDT, PARAM, QK, UNIT, RDF, RDFS, XSD, OWL, SKOS, SH, 
    TAG, BSH, REF, BACNET, BM, CONSTRAINT, HPF, HPFS, bind_prefixes, get_prefixes
)

def create_template_for_entity(entity_name, entity_data):
    """
    Create an S223 template for a given entity based on its Brick YAML data.
    
    Args:
        entity_name: The name of the entity (e.g., 'Temperature_Sensor')
        entity_data: Dictionary containing the entity's properties from the YAML file
    
    Returns:
        A string containing the template in Turtle format
    """
    g = Graph()
    bind_prefixes(g)
    
    # Create the main entity
    entity = PARAM.name
    
    # Add the type based on s223_class
    s223_class = entity_data.get('s223_class')
    if s223_class:
        s223_class_uri = URIRef(s223_class)
        g.add((entity, RDF.type, s223_class_uri))
    
    # For quantifiable properties, add the quantity kind
    if entity_data.get('quantitykind'):
        # Create a property for the quantity kind
        qk_property = PARAM[f"quantitykind_name"]
        g.add((entity, S223.hasProperty, qk_property))
    
    # Add medium if present
    if entity_data.get('medium') and entity_data.get('medium') != 'None':
        medium_property = PARAM[f"medium_name"]
        g.add((entity, S223.hasProperty, medium_property))
    
    # Add aspects if present
    if entity_data.get('aspects') and entity_data.get('aspects') != 'None':
        aspects = entity_data.get('aspects').split(',')
        for i, aspect in enumerate(aspects):
            aspect = aspect.strip()
            if aspect:
                aspect_property = PARAM[f"aspect{i+1}_name"]
                g.add((entity, S223.hasProperty, aspect_property))
    
    # Determine which namespaces are actually used in the graph
    used_namespaces = set()
    for s, p, o in g:
        if isinstance(s, URIRef):
            ns = str(s).split('#')[0] + '#'
            used_namespaces.add(ns)
        if isinstance(p, URIRef):
            ns = str(p).split('#')[0] + '#'
            used_namespaces.add(ns)
        if isinstance(o, URIRef):
            ns = str(o).split('#')[0] + '#'
            used_namespaces.add(ns)
    
    # Create a minimal graph with only the necessary namespaces
    minimal_g = Graph()
    
    # Only bind the namespaces that are actually used
    if str(PARAM) in used_namespaces:
        minimal_g.bind('p', PARAM)
    if str(BRICK) in used_namespaces:
        minimal_g.bind('brick', BRICK)
    if str(S223) in used_namespaces:
        minimal_g.bind('s223', S223)
    if str(QUDT) in used_namespaces:
        minimal_g.bind('qudt', QUDT)
    if str(QK) in used_namespaces:
        minimal_g.bind('quantitykind', QK)
    
    # Add all triples to the minimal graph
    for s, p, o in g:
        minimal_g.add((s, p, o))
    
    # Get the prefixes in Turtle format
    prefixes = []
    for prefix, namespace in minimal_g.namespace_manager.namespaces():
        if prefix and str(namespace) in used_namespaces:
            prefixes.append(f"@prefix {prefix}: <{namespace}> .")
    
    # # Serialize the graph without prefixes
    # turtle = minimal_g.serialize(format="turtle")
    
    # # Extract just the triples part (remove the prefixes)
    # turtle_lines = turtle.split('\n')
    # content_start = 0
    # for i, line in enumerate(turtle_lines):
    #     if not line.startswith('@prefix'):
    #         content_start = i
    #         break
    
    # # Combine our custom prefixes with the triples
    # template = '\n'.join(prefixes) + '\n' + '\n'.join(turtle_lines[content_start:])

    template = minimal_g.serialize(format="turtle")
    return template

def process_yaml_file(yaml_path, output_dir):
    """
    Process a YAML file and create templates for each entity in it.
    
    Args:
        yaml_path: Path to the YAML file
        output_dir: Directory to write the templates to
    """
    with open(yaml_path, 'r') as f:
        data = yaml.safe_load(f)
    print(data)
    if not data:
        return
    
    # Create the output directory structure
    rel_path = os.path.relpath(yaml_path, start=os.path.join('brick_yaml_reviewed', 'brick_yaml'))
    template_dir = os.path.join(output_dir, os.path.dirname(rel_path))
    os.makedirs(template_dir, exist_ok=True)
    
    # Process each entity in the YAML file
    template_dict = {}
    for entity_name, entity_data in data.items():
        # Generate the S223 template
        template = create_template_for_entity(entity_name, entity_data)
        
        # Create the entity directory
        entity_dir = os.path.join(template_dir, entity_name)
        os.makedirs(entity_dir, exist_ok=True)
        
        # Create the YAML template file in the format requested
        template_dict[entity_name] = {
                'body': template
            }
        
    yaml_path = os.path.join(entity_dir, f"{entity_name}.yml")
    with open(yaml_path, 'w') as f:
        yaml.dump(template_dict, f)
        
    # For debugging/reference, also save the raw turtle file
    ttl_path = os.path.join(entity_dir, f"{entity_name}.ttl")
    with open(ttl_path, 'w') as f:
        f.write(template)

def process_directory(dir_path, output_dir):
    """
    Recursively process all YAML files in a directory.
    
    Args:
        dir_path: Path to the directory containing YAML files
        output_dir: Directory to write the templates to
    """
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.endswith('.yml'):
                yaml_path = os.path.join(root, file)
                process_yaml_file(yaml_path, output_dir)

def main():
    """Main function to run the script."""
    input_dir = os.path.join('brick_yaml_reviewed', 'brick_yaml')
    output_dir = 's223_templates'
    
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Process all YAML files in the input directory
    process_directory(input_dir, output_dir)
    
    print(f"Templates generated in {output_dir}")

if __name__ == "__main__":
    main()

# %%
