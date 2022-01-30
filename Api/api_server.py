from flask import Flask, flash
import flask
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
import time
from datetime import date, datetime
import threading
import queue

interval = 15

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
api = Api(app)

protocolsItems = [{"id": 0, "creation_date": "nieustalona", "character": "Hospitowany", "course": "Analiza matematyczna", "committee_head": "Adam Kowalski", "status": "Utworzony"},
                        {"id": 1, "creation_date": "2021-12-10 15:15", "character": "Hospitujący", "course": "Analiza matematyczna", "committee_head": "Adam Kowalski", "status": "Wystawiony"},
                        {"id": 2, "creation_date": "2022-02-10 15:15", "character": "Hospitowany", "course": "Analiza matematyczna", "committee_head": "Adam Kowalski", "status": "Edytowany"}]

hospitationsItems = [{"id": 0, "creation_date": "nieustalona", "character": "Hospitowany", "course": "Analiza matematyczna", "committee_head": "Adam Kowalski", "status": "Utworzony"},
                        {"id": 1, "creation_date": "2021-12-10 15:15", "character": "Hospitujący", "course": "Analiza matematyczna", "committee_head": "Adam Kowalski", "status": "Wystawiony"},
                        {"id": 2, "creation_date": "2022-02-10 15:15", "character": "Hospitowany", "course": "Analiza matematyczna", "committee_head": "Adam Kowalski", "status": "Edytowany"}]

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

class Protocols(Resource):
    def get(self):
        #time.sleep(0.5)
        return protocolsItems
 
class Hospitations(Resource):
    def get(self):
        #time.sleep(0.5)
        return hospitationsItems

    def post(self):
        final_day = "2021-12-10 15:15"
        parser = reqparse.RequestParser()
        parser.add_argument('id', required=True)
        parser.add_argument('date', required=True)
        args= parser.parse_args()
        finalDate = final_day#hospitationsItems[int(args['id'])]["final_day"]
        changed_to= args['date']

        finalDate_day = finalDate[0 : 10]
        changed_to_day = changed_to[0:10]

        finalDate_day = datetime.strptime(finalDate_day, "%Y-%m-%d")
        changed_to_day = datetime.strptime(changed_to_day, "%Y-%m-%d")


        if changed_to_day > finalDate_day:
            return "400"
        hospitationsItems[int(args['id'])]["creation_date"] = args['date']
        return "ok"


api.add_resource(Protocols, '/protocols')
api.add_resource(Hospitations, '/hospitations')
announcer = MessageAnnouncer()


def format_sse(data: str, kurs: str, major: str, event=None) -> str:
    msg = f'data: {data}|{kurs}|{major}\n\n'
    
    # msg = f'data: {data}\n'
    # msg += f'{kurs}\n'
    # msg +=  f'{major}'
    return msg

@app.route('/ping')
def ping():
    msg = format_sse(data='pong', kurs='grweg', major='hweoiufoueolinwsefkoube')
    announcer.announce(msg=msg)
    return {}, 200

@app.route('/listen', methods=['GET'])
def listen():

    def stream():
        messages = announcer.listen()  # returns a queue.Queue
        while True:
            msg = messages.get()  # blocks until a new message arrives
            yield msg

    return flask.Response(stream(), mimetype='text/event-stream')


def myPeriodicFunction():
    msg = format_sse(data='01.01.2020, 15:15', kurs='Logika dla informatyków', major='Jan Dąbrowski')
    announcer.announce(msg=msg)

def startTimer():
    threading.Timer(interval, startTimer).start()
    myPeriodicFunction()


def run_server():
    startTimer()
    app.run(debug=True)


if __name__ == '__main__':
    run_server()
