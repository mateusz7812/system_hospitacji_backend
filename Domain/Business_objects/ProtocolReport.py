
import json

class ProtocolReport:
    def __init__(self, id, creation_date, character, course, committee_head, status) -> None:
        self.id = id
        self.creation_date = str(creation_date)
        self.character = character
        self.course = course
        self.committee_head = committee_head
        self.status = status