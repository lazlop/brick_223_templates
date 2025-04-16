# %%
from rdflib import Graph
from utils import * 
from namespaces import * 
from get_completion import get_completion



# %%
s223 = Graph()
s223.parse("https://open223.info/223p.ttl", format = "ttl")
bind_prefixes(s223)

# %%
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
display(prop_df)
s223_properties = prop_df.to_csv(index=False)

# %%
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
display(media_df)
s223_media = media_df.to_csv(index=False)

# %%
# Get Aspects
asp_query = """ SELECT DISTINCT ?s223_class ?s223_definition WHERE {
    ?s223_class rdfs:subClassOf* s223:EnumerationKind .
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
display(asp_df)
s223_aspects = asp_df.to_csv(index=False)

# %%
# Get EnumerationKind
ek_query = """ SELECT DISTINCT ?s223_class ?s223_definition WHERE {
    ?s223_class rdfs:subClassOf* s223:EnumerationKind .
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
display(ek_df)
s223_eks = ek_df.to_csv(index=False)

# %%
brick_class = brick_schema_df['brick_class'][0]
definition = brick_schema_df['brick_definition'][0]
system_prompt = """"""
prompt = f"""
Determine what s223_class the brick_class should be, based on its name and definition.
the possible s223 classes are <s223_properties>{s223_properties}</s223_properties> 

Only return the s223_class. Do not return any other information.

brick_class: {brick_class}
definition: {definition}
"""
s223_class = get_completion(prompt, system_prompt)
print(f"brick_class: {brick_class}")
print(f"definition: {definition}")
print(f"s223_class: {s223_class}")


# %%
# What are the valid quantitykinds
# building_models = Graph()
# building_models.parse("https://models.open223.info/compiled/nist-bdg1-1.ttl", format = "ttl")
# building_models.parse("https://models.open223.info/pnnl-bdg1-2.ttl", format = "ttl")
# building_models.parse("https://models.open223.info/pnnl-bdg2-1.ttl", format = "ttl")
# building_models.parse("https://models.open223.info/lbnl-bdg3-1.ttl", format = "ttl")
# building_models.parse("https://models.open223.info/lbnl-bdg4-1.ttl", format = "ttl")


# query = """ SELECT DISTINCT ?quantitykind WHERE {
#     ?s qudt:hasQuantityKind ?quantitykind .
# }"""
# quantitykind_df = query_to_df(query, building_models)
# display(quantitykind_df)

# Completed by hand

# %%
with open("quantitykinds.csv", "r") as f:
    quantitykinds = f.read()

# %%
prompt = f"""
Determine what quantitykind or enumerationkind the brick_class should be, based on its name and definition.
the possible quantitykinds are <quantitykinds>{quantitykinds}</quantitykinds> 
the possible enumerationkinds are <s223_eks>{s223_eks}</s223_eks>
Only return the quantitykind or enumerationkind. Do not return any other information.

brick_class: {brick_class}
definition: {definition}
"""
s223_class = get_completion(prompt, system_prompt)
print(f"brick_class: {brick_class}")
print(f"definition: {definition}")
print(f"s223_class: {s223_class}")


# %%
prompt = f"""
Determine what medium the brick_class should be associated with, based on its name and definition.
the possible media are <media>{s223_media}</media> 
Only return the quantitykind or enumerationkind. Do not return any other information.

If there is no sensible medium, return None.

brick_class: {brick_class}
definition: {definition}
"""
s223_class = get_completion(prompt, system_prompt)
print(f"brick_class: {brick_class}")
print(f"definition: {definition}")
print(f"s223_class: {s223_class}")


# %%
prompt = f"""
Determine what aspects the brick_class should be associated with, based on its name and definition.
the possible aspects are <aspects>{s223_aspects}</aspects> 
Only return the quantitykind or enumerationkind. Do not return any other information.

If there is no sensible medium, return None.

brick_class: {brick_class}
definition: {definition}
"""
s223_class = get_completion(prompt, system_prompt)
print(f"brick_class: {brick_class}")
print(f"definition: {definition}")
print(f"s223_class: {s223_class}")


# %%



