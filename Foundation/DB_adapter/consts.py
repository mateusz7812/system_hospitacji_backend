
import os 

db_path = os.path.join(os.path.dirname(__file__), 'sqlalchemy.sqlite')
DB_ADDRESS = f'sqlite:///{db_path}'

# DB_ADDRESS = "mysql+pymysql://mateusz7812:mysql123@mateusz7812.mysql.pythonanywhere-services.com:3306/db"
