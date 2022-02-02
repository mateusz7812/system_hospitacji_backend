
import json


class Hospitation:
    def __init__(self, id, creation_date, course, committee_head, status, test):
        self.id = id
        self.creation_date = creation_date
        self.course = course
        self.committee_head = committee_head
        self.status = status
        self.test = test