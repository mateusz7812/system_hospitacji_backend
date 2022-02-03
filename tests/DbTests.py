import unittest
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from ..Foundation.DB_adapter.consts import DB_ADDRESS
from sqlalchemy.exc import SQLAlchemyError


class DbTests(unittest.TestCase):
    def test_connection(self):
        engine = sqlalchemy.create_engine(DB_ADDRESS)
        try:
            con = engine.connect()
            print(con.execute('SELECT 1;').__dict__)
            con.close()
        except SQLAlchemyError as err:
            self.fail(err)


if __name__ == '__main__':
    unittest.main()
