from typing import Optional
from pydantic import BaseModel


class UsuarioBase(BaseModel):
    nombre: str
    email: str


class UsuarioCreate(UsuarioBase):
    tipo: str = "cliente"
    direccion: Optional[str] = None


class UsuarioRead(UsuarioBase):
    id: str  # Cambiado de int a str para soportar UUIDs
    es_admin: bool

    class Config:
        from_attributes = True