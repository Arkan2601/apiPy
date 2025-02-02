# roles.py
from fastapi import APIRouter, HTTPException
import pyodbc
from config import obtener_cadena_conexion

router = APIRouter(prefix="/api", tags=["Roles"])

# Función para conectar a la base de datos
def conectar_bd():
    try:
        connectionString = obtener_cadena_conexion()
        conn = pyodbc.connect(connectionString)
        return conn
    except Exception as e:
        print(f" Error al conectar a la base de datos: {e}")
        raise HTTPException(status_code=500, detail="Error al conectar a la base de datos")


# Ruta para insertar un Rol
@router.post("/roles/")
def insertar_rol(rol: str):
    conexion = conectar_bd()
    cursor = conexion.cursor()

    try:
        cursor.execute("EXEC Sp_InsertRol ?", (rol))
        conexion.commit()
        return {"mensaje": "Rol insertado correctamente"}
    except Exception as e:
        print(f" Error al insertar Rol: {e}")
        raise HTTPException(status_code=500, detail=f"Error al insertar Rol: {str(e)}")
    finally:
        conexion.close()

# Ruta para obtener todos los roles
@router.get("/roles/")
def obtener_roles():
    conexion = conectar_bd()
    cursor = conexion.cursor()

    try:
        cursor.execute("EXEC Sp_GetRoles")
        roles = cursor.fetchall()
        return [{"Id": p.Id, "Rol": p.Rol, "FechaRegistra": p.FechaRegistra, "FechaActualiza":p.FechaActualiza, "Estatus": p.Estatus} for p in roles]
    except Exception as e:
        print(f" Error al obtener roles: {e}")
        raise HTTPException(status_code=500, detail=f"Error al obtener roles: {str(e)}")
    finally:
        conexion.close()

# Ruta para actualizar un Rol
@router.put("/roles/{id}/")
def actualizar_Rol(id: int, rol: str):
    conexion = conectar_bd()
    cursor = conexion.cursor()

    try:
        cursor.execute("EXEC Sp_UpdateRol ?, ?", (id, rol))
        conexion.commit()
        return {"mensaje": "Rol actualizado correctamente"}
    except Exception as e:
        print(f" Error al actualizar Rol: {e}")
        raise HTTPException(status_code=500, detail=f"Error al actualizar Rol: {str(e)}")
    finally:
        conexion.close()

# Ruta para eliminar un Rol
@router.delete("/roles/{id}/")
def eliminar_Rol(id: int):
    conexion = conectar_bd()
    cursor = conexion.cursor()

    try:
        cursor.execute("EXEC Sp_DeleteRol ?", (id,))
        conexion.commit()
        return {"mensaje": "Rol eliminado correctamente"}
    except Exception as e:
        print(f" Error al eliminar Rol: {e}")
        raise HTTPException(status_code=500, detail=f"Error al eliminar Rol: {str(e)}")
    finally:
        conexion.close()
