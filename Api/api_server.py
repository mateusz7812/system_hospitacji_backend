from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import true
from Control.Protocol.ProtocolService import ProtocolService
from Control.TestService import TestService
from Domain.Mediators.ProtocolMediator import ProtocolMediator
from flask_cors import CORS
from Domain.Mediators.TestMediator import TestMediator
import sys

#sys.stdout = open('D:\\home\\LogFiles\\app.log', 'w')

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
api = Api(app)

testMediator = TestMediator()
testService = TestService(testMediator)

protocolMediator = ProtocolMediator()
protocolService = ProtocolService(protocolMediator)

debug = True

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
        print(f"INFO: {command} received")
        if command == "clear_db":
            testService.clearDb()
        elif command == "heartbeat":
            return True
        elif command == "ping":    
            response = testService.check_ping()
            if response == 0:
                return True
            else:
                return False
        return False


api.add_resource(ProtocolsReports, '/api/protocols/reports')
api.add_resource(ProtocolSign, '/api/protocols/<protocol_id>/sign')
api.add_resource(Protocol, '/api/protocols/<protocol_id>')
api.add_resource(Answers, '/api/protocols/<protocol_id>/answers')
api.add_resource(Questions, '/api/protocols/questions')

if debug:
    api.add_resource(Testing, '/api/test/<command>')


@app.route('/')
def give_greeting():
    return 'Hello, world!'


def run_server():
    app.run(host="0.0.0.0", port=80, debug=debug)


if __name__ == '__main__':
    run_server()
