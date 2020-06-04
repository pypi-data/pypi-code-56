import wget
import pandas as pd 


class State: 
    def __init__(self, name):
        self.name = name
        self.url = f'https://raw.githubusercontent.com/nicnguyen3103/US_coordinate/master/{self.name}_Z15_S2_BFS/combined_map_points.txt'
        self.coord = self.get_coord_list()
        
    def get_coord_tuple(self): 
        df = pd.read_csv(self.url, header=None)
        df = df.rename(columns={0: "lat", 1: "long"})
        final = []
        for i in range(len(df['lat'])):
            final.append((df['lat'][i], df['long'][i]))
            
        return final
    
    def get_coord_list(self): 
        df = pd.read_csv(self.url, header=None)
        df = df.rename(columns={0: "lat", 1: "long"})
        final = []
        for i in range(len(df['lat'])):
            final.append([df['lat'][i], df['long'][i]])
        
        return final
    
    def download(self):
        print(f'getting the coordinate of {self.name}')
        wget.download(self.url, f'./{self.name}_map_points.txt') 
        print('done')
        