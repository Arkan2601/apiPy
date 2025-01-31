# productos.py
from fastapi import APIRouter, HTTPException
import pyodbc
from config import obtener_cadena_conexion

router = APIRouter()

# Función para conectar a la base de datos
def conectar_bd():
    try:
        connectionString = obtener_cadena_conexion()
        conn = pyodbc.connect(connectionString)
        return conn
    except Exception as e:
        print(f" Error al conectar a la base de datos: {e}")
        raise HTTPException(status_code=500, detail="Error al conectar a la base de datos")


# Ruta para insertar un producto
@router.post("/productos/")
def insertar_producto(nombre: str, precio: float):
    conexion = conectar_bd()
    cursor = conexion.cursor()

    try:
        cursor.execute("EXEC Sp_InsertProducto ?, ?", (nombre, precio))
        conexion.commit()
        return {"mensaje": "Producto insertado correctamente"}
    except Exception as e:
        print(f" Error al insertar producto: {e}")
        raise HTTPException(status_code=500, detail=f"Error al insertar producto: {str(e)}")
    finally:
        conexion.close()

# Ruta para obtener todos los productos
@router.get("/productos/")
def obtener_productos():
    conexion = conectar_bd()
    cursor = conexion.cursor()

    try:
        cursor.execute("EXEC Sp_GetProductos")
        productos = cursor.fetchall()
        return [{"Id": p.Id, "Nombre": p.Nombre, "Precio": p.Precio, "Estatus": p.Estatus} for p in productos]
    except Exception as e:
        print(f" Error al obtener productos: {e}")
        raise HTTPException(status_code=500, detail=f"Error al obtener productos: {str(e)}")
    finally:
        conexion.close()

# Ruta para actualizar un producto
@router.put("/productos/{producto_id}")
def actualizar_producto(producto_id: int, nombre: str, precio: float):
    conexion = conectar_bd()
    cursor = conexion.cursor()

    try:
        cursor.execute("EXEC Sp_UpdateProducto ?, ?, ?", (producto_id, nombre, precio))
        conexion.commit()
        return {"mensaje": "Producto actualizado correctamente"}
    except Exception as e:
        print(f" Error al actualizar producto: {e}")
        raise HTTPException(status_code=500, detail=f"Error al actualizar producto: {str(e)}")
    finally:
        conexion.close()

# Ruta para eliminar un producto
@router.delete("/productos/{producto_id}")
def eliminar_producto(producto_id: int):
    conexion = conectar_bd()
    cursor = conexion.cursor()

    try:
        cursor.execute("EXEC Sp_DeleteProducto ?", (producto_id,))
        conexion.commit()
        return {"mensaje": "Producto eliminado correctamente"}
    except Exception as e:
        print(f" Error al eliminar producto: {e}")
        raise HTTPException(status_code=500, detail=f"Error al eliminar producto: {str(e)}")
    finally:
        conexion.close()
