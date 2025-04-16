# %%
from rdflib import Graph
from utils import * 
from namespaces import * 
from get_completion import get_completion
# %%
g = Graph()
g.parse("https://brickschema.org/schema/1.4.3/Brick.ttl", format = "ttl")

# %%
query = """ SELECT DISTINCT ?brick_class ?brick_definition ?brick_parent WHERE {
    ?brick_class rdfs:subClassOf brick:Sensor ;
        skos:definition ?brick_definition .
    FILTER NOT EXISTS {
        ?brick_class2 rdfs:subClassOf brick:Sensor .
        ?brick_class rdfs:subClassOf ?brick_class2 .
    }
    FILTER NOT EXISTS {
        ?brick_class owl:deprecated true .
    }
    FILTER (!strstarts(str(?brick_class), "https://w3id.org/rec#")) 
    BIND (brick:Sensor AS ?brick_parent).
}"""

def copy_brick_data_to_csv(input_df, existing_csv_path, output_csv_path=None):
    """
    Extracts brick_class and brick_parent from input DataFrame and adds them
    to an existing CSV file as new rows, preserving all existing data.
    
    Parameters:
    -----------
    input_df : pandas.DataFrame
        DataFrame containing at least brick_class and brick_parent columns
    existing_csv_path : str
        Path to the existing CSV file
    output_csv_path : str, optional
        Path to save the resulting CSV. If None, overwrites the existing CSV.
    
    Returns:
    --------
    pandas.DataFrame
        The resulting DataFrame that was saved to CSV
    """
    # Ensure the input DataFrame has the required columns
    if 'brick_class' not in input_df.columns or 'brick_parent' not in input_df.columns:
        raise ValueError("Input DataFrame must contain 'brick_class' and 'brick_parent' columns")
    
    # Extract only the needed columns
    brick_data = input_df[['brick_class', 'brick_parent', 'brick_definition']].copy()
    
    # Read the existing CSV
    try:
        existing_df = pd.read_csv(existing_csv_path)
    except FileNotFoundError:
        print(f"Warning: Existing CSV file {existing_csv_path} not found. Creating a new one.")
        # Create a new DataFrame with expected columns
        existing_df = pd.DataFrame(columns=['brick_class', 'brick_parent', 'brick_definition', '223_class', 
                                           'quantitykind', 'medium', 'aspects'])
    
    # Get all columns from existing CSV
    all_columns = existing_df.columns.tolist()
    
    # Filter out brick_class values that already exist in the CSV
    existing_brick_classes = set(existing_df['brick_class']) if 'brick_class' in existing_df.columns else set()
    new_brick_data = brick_data[~brick_data['brick_class'].isin(existing_brick_classes)]
    
    if len(new_brick_data) == 0:
        print("No new brick_class entries to add. All provided brick_class values already exist in the CSV.")
        return existing_df
    
    # Ensure brick_data has all the columns from the existing CSV
    for col in all_columns:
        if col not in brick_data.columns:
            brick_data[col] = None  # Add missing columns with None values
    
    # Reorder columns to match the existing CSV
    brick_data = brick_data[all_columns]
    
    # Append the new data to the existing data
    result_df = pd.concat([existing_df, brick_data], ignore_index=True)
    
    # Save to CSV
    output_path = output_csv_path if output_csv_path else existing_csv_path
    result_df.to_csv(output_path, index=False)
    
    print(f"Data successfully appended to {output_path}")
    return result_df

# Example usage:
# Assuming you have a DataFrame called 'df' with brick_class and brick_parent columns
# and an existing CSV file at 'path/to/existing.csv'

# df = pd.DataFrame({
#     'brick_class': ['Class1', 'Class2', 'Class3'],
#     'brick_parent': ['Parent1', 'Parent2', 'Parent3'],
#     'other_column': [1, 2, 3]
# })
# 
# result = copy_brick_data_to_csv(df, 'path/to/existing.csv', 'path/to/output.csv')

# %%
brick_schema_df = copy_brick_data_to_csv(query_to_df(query, g), "mapping.csv")
# %%
