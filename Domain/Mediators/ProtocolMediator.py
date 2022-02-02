import re
from typing import List
import uuid
from flask import session
import json
from sqlalchemy.orm import aliased
from sqlalchemy import literal
from Domain.Business_objects.Answer import Answer
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


def status_to_str(statusInt):
    if(statusInt == ProtocolStatus.UTWORZONY.value):
        return "Utworzony"
    elif(statusInt == ProtocolStatus.EDYTOWANY.value):
        return "Edytowany"
    elif(statusInt == ProtocolStatus.PODPISANY.value):
        return "Podpisany"
    elif(statusInt == ProtocolStatus.WYSTAWIONY.value):
        return "Wystawiony"
    else:
        return "Inny"


def course_form_to_str(formInt):
    if(formInt == 0):
        return "Stacjonarna"
    else:
        return "Zaoczna"


def group_form_to_str(formInt):
    if(formInt == 0):
        return "Laboratiorium"
    else:
        return "Wykład"


def get_weekday_name(weekdayInt):
    days = ["Poniedziałek", "Wtorek", "Środa",
            "Czwartek", "Piątek", "Sobota", "Niedziela"]
    return days[weekdayInt]


def get_protocol_from_model(s: db.Protokol):
    return Protocol(
        s.ID,
        s.Zapoznano_sie_z_karta_przedmiotu == 1,
        status_to_str(s.Status),
        str(s.Data_utworzenia or ''),
        str(s.Data_wystawienia or ''),
        str(s.Data_podpisu or ''),
        str(s.Data_odwolania or ''),
        s.Komisja_hospitujacaID
    )


def get_question_from_model(s: db.Pytanie):
    return Question(
        s.ID,
        s.Tresc
    )


def get_course_from_model(s: db.Kurs):
    return Course(
        s.ID,
        s.Nazwa_kursu,
        "I" * s.Stopien_studiow,
        course_form_to_str(s.Forma_studiow),
        s.Semestr
    )


def get_answer_from_model(s: db.Odpowiedz):
    return Answer(
        s.Tresc,
        s.PytanieID
    )


def get_teacher_from_model(s: db.NauczycielAkademicki):
    return Teacher(
        s.Imie,
        s.Nazwisko,
        str(s.Tytul),
        s.Nalezy_do_ZHZ == 1
    )


def get_group_from_model(s: db.GrupaZajeciowa):
    return LessonGroup(
        s.ID,
        group_form_to_str(s.Forma),
        get_weekday_name(s.Dzien_tygodnia),
        s.Budynek,
        s.Sala,
        s.Godzina.strftime("%H:%M")
    )

def get_question_answers_for_protocol(protocol_id, question_id, session):
    return session.query(db.Odpowiedz)\
        .filter(db.Odpowiedz.ProtokolID == protocol_id)\
        .filter(db.Odpowiedz.PytanieID == question_id)\
        .all()

def get_question_by_id(session, question_id):
    query = session.query(db.Pytanie)\
            .filter(db.Pytanie.ID == question_id)\
            .all()
    if len(query) == 1:
        return query[0]
    return None

def answer_text_is_valid(question, answer):
    if question.count(":") == 1:
        return True
    check = question[question.rindex(":")+1:-1]
    x = answer
    result = eval(check)
    return result

def get_field_name(field):
    return field[1:field.index(':')]

def get_fields_from_question(question):
    regex = "{[a-z | 0-9 |: |\/|\>|_|=]*\}"
    ret = re.findall(regex, question)
    return ret

def get_value_from_answer(answer, name):
    answer_dict = json.loads(answer)
    if name in answer_dict.keys():
        return answer_dict[name]
    return None

