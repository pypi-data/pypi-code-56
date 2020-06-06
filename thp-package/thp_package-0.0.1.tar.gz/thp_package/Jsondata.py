import csv
import json

def jsondata():
    csvFilepath = "Avg/avgTHPAll.csv"
    jsonFilepath = "avgTHPAll.json"

    data = {}
    with open(csvFilepath) as csvFile:
        csvReader = csv.DictReader(csvFile)
        for csvRow in csvReader:
            sl_no = csvRow['Sl No.']
            data[sl_no] = csvRow

    with open('JSON/avgTHPAll.json', 'w') as jsonFile:
        jsonFile.write(json.dumps(data, indent=4))
        