#!/usr/bin/env python3

"""
Module for reviewing and editing YAML files in brick_yaml_autocomplete.
This module provides functions to review and validate S223 mappings in Brick YAML files.
"""

import os
import yaml
import pandas as pd
from .get_s223_data import get_s223_info

def display_entity_info(entity_name, entity_data):
    """
    Display information about an entity.
    
    Args:
        entity_name (str): The name of the entity
        entity_data (dict): The entity data from the YAML file
    """
    print("=" * 94)
    print(f"Reviewing: {entity_name}")
    print(f"Definition: {entity_data.get('brick_definition', 'No definition available')}")
    print("=" * 94)
    print()

def display_s223_classes(prop_df):
    """
    Display available S223 classes.
    
    Args:
        prop_df (DataFrame): DataFrame containing S223 classes
    """
    print("\nAvailable S223 Classes:")
    print("-" * 80)
    for i, (s223_class, s223_definition) in enumerate(zip(prop_df['s223_class'], prop_df['s223_definition']), 1):
        print(f"{i}. {s223_class}: {s223_definition}")
    print("-" * 80)

def display_enumerationkinds(ek_df):
    """
    Display available enumeration kinds.
    
    Args:
        ek_df (DataFrame): DataFrame containing enumeration kinds
    """
    print("\nAvailable Enumeration Kinds:")
    print("-" * 80)
    for i, (ek, ek_definition) in enumerate(zip(ek_df['s223_class'], ek_df['s223_definition']), 1):
        print(f"{i}. {ek}: {ek_definition}")
    print("-" * 80)

def display_quantitykinds(qk_df):
    """
    Display available quantity kinds.
    
    Args:
        qk_df (DataFrame): DataFrame containing quantity kinds
    """
    print("\nAvailable Quantity Kinds:")
    print("-" * 80)
    for i, qk in enumerate(qk_df['s223_class'], 1):
        print(f"{i}. {qk}")
    print("-" * 80)

def display_media(media_df):
    """
    Display available media.
    
    Args:
        media_df (DataFrame): DataFrame containing media
    """
    print("\nAvailable Media:")
    print("-" * 80)
    for i, (medium, medium_definition) in enumerate(zip(media_df['s223_class'], media_df['s223_definition']), 1):
        print(f"{i}. {medium}: {medium_definition}")
    print("-" * 80)

def display_aspects(asp_df):
    """
    Display available aspects.
    
    Args:
        asp_df (DataFrame): DataFrame containing aspects
    """
    print("\nAvailable Aspects:")
    print("-" * 80)
    for i, (aspect, aspect_definition) in enumerate(zip(asp_df['s223_class'], asp_df['s223_definition']), 1):
        print(f"{i}. {aspect}: {aspect_definition}")
    print("-" * 80)

def display_property_of(meas_loc_df):
    """
    Display available property_of options.
    
    Args:
        meas_loc_df (DataFrame): DataFrame containing property_of options
    """
    print("\nAvailable Property Of Options:")
    print("-" * 80)
    for i, (prop_of, prop_of_definition) in enumerate(zip(meas_loc_df['s223_class'], meas_loc_df['s223_definition']), 1):
        print(f"{i}. {prop_of}: {prop_of_definition}")
    print("-" * 80)

def review_and_edit_s223_class(entity_data, prop_df):
    """
    Review and edit the S223 class of an entity.
    
    Args:
        entity_data (dict): The entity data from the YAML file
        prop_df (DataFrame): DataFrame containing S223 classes
        
    Returns:
        dict: The updated entity data
    """
    s223_class = entity_data.get('s223_class', 'None')
    is_valid = entity_data.get('s223_class_valid', False)
    
    print(f"S223 Class: {s223_class} (Valid: {is_valid})")
    
    view_options = input("Would you like to view available S223 classes? (y/n): ")
    if view_options.lower() == 'y':
        display_s223_classes(prop_df)
    
    change = input("Would you like to change the S223 class? (y/n): ")
    if change.lower() == 'y':
        new_s223_class = input("Enter new S223 class (or 'None' to clear): ")
        if new_s223_class.lower() == 'none':
            entity_data['s223_class'] = None
            entity_data['s223_class_valid'] = False
        else:
            entity_data['s223_class'] = new_s223_class
            # Validate the new S223 class
            entity_data['s223_class_valid'] = new_s223_class in prop_df['s223_class'].values
    
    return entity_data

