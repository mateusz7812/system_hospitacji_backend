

from email.policy import default
import json
from mimetypes import init
from typing import List
from Domain.Business_objects.Answer import Answer
from Domain.Business_objects.Hospitations import Hospitation
from Domain.Mediators.HospitationMediator import HospitationMediator
from Foundation.DB_adapter.db import Hospitacja


class HospitationService():
    def __init__(self, hospitationMediator: HospitationMediator) -> None:
        self.hospitationMediator = hospitationMediator

    
    def getAllHospitations(self, teacher_id) -> List[Hospitacja]:
        test = self.hospitationMediator.getAllHospitations(teacher_id)
        test =list(map(lambda x: x.__dict__, test))
        return test

    def getTeachersHospitations(self, teacher_id)-> List[Hospitation]:
        #return json.dumps(list(map(lambda x: x.__dict__, self.protocolMediator.getTeacherProtocolsReports(teacher_id))), default=str)
        return list(map(lambda x: x.__dict__, self.hospitationMediator.getTeachersHospitations(teacher_id)))

    def saveHospitationDate(self, hospitation_id, date):
        return self.hospitationMediator.saveHospitationDate(hospitation_id, date)

    def getNotificationData(self):
        return self.hospitationMediator.getNotificationData()


