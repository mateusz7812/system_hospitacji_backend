
from Domain.Mediators.TestMediator import TestMediator


class TestService():
    def __init__(self, testMediator: TestMediator) -> None:
        self.testMediator = testMediator

    def clearDb(self):
        self.testMediator.clearDb()
