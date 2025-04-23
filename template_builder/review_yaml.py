#!/usr/bin/env python3

"""
Module for reviewing and editing YAML files containing Brick classes and their S223 mappings.
"""

import os
import yaml
import sys
from .get_s223_data import get_s223_info
import pandas as pd

def display_s223_info(df, column_name='s223_class'):
    """
    Display S223 information from a DataFrame.
    
    Args:
        df (DataFrame): DataFrame containing S223 information
        column_name (str): Column name to display
    """
    print(f"\nAvailable {column_name} options:")
    for i, (idx, row) in enumerate(df.iterrows(), 1):
        class_name = row[column_name]
        definition = row.get('s223_definition', '')
        print(f"{i}. {class_name}: {definition[:100]}{'...' if len(definition) > 100 else ''}")

def select_from_df(df, prompt, column_name='s223_class', allow_none=True):
    """
    Allow user to select an item from a DataFrame.
    
    Args:
        df (DataFrame): DataFrame containing items to select from
        prompt (str): Prompt to display to the user
        column_name (str): Column name to display and select from
        allow_none (bool): Whether to allow selecting None
        
    Returns:
        str: Selected item or None if none selected
    """
    while True:
        try:
            choice = input(prompt)
            if choice.lower() == 'q':
                return None
            if choice.lower() == 'v':
                display_s223_info(df, column_name)
                continue
            
            if allow_none and (choice.lower() == 'none' or choice == ''):
                return None
            
            choice = int(choice)
            if 1 <= choice <= len(df):
                return df.iloc[choice-1][column_name]
            else:
                print(f"Invalid choice. Please enter a number between 1 and {len(df)}")
        except ValueError:
            print("Invalid input. Please enter a number, 'v' to view options, 'q' to quit, or 'none' for None.")

def review_and_edit_s223_class(brick_class, definition_data, prop_df):
    """
    Review and edit the s223_class field.
    
    Args:
        brick_class (str): The Brick class name
        definition_data (dict): The definition data for the Brick class
        prop_df (DataFrame): DataFrame containing S223 property information
        
    Returns:
        dict: Updated definition data
    """
    print("\n" + "="*80)
    print(f"Reviewing s223_class for {brick_class}")
    print("="*80)
    
    current_s223_class = definition_data.get('s223_class', 'None')
    is_valid = definition_data.get('s223_class_valid', False)
    
    print(f"Current s223_class: {current_s223_class}")
    print(f"Is valid: {is_valid}")
    
    while True:
        print("\nOptions:")
        print("1. Keep current s223_class")
        print("2. Change s223_class")
        print("3. Set to None")
        
        choice = input("Enter your choice (1-3): ")
        
        if choice == '1':
            return definition_data
        elif choice == '2':
            view_options = input("Would you like to view available s223 classes? (y/n): ")
            if view_options.lower() == 'y':
                display_s223_info(prop_df)
            
            prompt = "\nEnter the number of the s223_class to use (v to view options, q to quit): "
            new_s223_class = select_from_df(prop_df, prompt)
            
            if new_s223_class is not None:
                definition_data['s223_class'] = new_s223_class
                definition_data['s223_class_valid'] = True
            return definition_data
        elif choice == '3':
            definition_data['s223_class'] = None
            definition_data['s223_class_valid'] = False
            return definition_data
        else:
            print("Invalid choice. Please enter a number between 1 and 3.")

