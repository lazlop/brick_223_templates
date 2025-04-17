#%%
import os 
from rdflib import Graph
import yaml 
from template_builder import (
    process_brick_template, 
    get_s223_info, 
    strip_namespace, 
    process_class_hierarchy
)

g = Graph()
g.parse("https://brickschema.org/schema/1.4.3/Brick.ttl", format = "ttl")
start_parent = "brick:Temperature_Sensor"
start_parent_clean = strip_namespace(start_parent)

# Ensure templates directory exists
templates_dir = "brick_yaml"
os.makedirs(templates_dir, exist_ok=True)
print(f"Created directory: {templates_dir}")

# Start processing from the root parent class
processed_classes = process_class_hierarchy(start_parent, g, templates_dir)

# Print overall summary
print(f"\nOverall Summary:")
print(f"Processed {len(processed_classes)} unique classes in the hierarchy")
# %%

s223_properties, s223_media, s223_aspects, s223_eks, quantitykinds, prop_df, media_df, asp_df, ek_df, qk_df = get_s223_info()

template_dir = "brick_yaml"
new_dir = "brick_yaml_autocomplete"
for root, dirs, files in os.walk(template_dir):
    for file in files:
        if file.endswith(".yml"):
            template_file = os.path.join(root, file)
            process_brick_template(template_file, new_dir, s223_properties, s223_media, s223_aspects, s223_eks, quantitykinds, prop_df, media_df, asp_df, ek_df, qk_df)
            print(f"Template file: {template_file}")

# %%
