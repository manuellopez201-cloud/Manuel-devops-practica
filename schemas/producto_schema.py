from typing import Optional
from pydantic import BaseModel


class ProductoBase(BaseModel):
    nombre: str
    precio: float
    stock: int


class ProductoCreate(ProductoBase):
    tipo: str  # "electronico" o "ropa"
    meses_garantia: Optional[int] = None
    talla: Optional[str] = None
    color: Optional[str] = None


class ProductoRead(ProductoBase):
    id: str  # Cambiado de int a str para soportar UUIDs
    tipo: str
    meses_garantia: Optional[int] = None
    talla: Optional[str] = None
    color: Optional[str] = None

    class Config:
        from_attributes = True