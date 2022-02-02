
from Foundation.DB_adapter import db

class TestMediator:
    def clearDb(self):
        print("INFO mediator is cleaning db")
        db.cleanUpDB()
        db.initialize_db()
