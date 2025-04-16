#!/usr/bin/env python3
#%%
from rdflib import Graph
from utils import * 
from namespaces import * 
from get_completion import get_completion
import yaml
import os
import pandas as pd
import csv
from io import StringIO

def get_s223_info(g: Graph):
    # Get properties
    prop_query = """ SELECT DISTINCT ?s223_class ?s223_definition WHERE {
        ?s223_class rdfs:subClassOf* s223:Property ;
        rdfs:comment ?s223_definition .
        FILTER NOT EXISTS {
            ?s223_class qudt:hasQuantityKind ?qk .
        }
    }
    """
    prop_df = query_to_df(prop_query, s223)
    s223_properties = prop_df.to_csv(index=False)
    
    # Get Media
    med_query = """ SELECT DISTINCT ?s223_class ?s223_definition WHERE {
        ?s223_class rdfs:subClassOf* s223:EnumerationKind-Substance ;
        rdfs:comment ?s223_definition .
        FILTER NOT EXISTS {
            {
                ?s223_class rdfs:subClassOf+ s223:Electricity-DC .
            }
            UNION
            {
                ?s223_class rdfs:subClassOf+ s223:Electricity-AC .
            }
        }
    }
    """
    media_df = query_to_df(med_query, s223)
    s223_media = media_df.to_csv(index=False)
    
    # Get Aspects

    # looking at everything that could be an aspect 
    # asp_query = """ SELECT DISTINCT ?s223_class ?s223_definition WHERE {
    #     ?s223_class rdfs:subClassOf* s223:EnumerationKind .
    #     ?s223_class rdfs:comment ?s223_definition .
      
    #     FILTER NOT EXISTS {        
    #         ?s223_class rdfs:subClassOf* s223:EnumerationKind-Substance .
    #     }
    #     # Excluding all the voltages
    #     FILTER NOT EXISTS {        
    #         ?s223_class rdfs:subClassOf* s223:EnumerationKind-Numerical .
    #     }
    #     FILTER NOT EXISTS {        
    #         ?s223_class rdfs:subClassOf* s223:EnumerationKind-ElectricalPhaseIdentifier .
    #     }
    #     FILTER NOT EXISTS {        
    #         ?s223_class rdfs:subClassOf* s223:EnumerationKind-ElectricalVoltagePhases .
    #     }
    #     FILTER NOT EXISTS {        
    #         ?s223_class rdfs:subClassOf* s223:EnumerationKind-DayOfWeek .
    #     }
    # }
    # """

    # looking only at aspects
    asp_query = """ SELECT DISTINCT ?s223_class ?s223_definition WHERE {
        ?s223_class rdfs:subClassOf* s223:EnumerationKind-Aspect .
        ?s223_class rdfs:comment ?s223_definition .
      
        FILTER NOT EXISTS {        
            ?s223_class rdfs:subClassOf* s223:EnumerationKind-Substance .
        }
        # Excluding all the voltages
        FILTER NOT EXISTS {        
            ?s223_class rdfs:subClassOf* s223:EnumerationKind-Numerical .
        }
        FILTER NOT EXISTS {        
            ?s223_class rdfs:subClassOf* s223:EnumerationKind-ElectricalPhaseIdentifier .
        }
        FILTER NOT EXISTS {        
            ?s223_class rdfs:subClassOf* s223:EnumerationKind-ElectricalVoltagePhases .
        }
        FILTER NOT EXISTS {        
            ?s223_class rdfs:subClassOf* s223:EnumerationKind-DayOfWeek .
        }
    }
    """
    asp_df = query_to_df(asp_query, s223)
    s223_aspects = asp_df.to_csv(index=False)
    
    # Get EnumerationKind
    ek_query = """ SELECT DISTINCT ?s223_class ?s223_definition WHERE {
        ?s223_class rdfs:subClassOf+ s223:EnumerationKind .
        ?s223_class rdfs:comment ?s223_definition .
      
        FILTER NOT EXISTS {        
            ?s223_class rdfs:subClassOf* s223:EnumerationKind-Substance .
        }
        # Excluding all the voltages
        FILTER NOT EXISTS {        
            ?s223_class rdfs:subClassOf* s223:EnumerationKind-Numerical .
        }
        FILTER NOT EXISTS {        
            ?s223_class rdfs:subClassOf* s223:EnumerationKind-ElectricalPhaseIdentifier .
        }
        FILTER NOT EXISTS {        
            ?s223_class rdfs:subClassOf* s223:EnumerationKind-ElectricalVoltagePhases .
        }
        FILTER NOT EXISTS {        
            ?s223_class rdfs:subClassOf* s223:EnumerationKind-DayOfWeek .
        }
        FILTER NOT EXISTS {        
            ?s223_class rdfs:subClassOf* s223:EnumerationKind-Aspect .
        }
        FILTER NOT EXISTS {        
            ?s223_class rdfs:subClassOf* s223:EnumerationKind-Role .
        }
        FILTER NOT EXISTS {        
            ?s223_class rdfs:subClassOf* s223:EnumerationKind-Domain .
        }
    }
    """
    ek_df = query_to_df(ek_query, s223)
    s223_eks = ek_df.to_csv(index=False)
    
    # Convert quantitykinds to dataframe for validation
    qk_df = pd.read_csv("quantitykinds.csv")
    quantitykinds = qk_df.to_csv(index=False)
    
    return s223_properties, s223_media, s223_aspects, s223_eks, quantitykinds,prop_df, media_df, asp_df, ek_df, qk_df

