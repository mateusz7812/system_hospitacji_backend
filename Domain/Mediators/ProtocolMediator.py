import contextlib
from typing import List
from Domain.Business_objects.Protocol import Protocol
from Domain.Business_objects.ProtocolReport import ProtocolReport
from Foundation.DB_adapter import db
from Domain.Business_objects.ProtocolStatus import ProtocolStatus
from sqlalchemy.orm import sessionmaker


def getSession():
    return sessionmaker(bind=db.engine)()


class ProtocolMediator:
    def getAllProtocols(self) -> List[Protocol]:
        session = getSession()
        protocols: List[Protocol] = []
        query = session.query(db.Protokol).all()
        for s in query:
            protocol = Protocol(
                s.ID,
                s.Zapoznano_sie_z_karta_przedmiotu == 1,
                ProtocolStatus(s.Status),
                s.Data_utworzenia,
                s.Data_wystawienia,
                s.Data_podpisu,
                s.Data_odwolania,
                s.Komisja_hospitujacaID
            )
            protocols.append(protocol)
        return protocols

    def createNewProtocol(self, p: Protocol) -> None:
        protocol = db.Protokol()
        protocol.ID = p.id
        protocol.Zapoznano_sie_z_karta_przedmiotu = int(
            p.zapoznano_sie_z_karta_przedmiotu)
        protocol.Komisja_hospitujacaID = p.komisja_hospitujaca_id
        protocol.Status = p.status.value
        protocol.Data_utworzenia = p.data_utworzenia
        protocol.Data_wystawienia = p.data_wystawienia
        protocol.Data_podpisu = p.data_podpisu
        protocol.Data_odwolania = p.data_odwołania

        session = getSession()
        session.add(protocol)
        session.commit()

    def getTeacherProtocolsReports(self, teacher_id):
        
        session = getSession()
        reports: List[ProtocolReport] = []
        query = session.query(db.Protokol, db.Hospitacja).join(db.Hospitacja, db.Hospitacja.ID == db.Protokol.HospitacjaID).filter(db.Hospitacja.Nauczyciel_akademickiID == teacher_id).all()
        for s in query:
            print(s)
            report = ProtocolReport(
                s.Protokol.ID,
                s.Protokol.Data_utworzenia,
                "Hospitowany",
                "",
                "",
                ""
                #s.Nazwa_kursu,
            )
            reports.append(report)
        return reports

