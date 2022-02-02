import contextlib
from datetime import datetime, time
import json
from typing import Any
from sqlalchemy import Column, Date, ForeignKey, Integer, String, Table
from sqlalchemy import Column, Date, ForeignKey, Integer, String, Table, create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import TIME
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
import os

from Domain.Business_objects.ProtocolStatus import ProtocolStatus

Base = declarative_base()
metadata = Base.metadata

db_path = os.path.join(os.path.dirname(__file__), 'sqlalchemy.sqlite')
engine = create_engine(f'sqlite:///{db_path}')


class HarmonogramHospitacji(Base):
    __tablename__ = 'Harmonogram_hospitacji'

    ID = Column(String(25), primary_key=True)
    Data_opracowania = Column(Date)


class Kurs(Base):
    __tablename__ = 'Kurs'

    ID = Column(String(25), primary_key=True)
    Nazwa_kursu = Column(String(25), nullable=False)
    Stopien_studiów = Column(Integer, nullable=False)
    Forma_studiow = Column(Integer, nullable=False)
    Semestr = Column(Integer, nullable=False)


class NauczycielAkademicki(Base):
    __tablename__ = 'Nauczyciel_akademicki'

    ID = Column(String(25), primary_key=True)
    Pesel = Column(String(11), nullable=False)
    Należy_do_ZHZ = Column(Integer)
    Tytul = Column(Integer, nullable=False)
    Imie = Column(String(25), nullable=False)
    Nazwisko = Column(String(35), nullable=False)
    Haslo = Column(String(50), nullable=False)

    Zajecia = relationship(
        'Zajecia', secondary='Zajecia_Nauczyciel_akademicki')


class Pytanie(Base):
    __tablename__ = 'Pytanie'

    ID = Column(String(25), primary_key=True)
    Tresc = Column(Integer, nullable=False)


class Zajecia(Base):
    __tablename__ = 'Zajecia'

    ID = Column(String(25), primary_key=True)
    KursID = Column(ForeignKey('Kurs.ID'), nullable=False, index=True)
    Kurs = relationship('Kurs')


class GrupaZajeciowa(Base):
    __tablename__ = 'Grupa_zajeciowa'

    ID = Column(String(25), primary_key=True)
    ZajeciaID = Column(ForeignKey('Zajecia.ID'), nullable=False, index=True)
    Forma = Column(Integer, nullable=False)
    Dzien_tygodnia = Column(Integer, nullable=False)
    Budynek = Column(String(25), nullable=False)
    Sala = Column(String(25), nullable=False)
    Godzina = Column(TIME(fsp=6), nullable=False)

    Zajecia = relationship('Zajecia')


class KomisjaHospitujaca(Base):
    __tablename__ = 'Komisja_hospitujaca'

    ID = Column(String(25), primary_key=True)
    PrzewodniczacyID = Column(ForeignKey(
        'Nauczyciel_akademicki.ID'), nullable=False, index=True)

    Nauczyciel_akademicki = relationship('NauczycielAkademicki')
    Czlonkowie = relationship(
        'NauczycielAkademicki', secondary='Komisja_hospitujaca_Nauczyciel_akademicki')


t_Zajecia_Nauczyciel_akademicki = Table(
    'Zajecia_Nauczyciel_akademicki', metadata,
    Column('ZajeciaID', ForeignKey('Zajecia.ID'),
           primary_key=True, nullable=False),
    Column('Nauczyciel_akademickiID', ForeignKey(
        'Nauczyciel_akademicki.ID'), primary_key=True, nullable=False, index=True)
)


