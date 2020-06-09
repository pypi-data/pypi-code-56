from cmnSys.simpleConfig import SimpleConfig


class ServerConfig(SimpleConfig):
    def set_default_data(self):
        self.data = {
            'port': 6719
        }

