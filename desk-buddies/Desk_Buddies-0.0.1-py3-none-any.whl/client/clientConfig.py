from cmnSys.simpleConfig import SimpleConfig


class ClientConfig(SimpleConfig):

    def set_default_data(self):
        self.data = {
            'host': '',
            'uid': '',
            'port': 6719
        }
