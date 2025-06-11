# config.py

DB_SERVER = '67.217.245.127,1433'
DB_DATABASE = 'Paycheck'
DB_USERNAME = 'sa'
DB_PASSWORD = 'ABC1238f27$'

API_HOSTING = 'localhost'
API_PORT = 8000

def obtener_cadena_conexion():
    return (
        f"DRIVER={{SQL Server}};"
        f"SERVER={DB_SERVER};"
        f"DATABASE={DB_DATABASE};"
        f"UID={DB_USERNAME};"
        f"PWD={DB_PASSWORD};"
        f"Encrypt=no;"
        f"TrustServerCertificate=yes;"
    )
