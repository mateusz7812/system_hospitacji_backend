from flask import Flask
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

class Protocols(Resource):
    def get(self):
        time.sleep(0.5)
        protocolsItems = [{"id": 0, "creation_date": "nieustalona", "character": "Hospitowany", "course": "Analiza matematyczna", "committee_head": "Adam Kowalski", "status": "Utworzony"},
                        {"id": 1, "creation_date": "2021-12-10 15:15", "character": "Hospitujący", "course": "Analiza matematyczna", "committee_head": "Adam Kowalski", "status": "Wystawiony"},
                        {"id": 2, "creation_date": "2022-02-10 15:15", "character": "Hospitowany", "course": "Analiza matematyczna", "committee_head": "Adam Kowalski", "status": "Edytowany"}]
        return protocolsItems

api.add_resource(Protocols, '/protocols')

def run_server():
    app.run(debug=True)


if __name__ == '__main__':
    run_server()