def review_and_edit_enumerationkind(entity_data, ek_df):
    """
    Review and edit the enumeration kind of an entity.
    
    Args:
        entity_data (dict): The entity data from the YAML file
        ek_df (DataFrame): DataFrame containing enumeration kinds
        
    Returns:
        dict: The updated entity data
    """
    enumerationkind = entity_data.get('enumerationkind', 'None')
    is_valid = entity_data.get('enumerationkind_valid', False)
    
    print(f"Enumeration Kind: {enumerationkind} (Valid: {is_valid})")
    
    view_options = input("Would you like to view available enumeration kinds? (y/n): ")
    if view_options.lower() == 'y':
        display_enumerationkinds(ek_df)
    
    change = input("Would you like to change the enumeration kind? (y/n): ")
    if change.lower() == 'y':
        new_enumerationkind = input("Enter new enumeration kind (or 'None' to clear): ")
        if new_enumerationkind.lower() == 'none':
            entity_data['enumerationkind'] = None
            entity_data['enumerationkind_valid'] = False
        else:
            entity_data['enumerationkind'] = new_enumerationkind
            # Validate the new enumeration kind
            entity_data['enumerationkind_valid'] = new_enumerationkind in ek_df['s223_class'].values
    
    return entity_data

def review_and_edit_quantitykind(entity_data, qk_df):
    """
    Review and edit the quantity kind of an entity.
    
    Args:
        entity_data (dict): The entity data from the YAML file
        qk_df (DataFrame): DataFrame containing quantity kinds
        
    Returns:
        dict: The updated entity data
    """
    quantitykind = entity_data.get('quantitykind', 'None')
    is_valid = entity_data.get('quantitykind_valid', False)
    
    print(f"Quantity Kind: {quantitykind} (Valid: {is_valid})")
    
    view_options = input("Would you like to view available quantity kinds? (y/n): ")
    if view_options.lower() == 'y':
        display_quantitykinds(qk_df)
    
    change = input("Would you like to change the quantity kind? (y/n): ")
    if change.lower() == 'y':
        new_quantitykind = input("Enter new quantity kind (or 'None' to clear): ")
        if new_quantitykind.lower() == 'none':
            entity_data['quantitykind'] = None
            entity_data['quantitykind_valid'] = False
        else:
            entity_data['quantitykind'] = new_quantitykind
            # Validate the new quantity kind
            entity_data['quantitykind_valid'] = new_quantitykind in qk_df['s223_class'].values
    
    return entity_data

def review_and_edit_medium(entity_data, media_df):
    """
    Review and edit the medium of an entity.
    
    Args:
        entity_data (dict): The entity data from the YAML file
        media_df (DataFrame): DataFrame containing media
        
    Returns:
        dict: The updated entity data
    """
    medium = entity_data.get('medium', 'None')
    is_valid = entity_data.get('medium_valid', False)
    
    print(f"Medium: {medium} (Valid: {is_valid})")
    
    view_options = input("Would you like to view available media? (y/n): ")
    if view_options.lower() == 'y':
        display_media(media_df)
    
    change = input("Would you like to change the medium? (y/n): ")
    if change.lower() == 'y':
        new_medium = input("Enter new medium (or 'None' to clear): ")
        if new_medium.lower() == 'none':
            entity_data['medium'] = 'None'
            entity_data['medium_valid'] = True
        else:
            entity_data['medium'] = new_medium
            # Validate the new medium
            entity_data['medium_valid'] = new_medium in media_df['s223_class'].values
    
    return entity_data

