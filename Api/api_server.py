from ast import arg
import json
from flask import Flask, request, flash
import flask
from flask_restful import Resource, Api, reqparse
from Control.Protocol.ProtocolService import ProtocolService
from Control.Hospitation.HospitationService import HospitationService
from Control.TestService import TestService
from Domain.Business_objects.Teacher import Teacher
from Domain.Mediators.ProtocolMediator import ProtocolMediator
from Domain.Mediators.HospitationMediator import HospitationMediator
from flask_cors import CORS
import time
from datetime import date, datetime, timedelta
import threading
import queue

interval = 60

from Domain.Mediators.TestMediator import TestMediator

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
api = Api(app)

class MessageAnnouncer:

    def __init__(self):
        self.listeners = []

    def listen(self):
        q = queue.Queue(maxsize=5)
        self.listeners.append(q)
        return q

    def announce(self, msg):
        for i in reversed(range(len(self.listeners))):
            try:
                self.listeners[i].put_nowait(msg)
            except queue.Full:
                del self.listeners[i]

testMediator = TestMediator()
testService = TestService(testMediator)

protocolMediator = ProtocolMediator()
protocolService = ProtocolService(protocolMediator)

hospitationMediator = HospitationMediator()
hospitationService = HospitationService(hospitationMediator)

debug = True

class ProtocolsReports(Resource):
    def get(self):
        args = request.args
        teacher_id = args['teacher_id']
        return protocolService.getTeachersProtocolsReports(teacher_id)
        

class Hospitations(Resource):
    def get(self):
        args = request.args
        teacher_id = args['teacher_id']
        return hospitationService.getAllHospitations(teacher_id)

class HospitationsEdit(Resource):
    def get(self):
        args = request.args
        hospitation_id = args['hospitation_id']
        date = args['date']
        return hospitationService.saveHospitationDate(hospitation_id, date)

announcer = MessageAnnouncer()


def format_sse(data: str, kurs: str, major: str, event=None) -> str:
    msg = f'data: {data}|{kurs}|{major}\n\n'
    return msg

@app.route('/listen', methods=['GET'])
def listen():
    def stream():
        messages = announcer.listen()  # returns a queue.Queue
        while True:
            msg = messages.get()  # blocks until a new message arrives
            yield msg
    return flask.Response(stream(), mimetype='text/event-stream')


def myPeriodicFunction():
    temp = hospitationService.getNotificationData()
    msg = format_sse(data= temp[0], kurs=temp[1], major=temp[2])
    selectedDate =  temp[0].split('-')
    selectedDate = datetime(int(selectedDate[0]), int(selectedDate[1]), int(selectedDate[2][:2]))
    if (selectedDate < datetime.now() + timedelta(days=7)) and selectedDate > datetime.now():
        announcer.announce(msg=msg)
    

def startTimer():
    threading.Timer(interval, startTimer).start()
    myPeriodicFunction()

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
api.add_resource(HospitationsEdit, '/hospitations/edit')
api.add_resource(Hospitations, '/hospitations')

def run_server():
    startTimer()
    app.run(debug=debug)


if __name__ == '__main__':
    run_server()

if debug:
    api.add_resource(Testing, '/test/<command>')







