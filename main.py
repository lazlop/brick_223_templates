#%%
import os 
from rdflib import Graph
import yaml 
import shutil
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

#%%
template_dir = "brick_yaml"
new_dir = "brick_yaml_autocomplete"
#%%
# have to copy brick_yaml (or parts of brick_yaml I want to complete) to brick_yaml_autocomplete
# Could limit AI usage to certain files this way.
os.makedirs(new_dir, exist_ok=True)
shutil.copytree(template_dir, new_dir, dirs_exist_ok=True)
#running autocomplete
#%%
for root, dirs, files in os.walk(new_dir):
    for file in files:
        if file.endswith(".yml"):
            template_file = os.path.join(root, file)
            process_brick_template(template_file, prop_df, media_df, asp_df, ek_df, qk_df, meas_loc_df, as_agent= False)
            print(f"Template file: {template_file}")

 #%%
# Now manually review and edit the files
review_dir = "brick_yaml_reviewed"
os.makedirs(review_dir, exist_ok=False)
shutil.copytree(new_dir, review_dir, dirs_exist_ok=False)

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

def compute_cost(prompt_encoded, completion_encoded, model = 'sonnet'):
    if model == "sonnet":
        input_cost = 3
        output_cost = 15
    if model == "flash":
        input_cost = 0.35
        output_cost = 0.7
    prompt_cost = len(prompt_encoded) / 1_000_000 * input_cost 
    completion_cost = len(completion_encoded) / 1_000_000 * output_cost
    total_cost = prompt_cost + completion_cost
    print(f"Prompt cost: {prompt_cost}, Completion cost: {completion_cost}, Total cost: {total_cost}")
    return total_cost
print(f"For Most Expensive Model: {compute_cost(prompt_encoded, completion_encoded, model = 'sonnet')}")
print(f"For Cheapest Model: {compute_cost(prompt_encoded, completion_encoded, model = 'flash')}")

# %%
