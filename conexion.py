import os
import MySQLdb
from dotenv import load_dotenv
load_dotenv()

conexion = MySQLdb.connect(
  host= os.getenv("DB_HOST"),
  user=os.getenv("DB_USERNAME"),
  passwd= os.getenv("DB_PASSWORD"),
  db= os.getenv("DB_NAME"),
  autocommit = True,
  ssl_mode="VERIFY_IDENTITY",
    ssl= '/etc/ssl/certs/ca-certificates.crt'
  
)