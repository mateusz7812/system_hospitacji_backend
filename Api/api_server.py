import json
from flask import Flask, request
from flask_restful import Resource, Api
from Control.Protocol.ProtocolService import ProtocolService
from Domain.Mediators.ProtocolMediator import ProtocolMediator
from flask_cors import CORS
import time

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
api = Api(app)

protocolMediator = ProtocolMediator()
protocolService = ProtocolService(protocolMediator)

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

api.add_resource(ProtocolsReports, '/protocols/reports')
api.add_resource(ProtocolSign, '/protocols/<protocol_id>/sign')
api.add_resource(Protocol, '/protocols/<protocol_id>')
api.add_resource(Answers, '/protocols/<protocol_id>/answers')
api.add_resource(Questions, '/protocols/questions')

def run_server():
    app.run(debug=True)


if __name__ == '__main__':
    run_server()