def review_and_edit_quantitykind(brick_class, definition_data, qk_df):
    """
    Review and edit the quantitykind field.
    
    Args:
        brick_class (str): The Brick class name
        definition_data (dict): The definition data for the Brick class
        qk_df (DataFrame): DataFrame containing quantitykind information
        
    Returns:
        dict: Updated definition data
    """
    print("\n" + "="*80)
    print(f"Reviewing quantitykind for {brick_class}")
    print("="*80)
    
    current_quantitykind = definition_data.get('quantitykind', 'None')
    is_valid = definition_data.get('quantitykind_valid', False)
    
    print(f"Current quantitykind: {current_quantitykind}")
    print(f"Is valid: {is_valid}")
    
    while True:
        print("\nOptions:")
        print("1. Keep current quantitykind")
        print("2. Change quantitykind")
        print("3. Set to None")
        
        choice = input("Enter your choice (1-3): ")
        
        if choice == '1':
            return definition_data
        elif choice == '2':
            view_options = input("Would you like to view available quantity kinds? (y/n): ")
            if view_options.lower() == 'y':
                display_s223_info(qk_df, 's223_class')
            
            prompt = "\nEnter the number of the quantitykind to use (v to view options, q to quit): "
            new_quantitykind = select_from_df(qk_df, prompt, 's223_class')
            
            if new_quantitykind is not None:
                definition_data['quantitykind'] = new_quantitykind
                definition_data['quantitykind_valid'] = True
                # Clear enumerationkind if quantitykind is set
                if 'enumerationkind' in definition_data:
                    definition_data['enumerationkind'] = None
                    definition_data['enumerationkind_valid'] = False
            return definition_data
        elif choice == '3':
            definition_data['quantitykind'] = None
            definition_data['quantitykind_valid'] = False
            return definition_data
        else:
            print("Invalid choice. Please enter a number between 1 and 3.")

def review_and_edit_enumerationkind(brick_class, definition_data, ek_df):
    """
    Review and edit the enumerationkind field.
    
    Args:
        brick_class (str): The Brick class name
        definition_data (dict): The definition data for the Brick class
        ek_df (DataFrame): DataFrame containing enumerationkind information
        
    Returns:
        dict: Updated definition data
    """
    print("\n" + "="*80)
    print(f"Reviewing enumerationkind for {brick_class}")
    print("="*80)
    
    current_enumerationkind = definition_data.get('enumerationkind', 'None')
    is_valid = definition_data.get('enumerationkind_valid', False)
    
    print(f"Current enumerationkind: {current_enumerationkind}")
    print(f"Is valid: {is_valid}")
    
    while True:
        print("\nOptions:")
        print("1. Keep current enumerationkind")
        print("2. Change enumerationkind")
        print("3. Set to None")
        
        choice = input("Enter your choice (1-3): ")
        
        if choice == '1':
            return definition_data
        elif choice == '2':
            view_options = input("Would you like to view available enumeration kinds? (y/n): ")
            if view_options.lower() == 'y':
                display_s223_info(ek_df)
            
            prompt = "\nEnter the number of the enumerationkind to use (v to view options, q to quit): "
            new_enumerationkind = select_from_df(ek_df, prompt)
            
            if new_enumerationkind is not None:
                definition_data['enumerationkind'] = new_enumerationkind
                definition_data['enumerationkind_valid'] = True
                # Clear quantitykind if enumerationkind is set
                if 'quantitykind' in definition_data:
                    definition_data['quantitykind'] = None
                    definition_data['quantitykind_valid'] = False
            return definition_data
        elif choice == '3':
            definition_data['enumerationkind'] = None
            definition_data['enumerationkind_valid'] = False
            return definition_data
        else:
            print("Invalid choice. Please enter a number between 1 and 3.")

def review_and_edit_medium(brick_class, definition_data, media_df):
    """
    Review and edit the medium field.
    
    Args:
        brick_class (str): The Brick class name
        definition_data (dict): The definition data for the Brick class
        media_df (DataFrame): DataFrame containing medium information
        
    Returns:
        dict: Updated definition data
    """
    print("\n" + "="*80)
    print(f"Reviewing medium for {brick_class}")
    print("="*80)
    
    current_medium = definition_data.get('medium', 'None')
    is_valid = definition_data.get('medium_valid', False)
    
    print(f"Current medium: {current_medium}")
    print(f"Is valid: {is_valid}")
    
    while True:
        print("\nOptions:")
        print("1. Keep current medium")
        print("2. Change medium")
        print("3. Set to None")
        
        choice = input("Enter your choice (1-3): ")
        
        if choice == '1':
            return definition_data
        elif choice == '2':
            view_options = input("Would you like to view available media? (y/n): ")
            if view_options.lower() == 'y':
                display_s223_info(media_df)
            
            prompt = "\nEnter the number of the medium to use (v to view options, q to quit): "
            new_medium = select_from_df(media_df, prompt)
            
            if new_medium is not None:
                definition_data['medium'] = new_medium
                definition_data['medium_valid'] = True
            return definition_data
        elif choice == '3':
            definition_data['medium'] = None
            definition_data['medium_valid'] = False
            return definition_data
        else:
            print("Invalid choice. Please enter a number between 1 and 3.")

