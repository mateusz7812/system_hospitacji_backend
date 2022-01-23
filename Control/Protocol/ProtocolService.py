

from email.policy import default
import json
from mimetypes import init
from typing import List
from Domain.Business_objects.Protocol import Protocol
from Domain.Business_objects.ProtocolReport import ProtocolReport
from Domain.Mediators.ProtocolMediator import ProtocolMediator


class ProtocolService():
    def __init__(self, protocolMediator: ProtocolMediator) -> None:
        self.protocolMediator = protocolMediator

    def getAllProtocols(self) -> List[Protocol]:
        return self.protocolMediator.getAllProtocols()

    def getTeachersProtocolsReports(self, teacher_id)-> List[ProtocolReport]:
        #return json.dumps(list(map(lambda x: x.__dict__, self.protocolMediator.getTeacherProtocolsReports(teacher_id))), default=str)
        return self.protocolMediator.getTeacherProtocolsReports(teacher_id)