def review_and_edit_aspects(entity_data, asp_df):
    """
    Review and edit the aspects of an entity.
    
    Args:
        entity_data (dict): The entity data from the YAML file
        asp_df (DataFrame): DataFrame containing aspects
        
    Returns:
        dict: The updated entity data
    """
    aspects = entity_data.get('aspects', [])
    is_valid = entity_data.get('aspects_valid', [])
    
    if isinstance(aspects, str):
        aspects = [aspects]
    if isinstance(is_valid, bool):
        is_valid = [is_valid]
    
    print(f"Aspects: {aspects}")
    print(f"Valid: {is_valid}")
    
    view_options = input("Would you like to view available aspects? (y/n): ")
    if view_options.lower() == 'y':
        display_aspects(asp_df)
    
    change = input("Would you like to change the aspects? (y/n): ")
    if change.lower() == 'y':
        new_aspects_str = input("Enter new aspects (comma-separated, or 'None' to clear): ")
        if new_aspects_str.lower() == 'none':
            entity_data['aspects'] = []
            entity_data['aspects_valid'] = []
        else:
            new_aspects = [aspect.strip() for aspect in new_aspects_str.split(',')]
            entity_data['aspects'] = new_aspects
            # Validate the new aspects
            entity_data['aspects_valid'] = [aspect in asp_df['s223_class'].values for aspect in new_aspects]
    
    return entity_data

def review_and_edit_property_of(entity_data, meas_loc_df):
    """
    Review and edit the property_of of an entity.
    
    Args:
        entity_data (dict): The entity data from the YAML file
        meas_loc_df (DataFrame): DataFrame containing property_of options
        
    Returns:
        dict: The updated entity data
    """
    property_of = entity_data.get('property_of', 'None')
    is_valid = entity_data.get('property_of_valid', False)
    
    print(f"Property Of: {property_of} (Valid: {is_valid})")
    
    view_options = input("Would you like to view available property_of options? (y/n): ")
    if view_options.lower() == 'y':
        display_property_of(meas_loc_df)
    
    change = input("Would you like to change the property_of? (y/n): ")
    if change.lower() == 'y':
        new_property_of = input("Enter new property_of (or 'None' to clear): ")
        if new_property_of.lower() == 'none':
            entity_data['property_of'] = 'None'
            entity_data['property_of_valid'] = True
        else:
            entity_data['property_of'] = new_property_of
            # Validate the new property_of
            entity_data['property_of_valid'] = new_property_of in meas_loc_df['s223_class'].values
    
    return entity_data

def review_and_edit_yaml(yaml_file):
    """
    Review and edit a YAML file.
    
    Args:
        yaml_file (str): Path to the YAML file to review and edit
    """
    # Load the YAML file
    with open(yaml_file, 'r') as f:
        data = yaml.safe_load(f)
    
    if not data:
        print(f"Error: No data found in {yaml_file}")
        return
    
    # Get S223 data
    prop_df, media_df, asp_df, ek_df, qk_df, meas_loc_df = get_s223_info()
    
    # Review and edit each entity in the YAML file
    for entity_name, entity_data in data.items():
        display_entity_info(entity_name, entity_data)
        
        # Review and edit S223 class
        entity_data = review_and_edit_s223_class(entity_data, prop_df)
        print()
        
        # Review and edit enumeration kind or quantity kind based on S223 class
        if entity_data.get('s223_class') and 'Enumerated' in entity_data.get('s223_class', ''):
            entity_data = review_and_edit_enumerationkind(entity_data, ek_df)
        else:
            entity_data = review_and_edit_quantitykind(entity_data, qk_df)
        print()
        
        # Review and edit medium
        entity_data = review_and_edit_medium(entity_data, media_df)
        print()
        
        # Review and edit aspects
        entity_data = review_and_edit_aspects(entity_data, asp_df)
        print()
        
        # Review and edit property_of
        entity_data = review_and_edit_property_of(entity_data, meas_loc_df)
        print()
        
        # Ask if the user wants to continue to the next entity
        if entity_name != list(data.keys())[-1]:  # If not the last entity
            continue_review = input("Continue to the next entity? (y/n): ")
            if continue_review.lower() != 'y':
                break
    
    # Save the updated YAML file
    save
