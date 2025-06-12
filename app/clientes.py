# clientes.py
from fastapi import APIRouter, HTTPException
import pyodbc
from config import obtener_cadena_conexion
from dataModels.clientModel import clientModel

router = APIRouter(prefix="/api", tags=["Clientes"])

# Función para conectar a la base de datos
def conectar_bd():
    try:
        connectionString = obtener_cadena_conexion()
        conn = pyodbc.connect(connectionString)
        return conn
    except Exception as e:
        print(f" Error al conectar a la base de datos: {e}")
        raise HTTPException(status_code=500, detail="Error al conectar a la base de datos")

@router.get("/clientes/", response_model=clientModel)
def obtener_estatus_cliente(key: str):
    conexion = conectar_bd()
    cursor = conexion.cursor()

    try:
        cursor.execute("EXEC Sp_GetClienteStatus ?", (key,))
        cliente = cursor.fetchone()

        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")

        return clientModel(
            Nombre=cliente.nombreCliente,
            idProducto=cliente.idProducto,
            Descripcion=cliente.Descripcion,
            Estatus=cliente.estatus,
            Upago=cliente.ultimoPago,
            Flimite=cliente.fechaLimite
        )

    except Exception as e:
        print(f"{e}")
        raise HTTPException(status_code=500, detail=f"{str(e)}")

    finally:
        conexion.close()

@router.post("/clientes/")
def insertar_cliente(nombreCliente: str, nombreEmpresa: str, idProducto: int, claveLicencia: str, ultimoPago: str, fechaLimite: str):
    conexion = conectar_bd()
    cursor = conexion.cursor()

    try:
        cursor.execute(
            "EXEC SP_InsertarCliente ?, ?, ?, ?, ?, ?",
            (nombreCliente, nombreEmpresa, idProducto, claveLicencia, ultimoPago, fechaLimite)
        )
        
        response = cursor.fetchone()
        conexion.commit()
        if response:
            return {"mensaje": response.msg, "code": response.code}
        else:
            return {"mensaje": "No se recibió respuesta del procedimiento almacenado", "code": 500}
    except Exception as e:
        print(f"{e}")
        raise HTTPException(status_code=500, detail=f"{str(e)}")
    finally:
        conexion.close()

# @router.put("/clientes/{producto_id}/")
# def actualizar_producto(producto_id: int, nombre: str, precio: float):
#     conexion = conectar_bd()
#     cursor = conexion.cursor()

#     try:
#         cursor.execute("EXEC Sp_UpdateProducto ?, ?, ?", (producto_id, nombre, precio))
#         conexion.commit()
#         return {"mensaje": "Producto actualizado correctamente"}
#     except Exception as e:
#         print(f" Error al actualizar producto: {e}")
#         raise HTTPException(status_code=500, detail=f"Error al actualizar producto: {str(e)}")
#     finally:
#         conexion.close()

# @router.delete("/clientes/{producto_id}/")
# def eliminar_producto(producto_id: int):
#     conexion = conectar_bd()
#     cursor = conexion.cursor()

#     try:
#         cursor.execute("EXEC Sp_DeleteProducto ?", (producto_id,))
#         conexion.commit()
#         return {"mensaje": "Producto eliminado correctamente"}
#     except Exception as e:
#         print(f" Error al eliminar producto: {e}")
#         raise HTTPException(status_code=500, detail=f"Error al eliminar producto: {str(e)}")
#     finally:
#         conexion.close()