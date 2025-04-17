#%%
import os 
from rdflib import Graph
import yaml 
from template_builder import (
    process_brick_template, 
    get_s223_info, 
    strip_namespace, 
    process_class_hierarchy,
    process_directory,
    process_yaml_file
)
# %% 

prop_df, media_df, asp_df, ek_df, qk_df, meas_loc_df= get_s223_info()
#%%
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

#running autocomplete
#%%
template_dir = "brick_yaml"
# have to copy brick_yaml (or parts of brick_yaml I want to complete) to brick_yaml_autocomplete
# currently doing this to limit AI usage.
new_dir = "brick_yaml_autocomplete"
for root, dirs, files in os.walk(template_dir):
    for file in files:
        if file.endswith(".yml"):
            template_file = os.path.join(root, file)
            process_brick_template(template_file, new_dir,prop_df, media_df, asp_df, ek_df, qk_df, meas_loc_df)
            print(f"Template file: {template_file}")

# %%
input_dir = os.path.join('brick_yaml_reviewed', 'brick_yaml')
output_dir = 's223_templates'
os.makedirs(output_dir, exist_ok=True)

# Process all YAML files in the input directory
process_directory(input_dir, output_dir)

print(f"Templates generated in {output_dir}")

# cost estimate
# %%
import tiktoken

enc = tiktoken.encoding_for_model("gpt-4o")
example_prompt = """Determine what quantitykind or enumerationkind the brick_class should be, based on its name and definition.
        the possible quantitykinds are <quantitykinds>{df_to_csv_str(qk_df)}</quantitykinds> 
        the possible enumerationkinds are <s223_eks>{df_to_csv_str(ek_df)}</s223_eks>
        Only return the quantitykind or enumerationkind. Do not return any other information.

        brick_class: {brick_class}
        definition: {text_definition}"""
input_data = ('\n'.join([prop_df.to_csv(index=False), media_df.to_csv(index=False), asp_df.to_csv(index=False), ek_df.to_csv(index=False), qk_df.to_csv(index=False), meas_loc_df.to_csv(index=False)]))

approximate_completion = 's223:Aspect-DryBulb, s223:Aspect-WetBulb, s223:Medium-Water, s223:QuantifiableObservableProperty, s223:Temperature'

prompt_encoded = enc.encode((example_prompt * 5 + input_data) * len(processed_classes))
completion_encoded = enc.encode(approximate_completion * len(processed_classes))

input_cost = 3
output_cost = 15

prompt_cost = len(prompt_encoded) / 1_000_000 * 3
completion_cost = len(completion_encoded) / 1_000_000 * 15
print(f"{prompt_cost} + {completion_cost} = {prompt_cost + completion_cost}")
