from buildingmotif.namespaces import * 
from rdflib import Graph, URIRef, Literal
import pandas as pd
from typing import Optional


def get_prefixes(g: Graph):
    return "\n".join(f"PREFIX {prefix}: <{namespace}>" for prefix, namespace in g.namespace_manager.namespaces())

def convert_to_prefixed(uri, g: Graph):
    try:
        prefix, uri_ref, local_name = g.compute_qname(uri)
        return f"{prefix}:{local_name}"
    except Exception as e:
        print(e)
        return uri

def convert_to_uri(str_in, g: Graph):
    if str_in is None:
        return None
    if str_in.startswith("http"):
        return URIRef(str_in)
    if str_in.contains(":"):
        str_in.split(':')[-1]
        

def convert_to_localname(uri, g: Graph):
    """
    Given a URI and a Graph, remove the namespace prefix if it exists.

    Args:
        uri (str): The URI to strip the namespace from
        g (Graph): The RDF graph with the namespace mappings

    Returns:
        str: The URI with the namespace prefix removed
    """
    
    try:
        prefix, uri_ref, local_name = g.compute_qname(uri)
        return local_name
    except Exception as e:
        print(e)
        return uri

def query_to_df(query, g: Graph, remove_namespaces=False):
    results = g.query(query)
    if remove_namespaces:
        formatted_results = [
            [convert_to_localname(value, g) if isinstance(value, (str, bytes)) and value.startswith("http") else str(value) for value in row]
            for row in results
        ]
    else:        
        formatted_results = [
            [convert_to_prefixed(value, g) if isinstance(value, (str, bytes)) and value.startswith("http") else str(value) for value in row]
            for row in results
        ]
    df = pd.DataFrame(formatted_results, columns=[str(var) for var in results.vars])
    return df

def add_brick_inverse_relations(g):
    # Dictionary of relationships and their inverses
    inverse_pairs = {
        BRICK.isFedBy: BRICK.feeds,
        BRICK.feeds: BRICK.isFedBy,
        BRICK.hasPart: BRICK.isPartOf,
        BRICK.isPartOf: BRICK.hasPart,
        BRICK.hasPoint: BRICK.isPointOf,
        BRICK.isPointOf: BRICK.hasPoint,
        BRICK.hasLocation: BRICK.isLocationOf,
        BRICK.isLocationOf: BRICK.hasLocation,
        BRICK.controls: BRICK.isControlledBy,
        BRICK.isControlledBy: BRICK.controls,
        BRICK.affects: BRICK.isAffectedBy,
        BRICK.isAffectedBy: BRICK.affects,
        BRICK.hasInput: BRICK.isInputOf,
        BRICK.isInputOf: BRICK.hasInput,
        BRICK.hasOutput: BRICK.isOutputOf,
        BRICK.isOutputOf: BRICK.hasOutput,
        BRICK.measures: BRICK.isMeasuredBy,
        BRICK.isMeasuredBy: BRICK.measures,
        BRICK.regulates: BRICK.isRegulatedBy,
        BRICK.isRegulatedBy: BRICK.regulates,
        BRICK.hasSubject: BRICK.isSubjectOf,
        BRICK.isSubjectOf: BRICK.hasSubject
    }
    # For each relationship in the graph, add its inverse
    for s, p, o in g:
        if p in inverse_pairs:
            g.add((o, inverse_pairs[p], s))

    return g


def get_unique_uri(graph, uri):
    base_uri = str(uri)
    count = 1
    new_uri = URIRef(base_uri)
    # Check if the URI already exists in the graph
    while (new_uri, None, None) in graph or (None, None, new_uri) in graph:
        # Append an incremented number if it already exists
        new_uri = URIRef(f"{base_uri}-{count}")
        count += 1
    return new_uri

def get_uri_name(graph, uri):
    if isinstance(uri, URIRef):
        return graph.compute_qname(uri)[-1]
    else:
        return uri

def create_uri_name_from_uris(graph,ns, uri_lst, suffix: Optional[str] = ""):
    # append uri names in namespace and check uniqueness against graph
    # URI list may not be all uris
    node_names = []
    for uri in uri_lst:
        if isinstance(uri, URIRef):
            node_names.append(get_uri_name(graph, uri))
        else:
            node_names.append(uri)
    new_uri = get_unique_uri(graph, ns[f"{'_'.join(node_names)}{suffix}"])
    graph.add((new_uri, RDFS.label, Literal(get_uri_name(graph, new_uri))))
    return new_uri
