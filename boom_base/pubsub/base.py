from abc import ABC
from typing import Dict


class AbstractPubsubService(ABC):

    def publish(self, topicName: str, data: Dict):
        raise NotImplementedError
