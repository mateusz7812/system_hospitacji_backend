
import os 

#db_path = os.path.join(os.path.dirname(__file__), 'sqlalchemy.sqlite')
#DB_ADDRESS = f'sqlite:///{db_path}'

DB_ADDRESS = "mysql+mysqlconnector://mateusz7812@system-hospitacji-db:6jmM6Z55msqNnmB@system-hospitacji-db.mysql.database.azure.com:3306/db"


#import urllib
#params = urllib.parse.quote_plus(r'Driver={ODBC Driver 13 for SQL Server};Server=tcp:system-hospitacji-db.mysql.database.azure.com,1433;Database=db;Uid=mateusz7812@system-hospitacji-db;Pwd=6jmM6Z55msqNnmB;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
#DB_ADDRESS = 'mssql+pyodbc:///?odbc_connect={}'.format(params)