

from email.policy import default
import json
from mimetypes import init
from typing import List

from sqlalchemy import null
from Domain.Business_objects.Answer import Answer
from Domain.Business_objects.Teacher import Teacher
from Domain.Business_objects.ProtocolReport import ProtocolReport
from Domain.Mediators.TeacherMediator import TeacherMediator


class TeacherService():
    def __init__(self, teacherMediator: TeacherMediator) -> None:
        self.teacherMediator = teacherMediator

    def getAllTeachers(self) -> List[Teacher]:
        return list(map(lambda x: x.__dict__, self.teacherMediator.getAllTeachers()))

    def getTeacher(self, teacher_id) -> Teacher:
        teacher = self.teacherMediator.getTeacher(teacher_id)
        if teacher != null:
            teacher = teacher.__dict__
            return teacher
        return 404

    def getTeacherId(self, teacher_firstName, teacher_lastName, teacher_zhz) -> str:
        teacher_id = self.teacherMediator.getTeacherId(teacher_firstName, teacher_lastName, teacher_zhz)
        if(teacher_id != null):
            return teacher_id
        return 404

 