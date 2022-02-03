import re
from typing import List
import uuid
from flask import session
import json
from sqlalchemy.orm import aliased
from sqlalchemy import literal, null
from Domain.Business_objects.Answer import Answer
from Domain.Business_objects.HospitalizationCommittee import HospitalizationCommittee
from Domain.Business_objects.Course import Course
from Domain.Business_objects.Protocol import Protocol
from Domain.Business_objects.ProtocolDetails import ProtocolDetails
from Domain.Business_objects.ProtocolReport import ProtocolReport
from Domain.Business_objects.Question import Question
from Domain.Business_objects.Teacher import Teacher
from Domain.Business_objects.LessonGroup import LessonGroup
from Foundation.DB_adapter import db
from Domain.Business_objects.ProtocolStatus import ProtocolStatus
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Time, cast, func

def get_session():
    return sessionmaker(bind=db.engine)()


class TeacherMediator:
    def getAllTeachers(self) -> List[Teacher]:
        session = get_session()
        teachers: List[Teacher] = []
        query = session.query(db.NauczycielAkademicki).all()
        
        session.close()
        for s in query:
            teacher = get_teacher_from_model(s)
            teachers.append(teacher)
        return teachers

    def getTeacher(self, teacher_id):
        teacher: Teacher
        session = get_session()
        query = session.query(db.NauczycielAkademicki).filter(db.NauczycielAkademicki.ID == teacher_id).all()
        session.close()
        if(len(query) == 1):
            teacher = get_teacher_from_model(query[0])
            return teacher
        return null

    def getTeacherId(self, teacher_firstName, teacher_lastName, teacher_zhz):
        session = get_session()
        query = session.query(db.NauczycielAkademicki).filter(db.NauczycielAkademicki.Imie == teacher_firstName).filter(db.NauczycielAkademicki.Nazwisko == teacher_lastName).filter(db.NauczycielAkademicki.Należy_do_ZHZ == teacher_zhz).all()
        session.close()
        if(len(query) == 1):
            return query[0].ID
        return null

def get_teacher_from_model(s: db.NauczycielAkademicki):
    return Teacher(
        s.Imie,
        s.Nazwisko,
        str(s.Tytul),
        s.Należy_do_ZHZ == 1
    )