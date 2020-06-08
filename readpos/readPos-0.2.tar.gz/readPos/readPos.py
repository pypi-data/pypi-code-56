import pandas as pd

class ReadPos:

    def __init__(self, file_name, csv_file):
        self.csv_map = csv_file
        self.dat_file = file_name

    def read(self, encoding = 'UTF-8'):
        with open(self.dat_file, 'r', encoding) as f: # Reading raw data input
            data = f.readlines()
        
        df_response = pd.DataFrame() # Object returned by funcion. Wiil be filled with structured data.

        csv = pd.read_csv(self.csv_map, sep=';', encoding=encoding) # Reading csv map file
        

        for i in range(0,csv.shape[0]):
            curr_variable = csv.iloc[i]
            temp_list = []

            for line in data:
                temp_list.append(line[(curr_variable['initial']-1):curr_variable['end'] ] )
            df_response[curr_variable['variable']] = temp_list
        return df_response


    def write(self, dataframe, encoding = 'UTF-8'):
        csv = pd.read_csv(self.csv_map, sep=';') # Reading map and ordering to start with lowest position
        csv = csv.sort_values(by=['initial'])

        dataframe_output = pd.DataFrame()
        for i in range(0,csv.shape[0]):
            try:
                dataframe_output[csv['variable'].iloc[i]] = fill_column(dataframe[csv['variable'].iloc[i]], csv['initial'].iloc[i+1] - csv['initial'].iloc[i] ) 
            except:
                dataframe_output[csv['variable'].iloc[i]] = fill_column(dataframe[csv['variable'].iloc[i]], csv['end'].iloc[i] - csv['initial'].iloc[i] + 1 ) 
        
        dataframe_output = dataframe_output[list(dataframe_output.columns)].agg(''.join, axis=1)

        dataframe_output.to_csv(self.dat_file, sep='\t', encoding=encoding, header=None, index=None)                        


        

        return 'File ' + self.dat_file + ' created successfully'


def fill_column(column, next_var):
    column_filled = []
    for x in column:
        x = str(x)
        column_filled.append(x + ' '*(next_var-len(x))  )
    
    return column_filled
