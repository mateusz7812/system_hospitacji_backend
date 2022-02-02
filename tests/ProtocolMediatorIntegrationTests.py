from datetime import datetime
import unittest
from Domain.Business_objects.Protocol import Protocol
from Domain.Business_objects.ProtocolStatus import ProtocolStatus
from Domain.Mediators.ProtocolMediator import ProtocolMediator
from Foundation.DB_adapter import db


class ProtocolMediatorIntegrationTests(unittest.TestCase):
    def test_create_protocol(self):
        mediator = ProtocolMediator()
        creation_date = "2019-02-12"
        db.cleanUpDB()
        protocol = Protocol(
            "123", 
            True, 
            ProtocolStatus.WYSTAWIONY, 
            datetime.fromisoformat(creation_date), 
            None, 
            None, 
            None, 
            "321"
        )

        mediator.createNewProtocol(protocol)

        created = mediator.getAllProtocols()
        self.assertEqual(1, len(created))
        
        p = created[0]
        self.assertEqual(True,          p.course_card_read)
        self.assertEqual("Wystawiony",  p.status)
        self.assertEqual(creation_date, p.creation_date)
        self.assertEqual('',            p.issue_date)
        self.assertEqual('',            p.sign_date)
        self.assertEqual('',            p.appelation_date)
        self.assertEqual("321",         p.hospitalization_commitee_id)

    def test_sign_protocol(self):
        mediator = ProtocolMediator()
        db.cleanUpDB()
        db.initialize_db()
        protocols = mediator.getAllProtocols()
        issued_protocols = list(filter(lambda p: p.status == "Wystawiony", protocols))
        self.assertEqual(1, len(issued_protocols))
        protocol = issued_protocols[0]

        mediator.signProtocol(protocol.id)

        protocols = mediator.getAllProtocols()
        signed_protocols = list(filter(lambda p: p.status == "Podpisany" and p.id == protocol.id, protocols))
        self.assertEqual(1, len(signed_protocols))


if __name__ == '__main__':
    unittest.main()
