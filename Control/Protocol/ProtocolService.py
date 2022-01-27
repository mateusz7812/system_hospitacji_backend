

from email.policy import default
import json
from mimetypes import init
from typing import List
from Domain.Business_objects.Answer import Answer
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
        return list(map(lambda x: x.__dict__, self.protocolMediator.getTeacherProtocolsReports(teacher_id)))

    def getProtocolDetails(self, protocol_id):
        details = self.protocolMediator.getProtocolDetails(
            protocol_id)
        if details is None:
            return {"error": "protocol not found"}
        details = details.__dict__
        details["protocol"] = details["protocol"].__dict__
        details["hospitalized"] = details["hospitalized"].__dict__
        details["hospitals"] = list(map(lambda x: x.__dict__, details["hospitals"]))
        details["course"] = details["course"].__dict__
        details["group"] = details["group"].__dict__
        return details

    def getProtocolAnswers(self, protocol_id):
        answers = self.protocolMediator.getProtocolAnswers(protocol_id)
        answers = list(map(lambda x: x.__dict__, answers))
        return answers

    def saveProtocolAnswers(self, protocol_id, answers):
        for answer_dict in answers:
            answer_obj = Answer(answer_dict["text"], answer_dict["question_id"])
            self.protocolMediator.saveProtocolAnswer(protocol_id, answer_obj)
        return '', 200
    
    def getQuestions(self):
        questions = self.protocolMediator.getQuestions()
        questions = list(map(lambda x: x.__dict__, questions))
        return questions