s223 = Graph()
s223.parse("https://open223.info/223p.ttl", format="ttl")
bind_prefixes(s223)

s223_properties, s223_media, s223_aspects, s223_eks, quantitykinds, prop_df, media_df, asp_df, ek_df, qk_df = get_s223_info(s223)
def validate_result(result, df, column_name='s223_class'):
    """
    Validate if a result is in the provided dataframe.
    
    Args:
        result (str): The result to validate
        df (DataFrame): The dataframe to check against
        column_name (str): The column name to check in
        
    Returns:
        bool: True if the result is in the dataframe, False otherwise
    """
    result = result.strip()
    return (result in df[column_name].values)

def process_brick_template(template_file):
    """
    Process a Brick template file, running prompts on each brick class and definition
    and updating the YAML file with the results.
    
    Args:
        template_file (str): Path to the template YAML file
    """
    print(f"Processing template file: {template_file}")

    
    # Load the brick template
    with open(template_file, "r") as f:
        brick_dict = yaml.safe_load(f)
    
    # Process each brick class and definition
    system_prompt = """"""
    updated_brick_dict = {}
    
    for brick_class, definition_data in brick_dict.items():
        print(f"Processing brick_class: {brick_class}")
        
        # Extract the definition text
        if isinstance(definition_data, dict):
            # Keep the original structure
            updated_definition_data = definition_data.copy()
            text_definition = definition_data.get('brick_definition', '')
        else:
            # If it's just a string, create a dictionary
            text_definition = definition_data
            updated_definition_data = {'brick_definition': text_definition}
        
        # Prompt 1: Determine s223_class
        prompt1 = f"""
        Determine what s223_class the brick_class should be, based on its name and definition.
        the possible s223 classes are <s223_properties>{s223_properties}</s223_properties> 

        Only return the s223_class. Do not return any other information.

        brick_class: {brick_class}
        definition: {text_definition}
        """
        s223_class_result = get_completion(prompt1, system_prompt)
        s223_class_result = s223_class_result.strip()
        print(f"s223_class: {s223_class_result}")
        
        # Validate s223_class result
        is_valid_s223_class = validate_result(s223_class_result, prop_df)
        print(f"Is valid s223_class: {is_valid_s223_class}")
        
        updated_definition_data['s223_class'] = s223_class_result
        updated_definition_data['s223_class_valid'] = is_valid_s223_class
        
        # Prompt 2: Determine quantitykind or enumerationkind
        prompt2 = f"""
        Determine what quantitykind or enumerationkind the brick_class should be, based on its name and definition.
        the possible quantitykinds are <quantitykinds>{quantitykinds}</quantitykinds> 
        the possible enumerationkinds are <s223_eks>{s223_eks}</s223_eks>
        Only return the quantitykind or enumerationkind. Do not return any other information.

        brick_class: {brick_class}
        definition: {text_definition}
        """
        qk_ek_result = get_completion(prompt2, system_prompt)
        qk_ek_result = qk_ek_result.strip()
        print(f"quantitykind/enumerationkind: {qk_ek_result}")
        
        # Check if result is in quantitykind or enumerationkind list
        is_quantitykind = qk_ek_result in qk_df['quantitykinds'].values
        is_enumerationkind = validate_result(qk_ek_result, ek_df)
        
        qk_ek_type = "None"
        if is_quantitykind:
            updated_definition_data['quantitykind'] = qk_ek_result
            updated_definition_data['quantitykind_valid'] = True
        elif is_enumerationkind:
            updated_definition_data['enumerationkind'] = qk_ek_result
            updated_definition_data['enumerationkind_valid'] = True
        else:
            print(f"Warning: {qk_ek_result} not found in quantitykind or enumerationkind lists")
            updated_definition_data['quantitykind_valid'] = False
            updated_definition_data['enumerationkind_valid'] = False
            updated_definition_data['quantitykind'] = qk_ek_result
        
        # Prompt 3: Determine medium
        prompt3 = f"""
        Determine what medium the brick_class should be associated with, based on its name and definition.
        the possible media are <media>{s223_media}</media> 
        Only return the medium. Do not return any other information.

        If there is no sensible medium, return None.

        brick_class: {brick_class}
        definition: {text_definition}
        """
        medium_result = get_completion(prompt3, system_prompt)
        medium_result = medium_result.strip()
        print(f"medium: {medium_result}")
        
        # Validate medium result
        if medium_result.lower() == "none":
            is_valid_medium = True
            print("No medium specified")
        else:
            is_valid_medium = validate_result(medium_result, media_df)
            print(f"Is valid medium: {is_valid_medium}")
        
        updated_definition_data['medium'] = medium_result
        updated_definition_data['medium_valid'] = is_valid_medium
        
        # Prompt 4: Determine aspects
        prompt4 = f"""
        Determine what aspects the brick_class should be associated with, based on its name and definition.
        The possible aspects are <aspects>{s223_aspects}</aspects> 
        If there are no directly applicable aspects, return None.
        Only return the aspects as a comma separated list. Do not return any other information.

        brick_class: {brick_class}
        definition: {text_definition}
        """
        aspects_result = get_completion(prompt4, system_prompt)
        aspects_result = aspects_result.strip()
        print(f"aspects: {aspects_result}")
        
        # Validate aspects result
        is_valid_aspects = True
        for aspect in aspects_result.split(","):
            print(f"Validating aspect: {aspect}")
            is_valid_aspect = validate_result(aspect, asp_df)
            if is_valid_aspect == False:
                print(f"Warning: {aspect} not found in aspect list")
            else:
                print(f"Is valid aspect: {is_valid_aspects}")
            is_valid_aspects = is_valid_aspects and is_valid_aspect
        
        updated_definition_data['aspects'] = aspects_result
        updated_definition_data['aspects_valid'] = is_valid_aspects
        
        # Add the updated definition to the dictionary
        updated_brick_dict[brick_class] = updated_definition_data
    
    # Write the updated dictionary back to the YAML file
    with open(os.path.join('brick_yaml_autocomplete', template_file), "w") as f:
        yaml.dump(updated_brick_dict, f, default_flow_style=False, sort_keys=False)
    
    print(f"Updated {template_file} with s223 mappings")

#%%

template_dir = "templates"
for root, dirs, files in os.walk(template_dir):
    for file in files:
        if file.endswith(".yml"):
            template_file = os.path.join(root, file)
            process_brick_template(template_file)
            print(f"Template file: {template_file}")

# %%
