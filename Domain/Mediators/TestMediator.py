from Foundation.DB_adapter import db
from sqlalchemy.sql import text
from sqlalchemy.exc import SQLAlchemyError

class TestMediator:
    def clearDb(self):
        print("INFO mediator is cleaning db")
        db.create_db()
        db.cleanUpDB()
        db.initialize_db()
    
    def test_connection(self):
        try:
            print("trying connect to db")
            db.engine.connect()
            print("success")
            return True
        except SQLAlchemyError as err:
            print("error", err.__cause__) 
            return False
