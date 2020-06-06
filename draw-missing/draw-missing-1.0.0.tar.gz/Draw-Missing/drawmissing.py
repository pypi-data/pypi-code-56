import matplotlib.pyplot as mp


class Draw:
    # Initialization
    def __init__(self, df):
        self.df = df
        self.total_cells = len(df) * len(df.columns)
        self.missing_cells = 0

    # Creating a dataframe of missing variables
    def missing_df(self):
        self.df = self.df.isna().sum()
        self.df = self.df.to_frame()
        self.df.reset_index(inplace=True)
        self.df = self.df.rename(columns={"index": "Features", 0: "Missing_Count"})
        return self.df

    def draw_missing_plot(self):
        new = self.missing_df()
        # If there re no missing values found a message is printed
        if new.empty:
            print("There are no missing values")
        # Else the missing value bar graph is plotted
        else:
            self.missing_cells = sum(new['Missing_Count'])
            new = new[new['Missing_Count'] != 0]
            fig = mp.figure(figsize=(20, 10))
            mp.barh(new['Features'], new['Missing_Count'],
                    label=f"Missing values: {round((self.missing_cells * 100) / self.total_cells, 2)} %",
                    color='lightgrey')
            mp.legend(prop={'size': 15})
            for index, value in enumerate(new['Missing_Count']):
                mp.text(value, index, str(value))
