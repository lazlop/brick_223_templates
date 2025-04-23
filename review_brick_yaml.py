#!/usr/bin/env python3

"""
Script to review and edit Brick YAML files with S223 mappings.
"""

import os
import sys
import argparse
from template_builder.review_yaml import review_and_edit_yaml

def main():
    """
    Main function to parse arguments and call the review_and_edit_yaml function.
    """
    parser = argparse.ArgumentParser(description='Review and edit Brick YAML files with S223 mappings.')
    parser.add_argument('yaml_file', nargs='?', help='Path to the YAML file to review')
    parser.add_argument('--dir', '-d', help='Directory containing YAML files to review')
    
    args = parser.parse_args()
    
    if args.yaml_file:
        # Review a specific file
        if not os.path.exists(args.yaml_file):
            print(f"Error: File {args.yaml_file} does not exist")
            sys.exit(1)
        
        review_and_edit_yaml(args.yaml_file)
    elif args.dir:
        # Review all YAML files in a directory
        if not os.path.isdir(args.dir):
            print(f"Error: Directory {args.dir} does not exist")
            sys.exit(1)
        
        for root, dirs, files in os.walk(args.dir):
            for file in files:
                if file.endswith(".yml"):
                    template_file = os.path.join(root, file)
                    print(f"Template file: {template_file}")
                    review_and_edit_yaml(template_file)
    else:
        # No arguments provided, show usage
        parser.print_help()
        sys.exit(1)

if __name__ == '__main__':
    main()
