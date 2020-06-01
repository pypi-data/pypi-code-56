from typing import List

from pyterum.socket_conn import SocketConn
from pyterum.kill_message import KillMessage
from pyterum.fragmenter_input_message import FragmenterInputMessage
from pyterum import env
from pyterum.logger import logger

class FragmenterInput(SocketConn):

    def __init__(self, address:str=None):
        if address == None:
            env.verify_fragmenter_envs()
            address = env.FRAGMENTER_INPUT
        super().__init__(address, retry_policy={"consume": 0})

        logger.info(f"Initializing FragmenterInput...")
        self.connect()
        self.produce = None
        self._consumer = super().consumer()

    # Yields None if the message is the kill message, indicating that there will be no more messages
    def consumer(self) -> List[str]:
        while True:
            msg = next(self._consumer)
            output = None
            try:
                output = FragmenterInputMessage.from_json(msg)
            except (KeyError, TypeError) as errFrag:
                try:
                    KillMessage.from_json(msg)
                except (KeyError, TypeError) as errKill:
                    logger.debug(errFrag)
                    logger.debug(errKill)
                    raise Exception("Could not parse message as FragmenterInputMessage nor as KillMessage")
            yield output

class FragmenterOutput(SocketConn):

    def __init__(self, address:str=None):
        if address == None:
            env.verify_fragmenter_envs()
            address = env.FRAGMENTER_OUTPUT
        super().__init__(address, retry_policy={"produce": 0})

        logger.info(f"Initializing FragmenterOutput...")
        self.connect()
        self.consumer = None

    def produce(self, data:List[str]):
        super().produce(data)

    # To send that the fragmenter is done
    def produce_kill(self):
        super().produce(KillMessage().to_json())