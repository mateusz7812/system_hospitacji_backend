

from email.policy import default
import json
from mimetypes import init
from typing import List
from Domain.Business_objects.Answer import Answer
from Domain.Business_objects.HospitalizationCommittee import HospitalizationCommittee
from Domain.Business_objects.ProtocolReport import ProtocolReport
from Domain.Mediators.HospitalizationCommitteeMediator import HospitalizationCommitteeMediator


class HospitalizationCommitteeService():
    def __init__(self, hospitalizationCommitteeMediator: HospitalizationCommitteeMediator) -> None:
        self.hospitalizationCommitteeMediator = hospitalizationCommitteeMediator

    def getAllHospitalizationCommittees(self) -> List[HospitalizationCommittee]:
        hospitalizationCommittees = self.hospitalizationCommitteeMediator.getAllHospitalizationCommittees()
    
        hospitalizationCommittees = list(
            map(lambda x: x.__dict__, hospitalizationCommittees))
        for i in range(len(hospitalizationCommittees)):
            #hospitalizationCommittees[i]["committee_head"] = hospitalizationCommittees[i]["committee_head"].__dict__
            hospitalizationCommittees[i]["committee_members"] = list(map(lambda x: x.__dict__, hospitalizationCommittees[i]["committee_members"]))
        return hospitalizationCommittees

    def createNewHospitalizationCommittee(self, p:HospitalizationCommittee):
        return self.hospitalizationCommitteeMediator.createNewHospitalizationCommittee(p)