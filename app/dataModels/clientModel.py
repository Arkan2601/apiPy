from pydantic import BaseModel
from typing import Optional

class clientModel(BaseModel):
    Nombre: str
    idProducto: str
    Descripcion: str
    Estatus: str
    Upago: str
    Flimite: str