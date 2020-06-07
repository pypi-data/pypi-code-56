import requests
from .dataCleaning import *

def higherLevelAPI(nameAndTaxaTuple):
    name, taxaDetails = nameAndTaxaTuple
    if taxaDetails == '': return (name, False, [])
    if taxaDetails[0] == '': return (name,False,[])
    elif taxaDetails[0] == 'species': return (name,True,[cleanSingleSpeciesString(taxaDetails[1])])
    return convertHigherLevelTaxaToListOfSpecies(nameAndTaxaTuple)

def convertHigherLevelTaxaToListOfSpecies(nameAndTaxaTuple):
    name, taxaDetails = nameAndTaxaTuple
    taxaRank,taxaName = taxaDetails
    try:
        namesDicts = requests.get('https://api.gbif.org/v1/species/search?q='+taxaName+'&rank=species').json()['results']
        namesDicts = list(map(cleanSingleSpeciesString,map(lambda x: x.get('species',''), namesDicts)))
        namesDicts = list(filter(lambda x: x != '',namesDicts))
        if taxaRank == "genus": namesDicts = list(filter(lambda x: x.split(" ")[0] == taxaName,namesDicts))
        return (name,True,list(set(namesDicts)))
    except Exception as e:
        return (name,False,[])
