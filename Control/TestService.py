
from Domain.Mediators.TestMediator import TestMediator
import os


class TestService():
    def __init__(self, testMediator: TestMediator) -> None:
        self.testMediator = testMediator

    def clearDb(self):
        print("INFO: service is clearing db")
        self.testMediator.clearDb()

    def check_ping(self):
        hostname = "google.com"
        return os.system("ping -c 4 " + hostname)
        
        
