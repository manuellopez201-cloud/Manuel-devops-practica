"""Módulo que define las clases de productos para la tienda online."""

from uuid import uuid4


class Producto:
    """Clase base que representa un producto general en la tienda."""

    def __init__(self, nombre: str, precio: float, stock: int) -> None:
        """Inicializa una nueva instancia de Producto.

        Args:
            nombre (str): Nombre del producto.
            precio (float): Precio unitario del producto.
            stock (int): Cantidad de unidades disponibles.
        """
        self.id: str = str(uuid4())
        self.nombre: str = nombre
        self.precio: float = precio
        self.stock: int = stock

    def hay_stock(self, cantidad: int) -> bool:
        """Comprueba si hay suficiente stock disponible.

        Args:
            cantidad (int): Cantidad solicitada.

        Returns:
            bool: True si hay suficiente stock, False en caso contrario.
        """
        return self.stock >= cantidad

    def actualizar_stock(self, cantidad: int) -> None:
        """Actualiza el stock disponible sumando o restando unidades.

        Args:
            cantidad (int): Cantidad a modificar (positiva para reposición,
              negativa para ventas).
        """
        self.stock += cantidad

    def __str__(self) -> str:
        """Devuelve una representación legible del producto.

        Returns:
            str: Descripción básica del producto.
        """
        return f"[{self.id[:8]}] {self.nombre} - Precio: {self.precio:.2f}€ - Stock: {self.stock}"


class ProductoElectronico(Producto):
    """Clase que representa un producto electrónico con garantía."""

    def __init__(
        self, nombre: str, precio: float, stock: int, garantia_meses: int
    ) -> None:
        """Inicializa una nueva instancia de ProductoElectronico.

        Args:
            nombre (str): Nombre del producto.
            precio (float): Precio unitario.
            stock (int): Unidades disponibles.
            garantia_meses (int): Meses de garantía ofrecidos.
        """
        super().__init__(nombre, precio, stock)
        self.garantia_meses: int = garantia_meses

    def __str__(self) -> str:
        """Devuelve la representación en texto incluyendo la garantía.

        Returns:
            str: Descripción completa del producto electrónico.
        """
        return f"{super().__str__()} - Garantía: {self.garantia_meses} meses"


class ProductoRopa(Producto):
    """Clase que representa un artículo de ropa con talla y color."""

    def __init__(
        self, nombre: str, precio: float, stock: int, talla: str, color: str
    ) -> None:
        """Inicializa una nueva instancia de ProductoRopa.

        Args:
            nombre (str): Nombre del producto.
            precio (float): Precio unitario.
            stock (int): Unidades disponibles.
            talla (str): Talla de la prenda (p. ej., S, M, L).
            color (str): Color de la prenda.
        """
        super().__init__(nombre, precio, stock)
        self.talla: str = talla
        self.color: str = color

    def __str__(self) -> str:
        """Devuelve la representación en texto incluyendo talla y color.

        Returns:
            str: Descripción completa del artículo de ropa.
        """
        return f"{super().__str__()} - Talla: {self.talla} - Color: {self.color}"