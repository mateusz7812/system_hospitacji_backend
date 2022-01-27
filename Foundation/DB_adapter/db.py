import contextlib
from datetime import datetime, time
import json
from sqlalchemy import Column, Date, ForeignKey, Integer, String, Table
from sqlalchemy import Column, Date, ForeignKey, Integer, String, Table, create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import TIME
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
import os

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
    Nauczyciel_akademickiID = Column(ForeignKey(
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

    zajecia = Zajecia()
    zajecia.ID = "123zajecia"
    zajecia.KursID = kurs.ID
    session.add(zajecia)

    grupa_zajeciowa = GrupaZajeciowa()
    grupa_zajeciowa.ID = "123grupa"
    grupa_zajeciowa.ZajeciaID = zajecia.ID
    grupa_zajeciowa.Forma = 0
    grupa_zajeciowa.Dzien_tygodnia = 0
    grupa_zajeciowa.Budynek = "A1"
    grupa_zajeciowa.Sala = "123a"
    grupa_zajeciowa.Godzina = time(10, 45)
    session.add(grupa_zajeciowa)

    hospitujacy = NauczycielAkademicki()
    hospitujacy.ID = "123nauczyciel"
    hospitujacy.Pesel = "12312312312"
    hospitujacy.Należy_do_ZHZ = 1
    hospitujacy.Tytul = 0
    hospitujacy.Imie = "Jan"
    hospitujacy.Nazwisko = "Kowalski"
    hospitujacy.Haslo = "1234"
    session.add(hospitujacy)

    hospitujacy2 = NauczycielAkademicki()
    hospitujacy2.ID = "345nauczyciel"
    hospitujacy2.Pesel = "12312312312"
    hospitujacy2.Należy_do_ZHZ = 1
    hospitujacy2.Tytul = 0
    hospitujacy2.Imie = "Anna"
    hospitujacy2.Nazwisko = "Kowalska"
    hospitujacy2.Haslo = "1234"
    # session.add(hospitujacy2)

    hospitowany = NauczycielAkademicki()
    hospitowany.ID = "234nauczyciel"
    hospitowany.Pesel = "23423423423"
    hospitowany.Należy_do_ZHZ = 1
    hospitowany.Tytul = 0
    hospitowany.Imie = "Adam"
    hospitowany.Nazwisko = "Kowalski"
    hospitowany.Haslo = "1234"
    hospitowany.Zajecia.append(zajecia)
    session.add(hospitowany)

    komisja = KomisjaHospitujaca()
    komisja.ID = "123komisja"
    komisja.PrzewodniczacyID = hospitujacy.ID
    komisja.Czlonkowie.append(hospitujacy2)
    session.add(komisja)

    harmonogram = HarmonogramHospitacji()
    harmonogram.ID = "123harmonogram"
    harmonogram.Data_opracowania = datetime(2021, 11, 28, 10, 45)
    session.add(harmonogram)

    hospitacja = Hospitacja()
    hospitacja.Harmonogram_hospitacjiID = harmonogram.ID
    hospitacja.Data_przeprowadzenia = datetime(2022, 1, 28, 10, 45)
    hospitacja.ID = "123hospitacja"
    hospitacja.Komisja_hospitujacaID = komisja.ID
    hospitacja.Nauczyciel_akademickiID = hospitowany.ID
    hospitacja.ZajeciaID = zajecia.ID
    session.add(hospitacja)

    pytanie = Pytanie()
    pytanie.ID = "123pytanie"
    pytanie.Tresc = "{punktualnie:tak/nie}Czy zajęcia odbyły się punktualnie, opóźnienie {opoznienie:int}"
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

    protokol = Protokol()
    protokol.ID = "123protokol"
    protokol.Komisja_hospitujacaID = komisja.ID
    protokol.Zapoznano_sie_z_karta_przedmiotu = 1
    protokol.Status = 0
    protokol.HospitacjaID = hospitacja.ID
    protokol.Data_utworzenia = datetime(2022, 1, 20, 10)
    session.add(protokol)

    odpowiedz = Odpowiedz()
    odpowiedz.ID = "123odpowiedz"
    odpowiedz.ProtokolID = protokol.ID
    odpowiedz.PytanieID = pytanie.ID
    odpowiedz.Tresc = str(json.dumps({"punktualnie": "tak", "opoznienie": 10}))
    session.add(odpowiedz)

    session.commit()


if not database_exists(engine.url):
    create_database(engine.url)
    metadata.create_all(engine)
    initialize_db()
