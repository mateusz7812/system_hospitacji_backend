import contextlib
from sqlalchemy import Column, Date, ForeignKey, Integer, String, Table
from sqlalchemy import Column, Date, ForeignKey, Integer, String, Table, create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import TIME
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database
import os

Base = declarative_base()
metadata = Base.metadata

db_path = os.path.join(os.path.dirname(__file__), 'sqlalchemy.sqlite')
engine = create_engine(
    f'sqlite:///{db_path}', echo=True)

class HarmonogramHospitacji(Base):
    __tablename__ = 'Harmonogram_hospitacji'

    ID = Column(Integer, primary_key=True)
    Data_opracowania = Column(Date)


class Kur(Base):
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

    ID = Column(Integer, primary_key=True)
    Tresc = Column(Integer, nullable=False)


class Zajecia(Base):
    __tablename__ = 'Zajecia'

    ID = Column(Integer, primary_key=True)


class GrupaZajeciowa(Base):
    __tablename__ = 'Grupa_zajeciowa'

    ID = Column(String(255), primary_key=True)
    ZajeciaID = Column(ForeignKey('Zajecia.ID'), nullable=False, index=True)
    Forma = Column(Integer, nullable=False)
    Dzien_tygodnia = Column(Integer, nullable=False)
    Budynek = Column(String(25), nullable=False)
    Sala = Column(String(25), nullable=False)
    Godzina = Column(TIME(fsp=6), nullable=False)
    KursID = Column(ForeignKey('Kurs.ID'), nullable=False, index=True)

    Kur = relationship('Kur')
    Zajecia = relationship('Zajecia')


class KomisjaHospitujaca(Base):
    __tablename__ = 'Komisja_hospitujaca'

    ID = Column(String(25), primary_key=True)
    Nauczyciel_akademickiID = Column(ForeignKey(
        'Nauczyciel_akademicki.ID'), nullable=False, index=True)

    Nauczyciel_akademicki = relationship('NauczycielAkademicki')
    Nauczyciel_akademicki1 = relationship(
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
    Komisja_hospitującaID = Column(ForeignKey(
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

    Komisja_hospitujaca = relationship('KomisjaHospitujaca')


class Odpowiedz(Base):
    __tablename__ = 'Odpowiedz'

    ID = Column(Integer, primary_key=True)
    PytanieID = Column(ForeignKey('Pytanie.ID'), nullable=False, index=True)
    Tresc = Column(String(100))
    ProtokolID = Column(ForeignKey('Protokol.ID'), nullable=False, index=True)

    Protokol = relationship('Protokol')
    Pytanie = relationship('Pytanie')


def cleanUpDB() -> None:
    with contextlib.closing(engine.connect()) as con:
        trans = con.begin()
        for table in reversed(metadata.sorted_tables):
            con.execute(table.delete())
        trans.commit()

if not database_exists(engine.url):
    create_database(engine.url)
    metadata.create_all(engine)