class ProtocolMediator:
    def getAllProtocols(self) -> List[Protocol]:
        session = get_session()
        protocols: List[Protocol] = []
        query = session.query(db.Protokol).all()
        session.close()
        for s in query:
            protocol = get_protocol_from_model(s)
            protocols.append(protocol)
        return protocols

    def createNewProtocol(self, p: Protocol) -> None:
        protocol = db.Protokol()
        protocol.ID = p.id
        protocol.Zapoznano_sie_z_karta_przedmiotu = int(
            p.course_card_read)
        protocol.Komisja_hospitujacaID = p.hospitalization_commitee_id
        protocol.Status = p.status.value
        protocol.Data_utworzenia = p.creation_date

        session = get_session()
        session.add(protocol)
        session.commit()
        session.close()

    def getTeacherProtocolsReports(self, teacher_id):
        session = get_session()
        reports: List[ProtocolReport] = []
        nauczyciele = aliased(db.NauczycielAkademicki)
        query1 = session.query(db.Protokol.ID, db.Protokol.Data_utworzenia, db.Protokol.Status, literal("Hospitowany").label("Charakter"), db.Kurs.Nazwa_kursu, db.KomisjaHospitujaca.PrzewodniczacyID, nauczyciele.Imie, nauczyciele.Nazwisko)\
            .join(db.Hospitacja, db.Hospitacja.ID == db.Protokol.HospitacjaID)\
            .filter(db.Hospitacja.HospitowanyID == teacher_id)\
            .join(db.Zajecia, db.Hospitacja.ZajeciaID == db.Zajecia.ID)\
            .join(db.Kurs, db.Zajecia.KursID == db.Kurs.ID)\
            .join(db.KomisjaHospitujaca, db.KomisjaHospitujaca.ID == db.Protokol.Komisja_hospitujacaID)\
            .join(nauczyciele, db.KomisjaHospitujaca.PrzewodniczacyID == nauczyciele.ID)

        query2 = session.query(db.Protokol.ID, db.Protokol.Data_utworzenia, db.Protokol.Status, literal("Hospitujący").label("Charakter"), db.Kurs.Nazwa_kursu, db.KomisjaHospitujaca.PrzewodniczacyID, nauczyciele.Imie, nauczyciele.Nazwisko)\
            .join(db.KomisjaHospitujaca, db.KomisjaHospitujaca.ID == db.Protokol.Komisja_hospitujacaID)\
            .join(db.NauczycielAkademicki, db.NauczycielAkademicki.ID == db.KomisjaHospitujaca.PrzewodniczacyID)\
            .filter(db.KomisjaHospitujaca.PrzewodniczacyID == teacher_id)\
            .join(db.Hospitacja, db.Hospitacja.ID == db.Protokol.HospitacjaID)\
            .join(db.Zajecia, db.Hospitacja.ZajeciaID == db.Zajecia.ID)\
            .join(db.Kurs, db.Zajecia.KursID == db.Kurs.ID)\
            .join(nauczyciele, db.KomisjaHospitujaca.PrzewodniczacyID == nauczyciele.ID)

        union_query = query1.union(query2).all()
        session.close()
        for s in union_query:
            report = ProtocolReport(
                s.ID,
                s.Data_utworzenia,
                s.Charakter,
                s.Nazwa_kursu,
                f"{s.Imie} {s.Nazwisko}",
                status_to_str(s.Status)
            )
            reports.append(report)

        return reports

    def getProtocolDetails(self, protocol_id):
        session = get_session()
        query = session.query(db.Protokol, db.Kurs, db.GrupaZajeciowa, db.Hospitacja.Komisja_hospitujacaID,
                              # cast(db.Hospitacja.Data_przeprowadzenia, Time),
                              db.Hospitacja.Data_przeprowadzenia, db.GrupaZajeciowa.Godzina, db.NauczycielAkademicki,
                              #func.extract('dow', db.Hospitacja.Data_przeprowadzenia),
                              db.GrupaZajeciowa.Dzien_tygodnia)\
            .filter(db.Protokol.ID == protocol_id)\
            .join(db.Hospitacja, db.Hospitacja.ID == db.Protokol.HospitacjaID)\
            .join(db.NauczycielAkademicki, db.NauczycielAkademicki.ID == db.Hospitacja.HospitowanyID)\
            .join(db.Zajecia, db.Zajecia.ID == db.Hospitacja.ZajeciaID)\
            .join(db.Kurs, db.Kurs.ID == db.Zajecia.KursID)\
            .join(db.GrupaZajeciowa, db.GrupaZajeciowa.ZajeciaID == db.Zajecia.ID)\
            .all()
        # .filter(db.Hospitacja.Data_przeprowadzenia.strftime('%H:%M') == db.GrupaZajeciowa.Godzina)\
        # .filter(db.Hospitacja.Data_przeprowadzenia.weekday() == db.GrupaZajeciowa.Dzien_tygodnia)\

        if len(query) == 1:
            hospitals = session.query(db.KomisjaHospitujaca)\
                .filter(db.KomisjaHospitujaca.ID == query[0].Komisja_hospitujacaID).one().Czlonkowie
            session.close()
            protocol_details = ProtocolDetails(get_protocol_from_model(query[0].Protokol), get_teacher_from_model(query[0].NauczycielAkademicki), list(
                map(get_teacher_from_model, hospitals)), get_course_from_model(query[0].Kurs), get_group_from_model(query[0].GrupaZajeciowa))
            return protocol_details
        session.close()
        return None

    def getProtocolAnswers(self, protocol_id):
        session = get_session()
        query = session.query(db.Odpowiedz)\
            .filter(db.Odpowiedz.ProtokolID == protocol_id)\
            .all()
        session.close()
        return list(map(get_answer_from_model, query))

    def saveProtocolAnswer(self, protocol_id, answer: Answer):
        session = get_session()
        pytanie = get_question_by_id(session, answer.question_id)
        if pytanie is None:
            return None
        query = get_question_answers_for_protocol(protocol_id, answer.question_id, session)
        odpowiedz: db.Odpowiedz
        if len(query) == 0:
            odpowiedz = db.Odpowiedz()
            odpowiedz.ID = str(uuid.uuid4())[:25]
            odpowiedz.ProtokolID = protocol_id
            odpowiedz.PytanieID = answer.question_id
            odpowiedz.Tresc = json.dumps({})
            session.add(odpowiedz)
        else:
            odpowiedz = query[0]
        fields = get_fields_from_question(pytanie.Tresc)
        not_valid_fields = []
        answer_text = json.loads(odpowiedz.Tresc)
        for field in fields:
            name = get_field_name(field)
            value = get_value_from_answer(answer.text, name)
            if value:
                if answer_text_is_valid(field, value):
                    answer_text[name] = value
                else:
                    not_valid_fields.append({
                        "question_id": answer.question_id,
                        "name": name
                    })
        odpowiedz.Tresc = json.dumps(answer_text)
        session.commit()
        session.close()
        return not_valid_fields


    def getQuestions(self):
        session = get_session()
        query = session.query(db.Pytanie).all()
        session.close()
        return list(map(get_question_from_model, query))

    def signProtocol(self, protocol_id):
        session = get_session()
        query = session.query(db.Protokol).filter(db.Protokol.ID == protocol_id).all()
        query[0].Status = ProtocolStatus.PODPISANY.value
        session.commit()
        session.close()
        return True
