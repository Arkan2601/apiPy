import pyodbc

conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=192.168.54.189;"
    "DATABASE=ProyectoIa;"
    "UID=devops;"
    "PWD=Tecnologia.18;"
    "Encrypt=yes;"
    "TrustServerCertificate=yes;"
)

print("Conexión OK")