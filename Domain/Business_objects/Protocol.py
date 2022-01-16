


from datetime import datetime
from Domain.Business_objects.ProtocolStatus import ProtocolStatus


class Protocol:
    def __init__(self, id: str, zapoznano_sie_z_karta_przedmiotu: bool, status: ProtocolStatus, data_utworzenia: datetime, data_wystawienia: datetime, data_podpisu: datetime, data_odwołania: datetime, komisja_hospitujaca_id: str):
        self.id = id
        self.zapoznano_sie_z_karta_przedmiotu = zapoznano_sie_z_karta_przedmiotu
        self.status = status
        self.data_utworzenia = data_utworzenia
        self.data_wystawienia = data_wystawienia
        self.data_podpisu = data_podpisu
        self.data_odwołania = data_odwołania
        self.komisja_hospitujaca_id = komisja_hospitujaca_id
