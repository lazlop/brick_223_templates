# Brick to S223 Templates

A tool for converting Brick ontology classes to ASHRAE Standard 223 (S223) templates.

## Overview

This project provides a workflow for converting Brick ontology classes to ASHRAE Standard 223 (S223) templates. The process involves:

1. Extracting Brick classes and their hierarchies from the Brick ontology
2. Creating YAML representations of these classes
3. Enhancing the YAML files with S223-specific information using an LLM
4. Reviewing the LLM provided yaml files by hand
5. Generating S223 BuildingMOTIF templates

## Installation

### Prerequisites

- Python 3.10
- [uv](https://github.com/astral-sh/uv) (Python package manager)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/brick-to-223-templates.git
   cd brick-to-223-templates
   ```

2. Install dependencies:
   ```bash
   uv sync
   ```

## Project Structure

- `brick_yaml/`: Initial YAML files extracted from Brick ontology
- `brick_yaml_autocomplete/`: AI-enhanced YAML files (automatically generated)
- `brick_yaml_reviewed/`: AI-enhanced YAML files after manual review
- `s223_templates/`: Generated S223 templates in yaml format
- `quantitykinds.csv`: Reference quantitykinds that are applicable to buildings
- `namespaces.py`: Namespace definitions for RDF processing
- `utils.py`: Utility functions for RDF processing
- `create_yaml_brick.py`: Script to extract Brick classes and create YAML files
- `ai_complete_yaml.py`: Script to enhance YAML files with S223 information using AI
- `get_completion.py`: Utility for AI completions
- `main.py`: runs through workflow of creating yaml structure, completing it using an LLM, and turning those into templates

## Workflow

### 1. Create Brick YAML Files

Extract Brick classes and create YAML representations:

```bash
python create_yaml_brick.py
```

This script:
- Parses the Brick ontology
- Extracts class hierarchies starting from a specified parent class (e.g., "Temperature_Sensor")
- Creates YAML files with class information in the `brick_yaml/` directory

### 2. Enhance YAML Files with S223 Information

Use AI to enhance the YAML files with S223-specific information:

```bash
python ai_complete_yaml.py
```

This script:
- Processes each YAML file in the `brick_yaml/` directory
- Uses AI to determine appropriate S223 classes, quantity kinds, media, and aspects
- Validates the AI-generated information against S223 ontology
- Saves the enhanced YAML files to `brick_yaml_autocomplete/`

The schema used in this YAML may also be useful for "flattening" 223P graphs into a tag-based structure for storage in tabular databases. This will be explored more in the future.

### 3. Review and Refine (Manual Step)

Review the AI-enhanced YAML files and make any necessary corrections:
- Copy files from `brick_yaml_autocomplete/` to `brick_yaml_reviewed/`
- Manually review and edit the files as needed

### 4. Generate S223 Templates

Convert the reviewed YAML files to S223 templates:

```bash
python -m src.brick_to_223_templates.create_223_templates
```

This script:
- Processes each YAML file in the `brick_yaml_reviewed/` directory
- Creates S223 templates in Turtle (TTL) format
- Saves the templates to `s223_templates/`

## S223 Template Structure

The generated S223 templates include:
- RDF type based on the S223 class
- Quantity kind for quantifiable properties
- Enumeration kind for enumerable properties
- Medium information (e.g., air, water)
- Aspect information (e.g., dry bulb, wet bulb)

## Example

A Brick class like "Water_Temperature_Sensor" is converted to an S223 template with:
- Type: s223:QuantifiableObservableProperty
- Quantity kind: Temperature
- Medium: s223:Fluid-Water
- Aspects: s223:Aspect-DryBulb, s223:Aspect-WetBulb

## Contributing

## License

This project is licensed under the [BSD3](LICENSE).
