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
    
    # Get possible measurement locations/conncetables that have the property
    meas_loc_query = """ SELECT DISTINCT ?s223_class ?s223_definition WHERE {
    {
    ?s223_class rdfs:subClassOf+ s223:Connectable .
    }
    UNION
    {
    ?s223_class rdfs:subClassOf* s223:Connection .
    }
    UNION
    {
    ?s223_class rdfs:subClassOf+ s223:ConnectionPoint .
    }

    ?s223_class rdfs:comment ?s223_definition .
    
    # have to remove sensors since they are not measurement locations
    FILTER NOT EXISTS {
        ?s223_class rdfs:subClassOf* s223:Sensor .
    }
    # Generic equipment might not be a useful measurement location, so we remove it 
    FILTER ( ?s223_class != s223:Equipment )
    FILTER ( ?s223_class != s223:Sensor )
    FILTER(STRSTARTS (str(?s223_class), \"http://data.ashrae.org/standard223#\"))
    }
    """
    meas_loc_df = query_to_df(meas_loc_query, s223)

    # Convert quantitykinds to dataframe for validation
    qk_df = pd.read_csv(quantityknds_file)
    
    return prop_df, media_df, asp_df, ek_df, qk_df, meas_loc_df
