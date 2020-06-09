import yaml

class TestConfig:
    '''
        Extend this Base class to avoid Re-writing most of the things

        example:
            class config(TestConfig):
                def __init__(self):
                    super().__init__()
                    self.EXPERIMENT = {
                        'NAME':"Exp1",
                        'DATE' : datetime.datetime.now(),
                    }
                    self.DATA_FILE = '../hsjdhfs/sdfjsk.zip'
                    self.DEVICE = 'cpu'

            config = config()
            config.DEVICE
            config.BATCHSIZE
    '''

    def __init__(self):
        self.OPTIMIZER = 0.0001
        self.DEVICE = 'cuda'

        self.BATCHSIZE = 32

    def dumpconfig(self, location):
        with open(location, 'w') as dumpfile:
            yaml.dump(self.__dict__, dumpfile)

        return "you file has successfully saved"