def review_and_edit_aspects(brick_class, definition_data, asp_df):
    """
    Review and edit the aspects field.
    
    Args:
        brick_class (str): The Brick class name
        definition_data (dict): The definition data for the Brick class
        asp_df (DataFrame): DataFrame containing aspect information
        
    Returns:
        dict: Updated definition data
    """
    print("\n" + "="*80)
    print(f"Reviewing aspects for {brick_class}")
    print("="*80)
    
    current_aspects = definition_data.get('aspects', [])
    if isinstance(current_aspects, str):
        if current_aspects.lower() == 'none':
            current_aspects = []
        else:
            current_aspects = [aspect.strip() for aspect in current_aspects.split(',')]
    
    is_valid = definition_data.get('aspects_valid', False)
    
    print(f"Current aspects: {', '.join(current_aspects) if current_aspects else 'None'}")
    print(f"Is valid: {is_valid}")
    
    while True:
        print("\nOptions:")
        print("1. Keep current aspects")
        print("2. Change aspects")
        print("3. Set to None")
        
        choice = input("Enter your choice (1-3): ")
        
        if choice == '1':
            return definition_data
        elif choice == '2':
            view_options = input("Would you like to view available aspects? (y/n): ")
            if view_options.lower() == 'y':
                display_s223_info(asp_df)
            
            new_aspects = []
            print("\nEnter the numbers of the aspects to use, one at a time.")
            print("Press Enter with no input when done, 'v' to view options, 'q' to quit.")
            
            while True:
                prompt = f"Aspect {len(new_aspects) + 1} (Enter to finish): "
                new_aspect = select_from_df(asp_df, prompt, allow_none=True)
                
                if new_aspect is None:
                    if len(new_aspects) == 0:
                        print("No aspects selected.")
                    break
                
                new_aspects.append(new_aspect)
                print(f"Added aspect: {new_aspect}")
            
            definition_data['aspects'] = new_aspects
            definition_data['aspects_valid'] = True if new_aspects else False
            return definition_data
        elif choice == '3':
            definition_data['aspects'] = []
            definition_data['aspects_valid'] = False
            return definition_data
        else:
            print("Invalid choice. Please enter a number between 1 and 3.")

def review_and_edit_property_of(brick_class, definition_data, meas_loc_df):
    """
    Review and edit the property_of field.
    
    Args:
        brick_class (str): The Brick class name
        definition_data (dict): The definition data for the Brick class
        meas_loc_df (DataFrame): DataFrame containing property_of information
        
    Returns:
        dict: Updated definition data
    """
    print("\n" + "="*80)
    print(f"Reviewing property_of for {brick_class}")
    print("="*80)
    
    current_property_of = definition_data.get('property_of', 'None')
    is_valid = definition_data.get('property_of_valid', False)
    
    print(f"Current property_of: {current_property_of}")
    print(f"Is valid: {is_valid}")
    
    while True:
        print("\nOptions:")
        print("1. Keep current property_of")
        print("2. Change property_of")
        print("3. Set to None")
        
        choice = input("Enter your choice (1-3): ")
        
        if choice == '1':
            return definition_data
        elif choice == '2':
            view_options = input("Would you like to view available property_of options? (y/n): ")
            if view_options.lower() == 'y':
                display_s223_info(meas_loc_df)
            
            prompt = "\nEnter the number of the property_of to use (v to view options, q to quit): "
            new_property_of = select_from_df(meas_loc_df, prompt)
            
            if new_property_of is not None:
                definition_data['property_of'] = new_property_of
                definition_data['property_of_valid'] = True
            return definition_data
        elif choice == '3':
            definition_data['property_of'] = None
            definition_data['property_of_valid'] = False
            return definition_data
        else:
            print("Invalid choice. Please enter a number between 1 and 3.")

