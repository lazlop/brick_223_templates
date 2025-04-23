#!/usr/bin/env python3

"""
Script to review and edit YAML files in brick_yaml_autocomplete.
This script helps review and validate S223 mappings in Brick YAML files.
"""

import os
import sys
import argparse
from template_builder.review_yaml import review_and_edit_yaml

def main():
    parser = argparse.ArgumentParser(
        description='Review and edit YAML files in brick_yaml_autocomplete'
    )
    parser.add_argument(
        'yaml_file', 
        help='Path to the YAML file to review and edit'
    )
    args = parser.parse_args()
    
    # Check if the file exists
    if not os.path.isfile(args.yaml_file):
        print(f"Error: File '{args.yaml_file}' does not exist.")
        sys.exit(1)
    
    # Call the review_and_edit_yaml function
    review_and_edit_yaml(args.yaml_file)

if __name__ == '__main__':
    main()
