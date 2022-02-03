import re
from typing import List
import uuid
import json
from Control.Teacher.TeacherService import TeacherService
from Domain.Mediators.TeacherMediator import TeacherMediator
from flask import session
import json
from sqlalchemy.orm import aliased
from sqlalchemy import literal
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




class HospitalizationCommitteeMediator:
    def getAllHospitalizationCommittees(self) -> List[HospitalizationCommittee]:
        session = get_session()
        hospitalizationCommittees: List[HospitalizationCommittee] = []
        query = session.query(db.KomisjaHospitujaca).all()
        session.close()
        for s in query:
            hospitalizationCommittee = get_hospitalizationCommittee_from_model(s)
            hospitalizationCommittees.append(hospitalizationCommittee)
        return hospitalizationCommittees

    def createNewHospitalizationCommittee(self, p: HospitalizationCommittee) -> None:

        hospitalizationCommittee = db.KomisjaHospitujaca()
        p=json.loads(p)
        hospitalizationCommittee.ID = p["id"]
        hospitalizationCommittee.PrzewodniczacyID = p["committee_head"]
        for item in p["committee_members"]:
            
            itemToAdd = db.NauczycielAkademicki()
            itemToAdd.Należy_do_ZHZ = item["zhz"] == 1
            itemToAdd.Nazwisko = item["last_name"]
            itemToAdd.Imie = item["first_name"]
            itemToAdd.Tytul = item["title"]
            session = get_session()
            query = session.query(db.NauczycielAkademicki).filter(db.NauczycielAkademicki.Imie == itemToAdd.Imie).filter(db.NauczycielAkademicki.Nazwisko == itemToAdd.Nazwisko).filter(db.NauczycielAkademicki.Należy_do_ZHZ == itemToAdd.Należy_do_ZHZ).all()
            itemToAdd.ID = query[0].ID
            itemToAdd.Pesel = query[0].Pesel
            itemToAdd.Haslo = query[0].Haslo
            hospitalizationCommittee.Czlonkowie.append(query[0])
            session.commit()
            session.close()

        
        session = get_session()
        session.add(hospitalizationCommittee)
        session.commit()
        session.close()
        

def get_teacher_from_model(s: db.NauczycielAkademicki):
    return Teacher(
        s.Imie,
        s.Nazwisko,
        str(s.Tytul),
        s.Należy_do_ZHZ == 1
    )

def get_hospitalizationCommittee_from_model(s: db.KomisjaHospitujaca):
    return HospitalizationCommittee(
        s.ID,
        s.PrzewodniczacyID,
        list(map(get_teacher_from_model, s.Czlonkowie))
    )