class Hospitacja(Base):
    __tablename__ = 'Hospitacja'

    ID = Column(String(25), primary_key=True)
    HospitowanyID = Column(ForeignKey(
        'Nauczyciel_akademicki.ID'), nullable=False, index=True)
    Harmonogram_hospitacjiID = Column(ForeignKey(
        'Harmonogram_hospitacji.ID'), nullable=False, index=True)
    ZajeciaID = Column(ForeignKey('Zajecia.ID'), nullable=False, index=True)
    Komisja_hospitujacaID = Column(ForeignKey(
        'Komisja_hospitujaca.ID'), nullable=False, index=True)
    Data_przeprowadzenia = Column(Date)

    Harmonogram_hospitacji = relationship('HarmonogramHospitacji')
    Komisja_hospitujaca = relationship('KomisjaHospitujaca')
    Nauczyciel_akademicki = relationship('NauczycielAkademicki')
    Zajecia = relationship('Zajecia')


t_Komisja_hospitujaca_Nauczyciel_akademicki = Table(
    'Komisja_hospitujaca_Nauczyciel_akademicki', metadata,
    Column('Komisja_hospitującaID', ForeignKey(
        'Komisja_hospitujaca.ID'), primary_key=True, nullable=False),
    Column('Nauczyciel_akademickiID', ForeignKey(
        'Nauczyciel_akademicki.ID'), primary_key=True, nullable=False, index=True)
)


class Protokol(Base):
    __tablename__ = 'Protokol'

    ID = Column(String(25), primary_key=True)
    Komisja_hospitujacaID = Column(ForeignKey(
        'Komisja_hospitujaca.ID'), nullable=False, index=True)
    Zapoznano_sie_z_karta_przedmiotu = Column(Integer)
    Status = Column(Integer)
    Data_utworzenia = Column(Date)
    Data_wystawienia = Column(Date)
    Data_podpisu = Column(Date)
    Data_odwolania = Column(Date)
    HospitacjaID = Column(ForeignKey('Hospitacja.ID'),
                          nullable=True, index=True)

    Hospitacja = relationship('Hospitacja')
    Komisja_hospitujaca = relationship('KomisjaHospitujaca')


class Odpowiedz(Base):
    __tablename__ = 'Odpowiedz'

    ID = Column(String(25), primary_key=True)
    PytanieID = Column(ForeignKey('Pytanie.ID'), nullable=False, index=True)
    Tresc = Column(String(255))
    ProtokolID = Column(ForeignKey('Protokol.ID'), nullable=False, index=True)

    Protokol = relationship('Protokol')
    Pytanie = relationship('Pytanie')


def cleanUpDB() -> None:
    with contextlib.closing(engine.connect()) as con:
        trans = con.begin()
        for table in reversed(metadata.sorted_tables):
            con.execute(table.delete())
        trans.commit()


def getSession():
    return sessionmaker(bind=engine)()


