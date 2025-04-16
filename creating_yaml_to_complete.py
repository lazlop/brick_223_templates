# %%
from rdflib import Graph
from utils import * 
from namespaces import * 
from get_completion import get_completion
import yaml
import re
import pandas as pd
from string import Template
import os
import pathlib
# %%
g = Graph()
g.parse("https://brickschema.org/schema/1.4.3/Brick.ttl", format = "ttl")

# %%
# Define the starting parent class
start_parent = "brick:Sensor"
start_parent_clean = strip_namespace(start_parent)

# Template for the SPARQL query
query_template = Template("""SELECT DISTINCT ?brick_class ?brick_definition ?brick_parent WHERE {
    ?brick_class rdfs:subClassOf $start_parent ;
        skos:definition ?brick_definition .
    FILTER NOT EXISTS {
        ?brick_class2 rdfs:subClassOf $start_parent .
        ?brick_class rdfs:subClassOf ?brick_class2 .
    }
    FILTER NOT EXISTS {
        ?brick_class owl:deprecated true .
    }
    FILTER (!strstarts(str(?brick_class), "https://w3id.org/rec#")) 
    BIND ($start_parent AS ?brick_parent).
}""")

# %%
def strip_namespace(uri):
    """
    Strips namespace prefixes from URIs.
    For example, 'brick:TemperatureSensor' becomes 'TemperatureSensor'
    
    Parameters:
    -----------
    uri : str
        URI with namespace prefix
    
    Returns:
    --------
    str
        URI without namespace prefix
    """
    # Check if the URI contains a namespace prefix (contains a colon)
    if isinstance(uri, str) and ':' in uri:
        # Return everything after the colon
        return uri.split(':', 1)[1]
    return uri

def create_directory_structure(parent_class, parent_path=None):
    """
    Creates a directory named after the parent class within the parent path.
    
    Parameters:
    -----------
    parent_class : str
        Name of the parent class (without namespace)
    parent_path : str, optional
        Path to the parent directory. If None, uses the templates directory.
    
    Returns:
    --------
    str
        Path to the created directory
    """
    # Determine the base path
    if parent_path is None:
        # This is a top-level class, create it directly under templates
        base_path = "templates"
    else:
        # This is a subclass, create it under its parent's directory
        base_path = parent_path
    
    # Create the directory if it doesn't exist
    dir_path = os.path.join(base_path, parent_class)
    os.makedirs(dir_path, exist_ok=True)
    print(f"Created directory: {dir_path}")
    return dir_path

def save_classes_to_yaml(parent_class, children_data, parent_dir):
    """
    Saves all child classes of a parent to a single YAML file.
    
    Parameters:
    -----------
    parent_class : str
        Name of the parent class (without namespace)
    children_data : dict
        Dictionary mapping child class names to their data
    parent_dir : str
        Path to the parent directory
    
    Returns:
    --------
    str
        Path to the created YAML file
    """
    # Create the file path
    file_path = os.path.join(parent_dir, f"{parent_class}.yml")
    
    # Save to YAML
    with open(file_path, 'w') as file:
        yaml.dump(children_data, file, default_flow_style=False, sort_keys=False)
    
    print(f"Created YAML file: {file_path}")
    return file_path

def process_brick_classes(input_df, parent_dir):
    """
    Processes brick classes from a DataFrame and creates a single YAML file
    containing all classes organized by parent.
    
    Parameters:
    -----------
    input_df : pandas.DataFrame
        DataFrame containing brick_class, brick_parent, and brick_definition columns
    parent_dir : str
        Path to the parent directory where the YAML file should be saved.
    
    Returns:
    --------
    dict
        Dictionary mapping parent classes to their child classes data
    """
    # Ensure the input DataFrame has the required columns
    required_cols = ['brick_class', 'brick_parent', 'brick_definition']
    for col in required_cols:
        if col not in input_df.columns:
            raise ValueError(f"Input DataFrame must contain '{col}' column")
    
    # Group classes by parent
    parent_to_children_data = {}
    
    # Process each row in the DataFrame
    for _, row in input_df.iterrows():
        # Strip namespace prefixes
        brick_class = strip_namespace(row['brick_class'])
        brick_parent = strip_namespace(row['brick_parent'])
        brick_definition = row['brick_definition']
        
        # Create entry data (excluding brick_class)
        entry_data = {
            'brick_parent': brick_parent,
            'brick_definition': brick_definition
        }
        
        # Add to parent_to_children_data dictionary
        if brick_parent not in parent_to_children_data:
            parent_to_children_data[brick_parent] = {}
        
        # Add this class to its parent's data
        parent_to_children_data[brick_parent][brick_class] = entry_data
    
    # Save each parent's children to a single YAML file
    for parent, children_data in parent_to_children_data.items():
        save_classes_to_yaml(parent, children_data, parent_dir)
    
    return parent_to_children_data

# %%
def process_class_hierarchy(parent_class, graph, parent_path=None, processed_classes=None):
    """
    Recursively processes a class hierarchy, creating directories and YAML files
    for each class and its subclasses.
    
    Parameters:
    -----------
    parent_class : str
        The parent class URI with namespace (e.g., 'brick:Sensor')
    graph : rdflib.Graph
        The RDF graph containing the ontology
    parent_path : str, optional
        Path to the parent directory. If None, uses the templates directory.
    processed_classes : set, optional
        Set of classes that have already been processed to avoid cycles
    
    Returns:
    --------
    set
        Set of processed classes
    """
    if processed_classes is None:
        processed_classes = set()
    
    # Strip namespace for directory/file naming
    parent_class_clean = strip_namespace(parent_class)
    
    # Skip if already processed to avoid cycles
    if parent_class_clean in processed_classes:
        return processed_classes
    
    # Add to processed set
    processed_classes.add(parent_class_clean)
    
    
    # Get direct subclasses
    query = query_template.substitute(start_parent=parent_class)
    subclasses_df = query_to_df(query, graph)
    
    # If no subclasses, return
    if not subclasses_df.empty:
        parent_dir = create_directory_structure(parent_class_clean, parent_path)
        # Process subclasses and create YAML file
        parent_to_children_data = process_brick_classes(subclasses_df, parent_dir)
        
        # Print summary for this level
        for parent, children_data in parent_to_children_data.items():
            print(f"{parent}: {len(children_data)} direct subclasses")
        
        # Recursively process each subclass
        for _, row in subclasses_df.iterrows():
            subclass = row['brick_class']
            process_class_hierarchy(subclass, graph, parent_dir, processed_classes)
    
    return processed_classes

# %%
# Ensure templates directory exists
templates_dir = "templates"
os.makedirs(templates_dir, exist_ok=True)
print(f"Created directory: {templates_dir}")

# Start processing from the root parent class
processed_classes = process_class_hierarchy(start_parent, g, templates_dir)

# Print overall summary
print(f"\nOverall Summary:")
print(f"Processed {len(processed_classes)} unique classes in the hierarchy")
# %%
