
from cgi import test
import json
import unittest
from datetime import datetime
import unittest
from unittest.mock import Mock
from Domain.Business_objects.Answer import Answer
from Domain.Business_objects.Protocol import Protocol
from Domain.Business_objects.ProtocolStatus import ProtocolStatus
from Domain.Business_objects.Question import Question
from Domain.Mediators.ProtocolMediator import ProtocolMediator, get_field_name, get_fields_from_question
from Foundation.DB_adapter import db
from unittest.mock import patch


class ProtocolMediatorUnitTests(unittest.TestCase):
    @patch('Domain.Mediators.ProtocolMediator.get_session')
    def test_create_protocol(self, getSessionMock):
        mediator = ProtocolMediator()
        creation_date = "2019-02-12"
        issue_date = "2019-02-12"
        sign_date = "2019-02-12"
        appelation_date = "2019-02-12"
        protocol = Protocol(
            "123",
            True,
            ProtocolStatus.WYSTAWIONY,
            datetime.fromisoformat(creation_date),
            datetime.fromisoformat(issue_date),
            datetime.fromisoformat(sign_date),
            datetime.fromisoformat(appelation_date),
            "321"
        )

        mediator.createNewProtocol(protocol)

        add_mock = getSessionMock.return_value.add
        add_mock.assert_called_once()
        (protocol, ), _ = add_mock.call_args

        p: db.Protokol = protocol

        self.assertEqual(True,          p.Zapoznano_sie_z_karta_przedmiotu)
        self.assertEqual(ProtocolStatus.WYSTAWIONY.value,  
                                        p.Status)
        self.assertEqual(datetime.fromisoformat(creation_date), 
                                        p.Data_utworzenia)
        self.assertEqual(None,          p.Data_wystawienia)
        self.assertEqual(None,          p.Data_podpisu)
        self.assertEqual(None,          p.Data_odwolania)
        self.assertEqual("321",         p.Komisja_hospitujacaID)

    @patch('Domain.Mediators.ProtocolMediator.answer_text_is_valid')
    @patch('Domain.Mediators.ProtocolMediator.get_question_by_id')
    @patch('Domain.Mediators.ProtocolMediator.get_session')
    @patch('Domain.Mediators.ProtocolMediator.get_question_answers_for_protocol')
    def test_create_new_answer_if_not_exists(self, getAnswersMock, getSessionMock, getQuestionMock, checkAnswerMock):
        mediator = ProtocolMediator()
        protocol_id = "123protocol"
        answer_text = {"test": -3}
        pytanie = db.Pytanie()
        pytanie.Tresc = "{test:int}"
        getQuestionMock.return_value = pytanie
        answer = Answer(
            str(json.dumps(answer_text)),
            "testquestion"
        )
        getAnswersMock.return_value = []
        checkAnswerMock.return_value = True

        mediator.saveProtocolAnswer(protocol_id, answer)

        add_mock = getSessionMock.return_value.add
        add_mock.assert_called_once()
        (added_answer, ), _ = add_mock.call_args
        self.assertEqual(json.dumps(answer_text), added_answer.Tresc)

    @patch('Domain.Mediators.ProtocolMediator.answer_text_is_valid')
    @patch('Domain.Mediators.ProtocolMediator.get_question_by_id')
    @patch('Domain.Mediators.ProtocolMediator.get_session')
    @patch('Domain.Mediators.ProtocolMediator.get_question_answers_for_protocol')
    def test_update_answer_if_exists(self, getAnswersMock, getSessionMock, getQuestionMock, checkAnswerMock):
        mediator = ProtocolMediator()
        protocol_id = "123protocol"
        answer_text = {"test": -3}
        pytanie = db.Pytanie()
        pytanie.Tresc = "{test:int}"
        getQuestionMock.return_value = pytanie
        answer = Answer(
            str(json.dumps(answer_text)),
            "testquestion"
        )
        odpowiedz = db.Odpowiedz()
        odpowiedz.Tresc = json.dumps({})
        getAnswersMock.return_value = [odpowiedz]
        checkAnswerMock.return_value = True

        mediator.saveProtocolAnswer(protocol_id, answer)

        add_mock = getSessionMock.return_value.add
        add_mock.assert_not_called()
        self.assertEqual(json.dumps(answer_text), odpowiedz.Tresc)

    @patch('Domain.Mediators.ProtocolMediator.get_question_by_id')
    @patch('Domain.Mediators.ProtocolMediator.get_session')
    @patch('Domain.Mediators.ProtocolMediator.get_question_answers_for_protocol')
    def test_check_answer_before_save_and_found_one_wrong(self, getAnswersMock, getSessionMock, getQuestionMock):
        mediator = ProtocolMediator()
        protocol_id = "123protocol"
        question_id = "testquestion"
        answer = Answer(
            str(json.dumps({"test": -3})),
            question_id
        )
        pytanie = db.Pytanie()
        pytanie.ID = question_id
        pytanie.Tresc = "{test:int:x>0}pytaniepytaniepytanie"
        getQuestionMock.return_value = pytanie

        result = mediator.saveProtocolAnswer(protocol_id, answer)

        self.assertEqual([{"question_id": question_id, "name": "test"}], result)

    @patch('Domain.Mediators.ProtocolMediator.get_question_by_id')
    @patch('Domain.Mediators.ProtocolMediator.get_session')
    @patch('Domain.Mediators.ProtocolMediator.get_question_answers_for_protocol')
    def test_check_answer_before_save(self, getAnswersMock, getSessionMock, getQuestionMock):
        mediator = ProtocolMediator()
        protocol_id = "123protocol"
        question_id = "testquestion"
        answer = Answer(
            str(json.dumps({"test": 3})),
            question_id
        )
        pytanie = db.Pytanie()
        pytanie.ID = question_id
        pytanie.Tresc = "{test:int:x>0}pytaniepytaniepytanie"
        getQuestionMock.return_value = pytanie

        result = mediator.saveProtocolAnswer(protocol_id, answer)

        self.assertEqual(
            [], result)

    def test_get_fields_from_question(self):
        question = "{punktualnie:tak/nie}Czy zajęcia odbyły się punktualnie, opóźnienie {opoznienie:int:x>=9}"
        result = get_fields_from_question(question)
        self.assertEqual(["{punktualnie:tak/nie}", "{opoznienie:int:x>=9}"], result)

    def test_get_field_name(self):
        result = get_field_name("{opoznienie:int:x>9}")
        self.assertEqual("opoznienie", result)


if __name__ == '__main__':
    unittest.main()