def add_note_to_entity(brick_class, definition_data):
    """
    Add a note to a Brick entity.
    
    Args:
        brick_class (str): The Brick class name
        definition_data (dict): The definition data for the Brick class
        
    Returns:
        dict: Updated definition data with note
    """
    print("\n" + "="*80)
    print(f"Add note for {brick_class}")
    print("="*80)
    
    current_note = definition_data.get('note', '')
    
    print(f"Current note: {current_note}")
    
    while True:
        print("\nOptions:")
        print("1. Keep current note")
        print("2. Add/Edit note")
        print("3. Remove note")
        
        choice = input("Enter your choice (1-3): ")
        
        if choice == '1':
            return definition_data
        elif choice == '2':
            print("\nEnter your note (press Enter twice to finish):")
            lines = []
            while True:
                line = input()
                if not line and (not lines or not lines[-1]):
                    break
                lines.append(line)
            
            new_note = '\n'.join(lines)
            if new_note:
                definition_data['note'] = new_note
            return definition_data
        elif choice == '3':
            if 'note' in definition_data:
                del definition_data['note']
            return definition_data
        else:
            print("Invalid choice. Please enter a number between 1 and 3.")

def review_and_edit_yaml(yaml_file):
    """
    Review and edit a YAML file containing Brick classes and their S223 mappings.
    
    Args:
        yaml_file (str): Path to the YAML file to review
    """
    print(f"\nReviewing YAML file: {yaml_file}")
    
    # Load the YAML file
    try:
        with open(yaml_file, 'r') as f:
            brick_dict = yaml.safe_load(f)
    except Exception as e:
        print(f"Error loading YAML file: {e}")
        return
    
    if not brick_dict:
        print("YAML file is empty or invalid")
        return
    
    # Get S223 data
    try:
        prop_df, media_df, asp_df, ek_df, qk_df, meas_loc_df = get_s223_info()
    except Exception as e:
        print(f"Error retrieving S223 data: {e}")
        return
    
    # Process each brick class
    updated_brick_dict = {}
    for brick_class, definition_data in brick_dict.items():
        print("\n" + "="*80)
        print(f"Reviewing brick class: {brick_class}")
        print("="*80)
        
        # Extract the definition text
        if isinstance(definition_data, dict):
            # Keep the original structure
            updated_definition_data = definition_data.copy()
            text_definition = definition_data.get('brick_definition', '')
        else:
            # If it's just a string, create a dictionary
            text_definition = definition_data
            updated_definition_data = {'brick_definition': text_definition}
        
        print(f"Brick definition: {text_definition}")
        
        # Review and edit each field
        updated_definition_data = review_and_edit_s223_class(brick_class, updated_definition_data, prop_df)
        
        # Check if quantitykind or enumerationkind is set
        if updated_definition_data.get('quantitykind'):
            updated_definition_data = review_and_edit_quantitykind(brick_class, updated_definition_data, qk_df)
        elif updated_definition_data.get('enumerationkind'):
            updated_definition_data = review_and_edit_enumerationkind(brick_class, updated_definition_data, ek_df)
        else:
            # Ask which one to set
            print("\n" + "="*80)
            print(f"Neither quantitykind nor enumerationkind is set for {brick_class}")
            print("="*80)
            
            while True:
                print("\nOptions:")
                print("1. Set quantitykind")
                print("2. Set enumerationkind")
                print("3. Leave both unset")
                
                choice = input("Enter your choice (1-3): ")
                
                if choice == '1':
                    updated_definition_data = review_and_edit_quantitykind(brick_class, updated_definition_data, qk_df)
                    break
                elif choice == '2':
                    updated_definition_data = review_and_edit_enumerationkind(brick_class, updated_definition_data, ek_df)
                    break
                elif choice == '3':
                    break
                else:
                    print("Invalid choice. Please enter a number between 1 and 3.")
        
        updated_definition_data = review_and_edit_medium(brick_class, updated_definition_data, media_df)
        updated_definition_data = review_and_edit_aspects(brick_class, updated_definition_data, asp_df)
        updated_definition_data = review_and_edit_property_of(brick_class, updated_definition_data, meas_loc_df)
        
        # Add note to the entity
        updated_definition_data = add_note_to_entity(brick_class, updated_definition_data)
        
        # Add the updated definition to the dictionary
        updated_brick_dict[brick_class] = updated_definition_data
    
    # Write the updated dictionary back to the YAML file
    try:
        with open(yaml_file, 'w') as f:
            yaml.dump(updated_brick_dict, f, default_flow_style=False, sort_keys=False)
        print(f"\nUpdated {yaml_file} with edited S223 mappings")
    except Exception as e:
        print(f"Error writing YAML file: {e}")
