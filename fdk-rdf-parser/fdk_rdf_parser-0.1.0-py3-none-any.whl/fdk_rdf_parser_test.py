from typing import Dict

from rdflib import Graph
from rdflib.namespace import FOAF, RDF

from fdk_rdf_parser.parse_functions.dataset import Dataset, DataService, parseDataset, parseDataService
from fdk_rdf_parser.rdf_utils import dcatURI


def parseDataServices(rdfData: str) -> Dict[str, DataService]:
    dataServices: Dict[str, DataService] = {}

    dataServicesGraph = Graph().parse(data=rdfData, format='turtle')

    for dataServiceURI in dataServicesGraph.subjects(
        predicate=RDF.type, object=dcatURI("DataService")
    ):
        dataServices[dataServiceURI.toPython()] = parseDataService(dataServicesGraph, dataServiceURI)

    return dataServices


def parseDatasets(rdfData: str) -> Dict[str, Dataset]:
    datasetsGraph = Graph().parse(data=rdfData, format="turtle")

    datasets: Dict[str, Dataset] = {}

    for recordURI in datasetsGraph.subjects(
        predicate=RDF.type, object=dcatURI("record")
    ):
        datasetURI = datasetsGraph.value(recordURI, FOAF.primaryTopic)
        if datasetURI is not None:
            datasets[datasetURI.toPython()] = parseDataset(
                datasetsGraph, recordURI, datasetURI
            )

    return datasets
