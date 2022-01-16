from datetime import datetime
import unittest
from Domain.Business_objects.Protocol import Protocol
from Domain.Business_objects.ProtocolStatus import ProtocolStatus
from Domain.Mediators.ProtocolMediator import ProtocolMediator
from Foundation.DB_adapter import db


class ProtocolMediatorTests(unittest.TestCase):
    def test_create_protocol(self):
        mediator = ProtocolMediator()
        db.cleanUpDB()
        protocol = Protocol("123", True, ProtocolStatus.WYSTAWIONY, datetime.fromisoformat(
            "2019-02-12"), datetime.fromisoformat("2020-03-12"), None, None, "321")

        mediator.createNewProtocol(protocol)

        created = mediator.getAllProtocols()
        self.assertEqual(1, len(created))


if __name__ == '__main__':
    unittest.main()
