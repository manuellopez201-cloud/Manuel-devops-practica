from typing import List
from pydantic import BaseModel
from schemas.producto_schema import ProductoRead
from schemas.usuario_schema import UsuarioRead


class PedidoItemCreate(BaseModel):
    producto_id: str  # Cambiado de int a str
    cantidad: int


class PedidoItemRead(BaseModel):
    producto: ProductoRead
    cantidad: int
    subtotal: float

    class Config:
        from_attributes = True


class PedidoCreate(BaseModel):
    cliente_id: str  # Cambiado de int a str
    items: List[PedidoItemCreate]


class PedidoRead(BaseModel):
    id: str  # Cambiado de int a str
    fecha: str
    cliente: UsuarioRead
    total: float
    items: List[PedidoItemRead]

    class Config:
        from_attributes = True