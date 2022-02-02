from ntpath import join
import re
from typing import List
import uuid
from flask import session
import json
from sqlalchemy.orm import aliased
from sqlalchemy import Date, literal
from Domain.Business_objects.Answer import Answer
from Domain.Business_objects.Course import Course
from Domain.Business_objects.Protocol import Protocol
from Domain.Business_objects.ProtocolDetails import ProtocolDetails
from Domain.Business_objects.ProtocolReport import ProtocolReport
from Domain.Business_objects.Question import Question
from Domain.Business_objects.Teacher import Teacher
from Domain.Business_objects.LessonGroup import LessonGroup
from Foundation.DB_adapter import db
from Domain.Business_objects.Hospitations import Hospitation
from sqlalchemy.orm import sessionmaker
from sqlalchemy import cast, func
from datetime import datetime, time


def get_session():
    return sessionmaker(bind=db.engine)()

def get_protocol_from_model(s: any):
    print(s.ID, s.Data_przeprowadzenia)
    return Hospitation(
        s.ID,
        str(s.Data_przeprowadzenia) + " 10:15",
        s.Nazwa_kursu,
        s.Imie +' ' + s.Nazwisko,
        "Utworzona",
        "Hospitowany"
    )
    # self.id = id
    #     self.creation_date = creation_date
    #     self.course = course
    #     self.committee_head = committee_head
    #     self.status = status
    #"id": 0, "creation_date": "nieustalona", "character": "Hospitowany", "course": "Analiza matematyczna", "committee_head": "Adam Kowalski", "status": "Utworzony"



class HospitationMediator:
    def getAllHospitations(self, teacher_id) -> List[Hospitation]:
        #self.createNewProtocol()
        session = get_session()
        protocols: List[Hospitation] = []
        query = session.query(db.Hospitacja.ID,db.Hospitacja.Data_przeprowadzenia,db.Hospitacja.Zajecia, db.Zajecia.Kurs, db.Kurs.Nazwa_kursu, db.Hospitacja.Komisja_hospitujaca, db.NauczycielAkademicki.Imie, db.NauczycielAkademicki.Nazwisko)\
            .join(db.Zajecia, db.Zajecia.ID == db.Hospitacja.ZajeciaID)\
            .join(db.Kurs, db.Zajecia.KursID == db.Kurs.ID)\
            .join(db.KomisjaHospitujaca, db.Hospitacja.Komisja_hospitujacaID == db.KomisjaHospitujaca.ID)\
            .join(db.NauczycielAkademicki,  db.KomisjaHospitujaca.PrzewodniczacyID == db.NauczycielAkademicki.ID)\
            .filter(db.Hospitacja.HospitowanyID == teacher_id)
            #.join(db.NauczycielAkademicki.Imie, db.NauczycielAkademicki.ID == db.KomisjaHospitujaca.PrzewodniczacyID)
            # .filter(db.NauczycielAkademicki.ID == db.Hospitacja.Nauczyciel_akademicki.ID)\
            #.filter(db.KomisjaHospitujaca.ID == db.Hospitacja.Komisja_hospitujaca)\
            #.join(db.NauczycielAkademicki, db.NauczycielAkademicki.ID == db.KomisjaHospitujaca.PrzewodniczacyID)\
        print(query)
        session.close()
        for s in query:
            protocol = get_protocol_from_model(s)
            protocols.append(protocol)
        return protocols


    def getTeachersHospitations(self, teacher_id):
            session = get_session()
            hospitations: List[Hospitation] = []
            # nauczyciele = aliased(db.NauczycielAkademicki)
            query1 = session.query(db.Hospitacja.HospitowanyID, db.Hospitacja.Data_przeprowadzenia)\
                .join(db.Hospitacja, db.Hospitacja.HospitowanyID == teacher_id)

            session.close()
            for s in query1:
                hospitation = Hospitation(
                    s.HospitowanyID,
                    s.Data_przeprowadzenia
                )
                hospitations.append(hospitation)

            return hospitations
            
    def saveHospitationDate(self, hospitation_id, date):
        session = get_session()
        query = session.query(db.Hospitacja).filter(db.Hospitacja.ID == hospitation_id).all()
        dateInTable = date.split('-')
        query[0].Data_przeprowadzenia = datetime(int(dateInTable[0]), int(dateInTable[1]), int(dateInTable[2][:2]), 10, 15)
        if datetime(int(dateInTable[0]), int(dateInTable[1]), int(dateInTable[2][:2]), 10, 15) < datetime.today():
            return (False, 400)
        else:
            session.commit()
            session.close()
            return (True, 200)
    
    def getNotificationData(self):
        session = get_session()
        query = session.query(db.Hospitacja.ID,db.Hospitacja.Data_przeprowadzenia,db.Hospitacja.Zajecia, db.Zajecia.Kurs, db.Kurs.Nazwa_kursu, db.Hospitacja.Komisja_hospitujaca, db.NauczycielAkademicki.Imie, db.NauczycielAkademicki.Nazwisko)\
            .join(db.Zajecia, db.Zajecia.ID == db.Hospitacja.ZajeciaID)\
            .join(db.Kurs, db.Zajecia.KursID == db.Kurs.ID)\
            .join(db.KomisjaHospitujaca, db.Hospitacja.Komisja_hospitujacaID == db.KomisjaHospitujaca.ID)\
            .join(db.NauczycielAkademicki,  db.KomisjaHospitujaca.PrzewodniczacyID == db.NauczycielAkademicki.ID)\
            .filter(db.Hospitacja.HospitowanyID == '123nauczyciel')
        session.close()
        return [str(query[0].Data_przeprowadzenia) + '10:15', query[0].Nazwa_kursu, query[0].Imie + ' ' + query[0].Nazwisko]


    # def get_hospitation_by_id(session, hospitation_id):
    #     query = session.query(db.Hospitacja)\
    #             .filter(db.Hospitacja.ID == hospitation_id)\
    #             .all()
    #     if len(query) == 1:
    #         return query[0]
    #     return None   
