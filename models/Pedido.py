"""Módulo que define la clase Pedido en la tienda online."""

from datetime import datetime
from typing import Dict
from uuid import uuid4

from models.Producto import Producto
from models.Usuario import Cliente


class Pedido:
    """Clase que representa un pedido realizado por un cliente."""

    def __init__(
        self, cliente: Cliente, productos_cantidad: Dict[Producto, int]
    ) -> None:
        """Inicializa una instancia de Pedido y calcula el importe total.

        Args:
            cliente (Cliente): Cliente que realiza el pedido.
            productos_cantidad (Dict[Producto, int]): Diccionario con los
              productos y sus respectivas cantidades.
        """
        self.id: str = str(uuid4())
        self.cliente: Cliente = cliente
        self.fecha: datetime = datetime.now()
        self.productos_cantidad: Dict[Producto, int] = productos_cantidad
        self.total: float = self._calcular_total()

    def _calcular_total(self) -> float:
        """Calcula el coste total de la compra.

        Returns:
            float: Importe total.
        """
        total = 0.0
        for producto, cantidad in self.productos_cantidad.items():
            total += producto.precio * cantidad
        return total

    def __str__(self) -> str:
        """Devuelve un resumen del pedido.

        Returns:
            str: Resumen del pedido con identificador, cliente, fecha y total.
        """
        fecha_str = self.fecha.strftime("%Y-%m-%d %H:%M:%S")
        return (
            f"Pedido [{self.id[:8]}] | Cliente: {self.cliente.nombre} | "
            f"Fecha: {fecha_str} | Total: {self.total:.2f}€"
        )