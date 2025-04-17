#%%
from rdflib import Graph
from .utils import * 
from .namespaces import * 
from .get_completion import get_completion
import yaml
import os
import pandas as pd
import csv
from io import StringIO
from importlib.resources import files

quantityknds_file = str(files('template_builder').joinpath('data/quantitykinds.csv'))

def get_s223_info():
    s223 = Graph()
    s223.parse("https://open223.info/223p.ttl", format="ttl")
    bind_prefixes(s223)
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
    s223_properties = prop_df.to_csv(index=False)
    
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
    s223_media = media_df.to_csv(index=False)
    
    # Get Aspects

    # looking at everything that could be an aspect 
    # asp_query = """ SELECT DISTINCT ?s223_class ?s223_definition WHERE {
    #     ?s223_class rdfs:subClassOf* s223:EnumerationKind .
    #     ?s223_class rdfs:comment ?s223_definition .
      
    #     FILTER NOT EXISTS {        
    #         ?s223_class rdfs:subClassOf* s223:EnumerationKind-Substance .
    #     }
    #     # Excluding all the voltages
    #     FILTER NOT EXISTS {        
    #         ?s223_class rdfs:subClassOf* s223:EnumerationKind-Numerical .
    #     }
    #     FILTER NOT EXISTS {        
    #         ?s223_class rdfs:subClassOf* s223:EnumerationKind-ElectricalPhaseIdentifier .
    #     }
    #     FILTER NOT EXISTS {        
    #         ?s223_class rdfs:subClassOf* s223:EnumerationKind-ElectricalVoltagePhases .
    #     }
    #     FILTER NOT EXISTS {        
    #         ?s223_class rdfs:subClassOf* s223:EnumerationKind-DayOfWeek .
    #     }
    # }
    # """

    # looking only at aspects
    asp_query = """ SELECT DISTINCT ?s223_class ?s223_definition WHERE {
        ?s223_class rdfs:subClassOf* s223:EnumerationKind-Aspect .
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
    s223_aspects = asp_df.to_csv(index=False)
    
    # Get EnumerationKind
    ek_query = """ SELECT DISTINCT ?s223_class ?s223_definition WHERE {
        ?s223_class rdfs:subClassOf+ s223:EnumerationKind .
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
    s223_eks = ek_df.to_csv(index=False)
    
    # Convert quantitykinds to dataframe for validation
    qk_df = pd.read_csv(quantityknds_file)
    quantitykinds = qk_df.to_csv(index=False)
    
    return s223_properties, s223_media, s223_aspects, s223_eks, quantitykinds,prop_df, media_df, asp_df, ek_df, qk_df
