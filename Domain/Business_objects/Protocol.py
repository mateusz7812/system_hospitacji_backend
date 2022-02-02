


from datetime import datetime
from Domain.Business_objects.ProtocolStatus import ProtocolStatus


class Protocol:
    def __init__(self, id: str, zapoznano_sie_z_karta_przedmiotu: bool, status: ProtocolStatus, data_utworzenia: datetime, data_wystawienia: datetime, data_podpisu: datetime, data_odwołania: datetime, komisja_hospitujaca_id: str):
        self.id = id
        self.course_card_read = zapoznano_sie_z_karta_przedmiotu
        self.status = status
        self.creation_date = data_utworzenia
        self.issue_date = data_wystawienia
        self.sign_date = data_podpisu
        self.appelation_date = data_odwołania
        self.hospitalization_commitee_id = komisja_hospitujaca_id