def initialize_db():
    session = getSession()

    kurs = Kurs()
    kurs.ID = "123kurs"
    kurs.Nazwa_kursu = "Analiza matematyczna"
    kurs.Stopien_studiów = 1
    kurs.Forma_studiow = 0
    kurs.Semestr = 3
    session.add(kurs)

    zajecia1 = Zajecia()
    zajecia1.ID = "123zajecia"
    zajecia1.KursID = kurs.ID
    session.add(zajecia1)

    zajecia2 = Zajecia()
    zajecia2.ID = "234zajecia"
    zajecia2.KursID = kurs.ID
    session.add(zajecia2)

    grupa_zajeciowa1 = GrupaZajeciowa()
    grupa_zajeciowa1.ID = "123grupa"
    grupa_zajeciowa1.ZajeciaID = zajecia1.ID
    grupa_zajeciowa1.Forma = 0
    grupa_zajeciowa1.Dzien_tygodnia = 0
    grupa_zajeciowa1.Budynek = "A1"
    grupa_zajeciowa1.Sala = "123a"
    grupa_zajeciowa1.Godzina = time(10, 45)
    session.add(grupa_zajeciowa1)

    grupa_zajeciowa2 = GrupaZajeciowa()
    grupa_zajeciowa2.ID = "234grupa"
    grupa_zajeciowa2.ZajeciaID = zajecia2.ID
    grupa_zajeciowa2.Forma = 0
    grupa_zajeciowa2.Dzien_tygodnia = 1
    grupa_zajeciowa2.Budynek = "A1"
    grupa_zajeciowa2.Sala = "123a"
    grupa_zajeciowa2.Godzina = time(10, 45)
    session.add(grupa_zajeciowa2)

    nauczyciel1 = NauczycielAkademicki()
    nauczyciel1.ID = "123nauczyciel"
    nauczyciel1.Pesel = "12312312312"
    nauczyciel1.Należy_do_ZHZ = 1
    nauczyciel1.Tytul = 0
    nauczyciel1.Imie = "Jan"
    nauczyciel1.Nazwisko = "Kowalski"
    nauczyciel1.Haslo = "1234"
    nauczyciel1.Zajecia.append(zajecia2)
    session.add(nauczyciel1)

    nauczyciel2 = NauczycielAkademicki()
    nauczyciel2.ID = "345nauczyciel"
    nauczyciel2.Pesel = "12312352312"
    nauczyciel2.Należy_do_ZHZ = 1
    nauczyciel2.Tytul = 0
    nauczyciel2.Imie = "Anna"
    nauczyciel2.Nazwisko = "Kowalska"
    nauczyciel2.Haslo = "1234"
    session.add(nauczyciel2)

    nauczyciel3 = NauczycielAkademicki()
    nauczyciel3.ID = "234nauczyciel"
    nauczyciel3.Pesel = "23423423423"
    nauczyciel3.Należy_do_ZHZ = 1
    nauczyciel3.Tytul = 0
    nauczyciel3.Imie = "Adam"
    nauczyciel3.Nazwisko = "Kowalski"
    nauczyciel3.Haslo = "1234"
    nauczyciel3.Zajecia.append(zajecia1)
    session.add(nauczyciel3)

    komisja1 = KomisjaHospitujaca()
    komisja1.ID = "123komisja"
    komisja1.PrzewodniczacyID = nauczyciel1.ID
    komisja1.Czlonkowie.append(nauczyciel2)
    session.add(komisja1)
    
    komisja2 = KomisjaHospitujaca()
    komisja2.ID = "234komisja"
    komisja2.PrzewodniczacyID = nauczyciel3.ID
    komisja2.Czlonkowie.append(nauczyciel2)
    session.add(komisja2)

    harmonogram = HarmonogramHospitacji()
    harmonogram.ID = "123harmonogram"
    harmonogram.Data_opracowania = datetime(2021, 11, 28, 10, 45)
    session.add(harmonogram)

    hospitacja1 = Hospitacja()
    hospitacja1.Harmonogram_hospitacjiID = harmonogram.ID
    hospitacja1.Data_przeprowadzenia = datetime(2022, 1, 28, 10, 15)
    hospitacja1.ID = "123hospitacja"
    hospitacja1.Komisja_hospitujacaID = komisja1.ID
    hospitacja1.HospitowanyID = nauczyciel3.ID
    hospitacja1.ZajeciaID = zajecia1.ID
    session.add(hospitacja1)

    hospitacja2 = Hospitacja()
    hospitacja2.Harmonogram_hospitacjiID = harmonogram.ID
    hospitacja2.Data_przeprowadzenia = datetime(1000, 1, 1, 0, 0)
    hospitacja2.ID = "23344hospitacja"
    hospitacja2.Komisja_hospitujacaID = komisja2.ID
    hospitacja2.HospitowanyID = nauczyciel1.ID
    hospitacja2.ZajeciaID = zajecia2.ID
    session.add(hospitacja2)


    hospitacja2 = Hospitacja()
    hospitacja2.Harmonogram_hospitacjiID = harmonogram.ID
    hospitacja2.Data_przeprowadzenia = datetime(2022, 1, 28, 10, 15)
    hospitacja2.ID = "2334hospitacja"
    hospitacja2.Komisja_hospitujacaID = komisja2.ID
    hospitacja2.HospitowanyID = nauczyciel1.ID
    hospitacja2.ZajeciaID = zajecia2.ID
    session.add(hospitacja2)


    hospitacja2 = Hospitacja()
    hospitacja2.Harmonogram_hospitacjiID = harmonogram.ID
    hospitacja2.Data_przeprowadzenia = datetime(2022, 1, 28, 10, 45)
    hospitacja2.ID = "234hospitacja"
    hospitacja2.Komisja_hospitujacaID = komisja2.ID
    hospitacja2.HospitowanyID = nauczyciel1.ID
    hospitacja2.ZajeciaID = zajecia2.ID
    session.add(hospitacja2)


    pytanie = Pytanie()
    pytanie.ID = "123pytanie"
    pytanie.Tresc = "{punktualnie:tak/nie}Czy zajęcia odbyły się punktualnie, opóźnienie {opoznienie:int:x>=0}"
    session.add(pytanie)

    pytanie1 = Pytanie()
    pytanie1.ID = "234pytanie"
    pytanie1.Tresc = "{sprawdzono:tak/nie/nie_dotyczy}Czy sprawdzono obecność studentów\nJeśli tak - liczba obecnych {obecni:int} / zapisanych {zapisani:int}"
    session.add(pytanie1)

    pytanie2 = Pytanie()
    pytanie2.ID = "345pytanie"
    pytanie2.Tresc = "{przystosowane:tak/nie}Czy sala i jej wyposażenie są przystosowane do formy prowadzonych zajęć.\nJeżeli nie, to z jakich powodów {powody:text_area}"
    session.add(pytanie2)

    pytanie3 = Pytanie()
    pytanie3.ID = "456pytanie"
    pytanie3.Tresc = "{zgodna:tak/nie}Treść zajęć jest zgodna z programem kursu i umożliwia osiągnięcie założonych efektów uczenia się ujętych w Karcie Przedmiotu"
    session.add(pytanie3)

    pytanie4 = Pytanie()
    pytanie4.ID = "567pytanie"
    pytanie4.Tresc = "{uwagi:text_area}Inne uwagi, wnioski i zalecenia dotyczące formalnej strony zajęć:"
    session.add(pytanie4)

    protokol1 = Protokol()
    protokol1.ID = "123protokol"
    protokol1.Komisja_hospitujacaID = komisja1.ID
    protokol1.Zapoznano_sie_z_karta_przedmiotu = 1
    protokol1.Status = ProtocolStatus.EDYTOWANY.value
    protokol1.HospitacjaID = hospitacja1.ID
    protokol1.Data_utworzenia = datetime(2022, 1, 20, 10)
    session.add(protokol1)

    protokol2 = Protokol()
    protokol2.ID = "2234protokol"
    protokol2.Komisja_hospitujacaID = komisja2.ID
    protokol2.Zapoznano_sie_z_karta_przedmiotu = 1
    protokol2.Status = ProtocolStatus.WYSTAWIONY.value
    protokol2.HospitacjaID = hospitacja2.ID
    protokol2.Data_utworzenia = datetime(2022, 1, 20, 10)
    session.add(protokol2)

    odpowiedz1 = Odpowiedz()
    odpowiedz1.ID = "123odpowiedz"
    odpowiedz1.ProtokolID = protokol1.ID
    odpowiedz1.PytanieID = pytanie.ID
    odpowiedz1.Tresc = str(json.dumps({"punktualnie": "nie", "opoznienie": 10}))
    session.add(odpowiedz1)

    odpowiedz2 = Odpowiedz()
    odpowiedz2.ID = "234odpowiedz"
    odpowiedz2.ProtokolID = protokol2.ID
    odpowiedz2.PytanieID = pytanie.ID
    odpowiedz2.Tresc = str(json.dumps({"punktualnie": "tak"}))
    session.add(odpowiedz2)

    session.commit()


if not database_exists(engine.url):
    create_database(engine.url)
    metadata.create_all(engine)
    initialize_db()
