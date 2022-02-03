from Domain.Business_objects.Teacher import Teacher
from typing import List

class HospitalizationCommittee: 
    def __init__(self, id: str, committee_head: Teacher, committee_members: List[Teacher]) -> None:
        self.id = id
        self.committee_head = committee_head
        self.committee_members = committee_members
