
from Foundation.DB_adapter import db

class TestMediator:
    def clearDb(self):
        db.cleanUpDB()
        db.initialize_db()
