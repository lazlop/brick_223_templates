#%% 
from buildingmotif.namespaces import bind_prefixes, A, XSD, QUDT, RDFS, A, SH, Namespace, RDF

HPF = Namespace(f"urn:hpflex#")
HPFS = Namespace('urn:hpflex/shapes#')

PARAM = Namespace("urn:___param___#")
# all versions of Brick > 1.1 have these namespaces
BRICK = Namespace("https://brickschema.org/schema/Brick#")
TAG = Namespace("https://brickschema.org/schema/BrickTag#")
BSH = Namespace("https://brickschema.org/schema/BrickShape#")
REF = Namespace("https://brickschema.org/schema/Brick/ref#")

# defaults
OWL = Namespace("http://www.w3.org/2002/07/owl#")
RDF = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
SH = Namespace("http://www.w3.org/ns/shacl#")
XSD = Namespace("http://www.w3.org/2001/XMLSchema#")

# QUDT namespaces
QUDT = Namespace("http://qudt.org/schema/qudt/")
QK = Namespace("http://qudt.org/vocab/quantitykind/")
DV = Namespace("http://qudt.org/vocab/dimensionvector/")
UNIT = Namespace("http://qudt.org/vocab/unit/")

# ASHRAE namespaces
BACNET = Namespace("http://data.ashrae.org/bacnet/2020#")
S223 = Namespace("http://data.ashrae.org/standard223#")

BM = Namespace("https://nrel.gov/BuildingMOTIF#")
CONSTRAINT = Namespace("https://nrel.gov/BuildingMOTIF/constraints#")
S223 = Namespace("http://data.ashrae.org/standard223#")

A = RDF.type

def bind_prefixes(graph, override = False):
    """Associate common prefixes with the graph.

    :param graph: graph
    :type graph: rdflib.Graph
    """

    graph.bind("xsd", XSD, override = override)
    graph.bind("rdf", RDF, override = override)
    graph.bind("owl", OWL, override = override)
    graph.bind("rdfs", RDFS, override = override)
    graph.bind("skos", SKOS, override = override)
    graph.bind("sh", SH, override = override)
    graph.bind("quantitykind", QK, override = override)
    graph.bind("qudt", QUDT, override = override)
    graph.bind("unit", UNIT, override = override)
    graph.bind("brick", BRICK, override = override)
    graph.bind("tag", TAG, override = override)
    graph.bind("bsh", BSH, override = override)
    graph.bind("P", PARAM, override = override)
    graph.bind("constraint", CONSTRAINT, override = override)
    graph.bind("bmotif", BM, override = override)
    graph.bind("hpflex", HPF, override = override)
    graph.bind("hpfs", HPFS, override = override)
    graph.bind('s223', S223, override = override)

def get_prefixes(g):
    return "\n".join(f"PREFIX {prefix}: <{namespace}>" for prefix, namespace in g.namespace_manager.namespaces())