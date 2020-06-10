import json
import csv

class jsontools(object):
    @staticmethod
    def json_parse(filename: str) -> dict:
        """
        Parse json data from file
        """
        with open(filename, "r") as json_file:
            json_data = json.loads(json_file.read())
        return json_data
        
    @staticmethod
    def write_file(json_data, filename: str) -> None:
        """
        Write json data to file
        """
        with open(filename, "a+") as json_file:
            print(json.dumps(json_data), file=json_file)
        return
    
    @staticmethod
    def pretty_print(json_data: dict) -> None:
        """
        Pretty print json
        """
        print(json.dumps(json_data, indent=4, sort_keys=True))
    
    @staticmethod
    def data_to_csv(json_data: str, filename: str) -> None:
        cols = [key for key in json_data[0].keys()]
        vals = []
        for json_match in json_data:
            json_items = json_match.items()
            item = [
                json.dumps(element[1]).replace('"', "'") 
                if 
                type(element[1]) == list or type(element[1]) == dict 
                else 
                element[1] for element in json_items
            ]
            vals.append(item)

        with open(filename, "a+") as csv_file:
            a_write = csv.writer(csv_file)
            a_write.writerow(tuple(cols))

            for val in vals:
                a_write.writerow(tuple(val))
