

from mimetypes import init
from typing import List
from Domain.Business_objects.Protocol import Protocol

from Domain.Mediators.ProtocolMediator import ProtocolMediator


class ProtocolService():
    def __init__(self, protocolMediator: ProtocolMediator) -> None:
        self.protocolMediator = protocolMediator

    def getAllProtocols(self) -> List[Protocol]:
        return self.protocolMediator.getAllProtocols()
