from pydantic import BaseModel
from typing import Optional

class clientModel(BaseModel):
    Nombre: str
    idProducto: int
    Estatus: int
    Upago: str
    Flimite: str