class Distribution:

    def __init__(self, mu=0, sigma=1) -> None:
        """Generic distribution class for calculating and visualizing a probability distribution.

        Args:
            mu (int, optional): [description]. Defaults to 0.
            sigma (int, optional): [description]. Defaults to 1.
        """

        self.mean = mu
        self.stdev = sigma
        self.data = []


    def read_data_file(self, file_name: str) -> None:
        """Function to read from a txt file. the txt file should have
        one number (float) per line. the numbers are stored in the data attribute.

        Args:
            file_name (str): name of the file to read from
        """

        with open(file_name) as file:
            data_list = []
            line = file.readline()
            while line:
                data_list.append(int(line))
                line = file.readline()
        file.close()

        self.data = data_list         
