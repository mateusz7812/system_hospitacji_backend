import json
from Domain.Business_objects.HospitalizationCommittee import HospitalizationCommittee
from flask import Flask, request
from flask_restful import reqparse
from flask_restful import Resource, Api
from Control.Protocol.ProtocolService import ProtocolService
from Control.TestService import TestService
from Domain.Mediators.ProtocolMediator import ProtocolMediator
from Domain.Mediators.HospitalizationCommitteeMediator import HospitalizationCommitteeMediator
from Control.HospitalizationCommittee.HospitalizationCommitteeService import HospitalizationCommitteeService
from Control.Teacher.TeacherService import TeacherService
from Domain.Mediators.TeacherMediator import TeacherMediator
from flask_cors import CORS
import time

from Domain.Mediators.TestMediator import TestMediator

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
api = Api(app)

testMediator = TestMediator()
testService = TestService(testMediator)

protocolMediator = ProtocolMediator()
protocolService = ProtocolService(protocolMediator)

hospitalizationCommitteeMediator = HospitalizationCommitteeMediator()
hospitalizationCommitteeService = HospitalizationCommitteeService(hospitalizationCommitteeMediator)

teacherMediator = TeacherMediator()
teacherService = TeacherService(teacherMediator)

debug = True

class HospitalizationCommittee(Resource):
    def get(self):
        return hospitalizationCommitteeService.getAllHospitalizationCommittees()

    def post(self):
        hospitalizationCommittee = request.json
        return hospitalizationCommitteeService.createNewHospitalizationCommittee(hospitalizationCommittee)


class Teachers(Resource):
    def get(self):
        return teacherService.getAllTeachers()
    # def get(self, teacher_id):
    #     return teacherService.getTeacher(teacher_id)
class Teacher(Resource):
    def get(self, teacher_id):
        return teacherService.getTeacher(teacher_id)

class TeacherId(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('teacher_firstName', type = str)
        self.reqparse.add_argument('teacher_lastName', type = str)
        self.reqparse.add_argument('teacher_zhz', type = bool)

    def get(self):
        args = self.reqparse.parse_args()
        print("args", args)
        return teacherService.getTeacherId(args['teacher_firstName'], args['teacher_lastName'], args['teacher_zhz'])

class ProtocolsReports(Resource):
    def get(self):
        args = request.args
        teacher_id = args['teacher_id']
        return protocolService.getTeachersProtocolsReports(teacher_id)


class Protocol(Resource):
    def get(self, protocol_id: str):
        return protocolService.getProtocolDetails(protocol_id)


class ProtocolSign(Resource):
    def get(self, protocol_id: str):
        return protocolService.signProtocol(protocol_id)


class Answers(Resource):
    def get(self, protocol_id):
        return protocolService.getProtocolAnswers(protocol_id)

    def post(self, protocol_id):
        answers = request.json
        return protocolService.saveProtocolAnswers(protocol_id, answers)


class Questions(Resource):
    def get(self):
        return protocolService.getQuestions()


class Testing(Resource):
    def get(self, command):
        if command == "clear_db":
            testService.clearDb()
        return True


api.add_resource(ProtocolsReports, '/protocols/reports')
api.add_resource(ProtocolSign, '/protocols/<protocol_id>/sign')
api.add_resource(Protocol, '/protocols/<protocol_id>')
api.add_resource(Answers, '/protocols/<protocol_id>/answers')
api.add_resource(Questions, '/protocols/questions')

api.add_resource(HospitalizationCommittee, '/committees')
api.add_resource(Teachers, '/teachers')
api.add_resource(Teacher, '/teachers/<teacher_id>')
api.add_resource(TeacherId, '/teacher')

if debug:
    api.add_resource(Testing, '/test/<command>')

def run_server():
    app.run(debug=debug)


if __name__ == '__main__':
    run_server()
