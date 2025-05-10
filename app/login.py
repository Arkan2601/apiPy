from fastapi import APIRouter, HTTPException
import pyodbc
import jwt
import datetime
from config import obtener_cadena_conexion
from pydantic import BaseModel
import hashlib
router = APIRouter(prefix="/api", tags=["Auth"])

SECRET_KEY = "jaiba"

def conectar_bd():
    try:
        connectionString = obtener_cadena_conexion()
        conn = pyodbc.connect(connectionString)
        return conn
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")
        raise HTTPException(status_code=500, detail="Error al conectar a la base de datos")

class LoginRequest(BaseModel):
    usuario: str
    contrasena: str

class UsuarioModel(BaseModel):
    Id: int
    NombreUsuario: str
    NombrePersona: str
    IdSucursal: int = 0
    NombreSucursal: str = None
    IdPerfil: int = 0
    theme: str = "default"
    PctDescuento: int = 0
    Rol: str = None
    IdRol: int

def generate_token(usuario: UsuarioModel) -> str:
    payload = {
        "email": usuario.NombreUsuario,
        "sid": usuario.Id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

@router.post("/login")
def login(request: LoginRequest):
    conexion = conectar_bd()
    cursor = conexion.cursor()

    try:
        cursor.execute("EXEC sp_Login ?, ?", (request.usuario, request.contrasena))
        row = cursor.fetchone()
        
        if not row:
            raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")


        stored_hashed_password = row.Contrasena.strip()  # Contraseña almacenada como hash

        # Verificar la contraseña usando bcrypt
        if not bcrypt.checkpw(request.contrasena.encode(), stored_hashed_password.encode()):
            raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")

        usuario = UsuarioModel(
            Id=row.Id,
            NombreUsuario=row.NombreUsuario,
            NombrePersona=row.NombrePersona,
            IdRol=row.IdRol,
            theme=row.theme if hasattr(row, 'theme') else "default"
        )
        
        token = generate_token(usuario)

        return {
            "StatusCode": 200,
            "Success": True,
            "Error": False,
            "Message": "Bienvenido",
            "Response": {
                "data": {
                    "Status": True,
                    "Mensaje": "Bienvenido",
                    "Token": token,
                    "Usuario": usuario.dict()
                }
            }
        }
    except Exception as e:
        print(f"Error en el login: {e}")
        raise HTTPException(status_code=500, detail=f"Error en el login: {str(e)}")
    finally:
        cursor.close()
        conexion.close()
