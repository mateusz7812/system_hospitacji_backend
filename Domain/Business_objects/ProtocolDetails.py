
from typing import List
from Domain.Business_objects.Course import Course
from Domain.Business_objects.LessonGroup import LessonGroup
from Domain.Business_objects.Protocol import Protocol
from Domain.Business_objects.Teacher import Teacher


class ProtocolDetails:
    def __init__(self, protocol: Protocol, hospitalized: Teacher, hospitals: List[Teacher], course: Course, group: LessonGroup) -> None:
        self.protocol = protocol
        self.hospitalized = hospitalized
        self.hospitals = hospitals
        self.course = course
        self.group = group
