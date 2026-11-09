"""Módulo que define los tipos de usuarios de la tienda online."""

from uuid import uuid4


class Usuario:
    """Clase base que representa un usuario del sistema."""

    def __init__(self, nombre: str, email: str) -> None:
        """Inicializa un usuario.

        Args:
            nombre (str): Nombre completo del usuario.
            email (str): Correo electrónico.
        """
        self.id: str = str(uuid4())
        self.nombre: str = nombre
        self.email: str = email

    def is_admin(self) -> bool:
        """Indica si el usuario tiene privilegios de administración.

        Returns:
            bool: False por defecto.
        """
        return False

    def __str__(self) -> str:
        """Devuelve representación en texto del usuario.

        Returns:
            str: Información general del usuario.
        """
        return f"[{self.id[:8]}] {self.nombre} ({self.email})"


class Cliente(Usuario):
    """Clase que representa un cliente de la tienda."""

    def __init__(self, nombre: str, email: str, direccion: str) -> None:
        """Inicializa un cliente con su dirección postal.

        Args:
            nombre (str): Nombre completo.
            email (str): Correo electrónico.
            direccion (str): Dirección de entrega.
        """
        super().__init__(nombre, email)
        self.direccion: str = direccion

    def __str__(self) -> str:
        """Devuelve representación en texto del cliente.

        Returns:
            str: Información del cliente y su dirección.
        """
        return f"{super().__str__()} - Dirección: {self.direccion}"


class Administrador(Usuario):
    """Clase que representa a un gestor/administrador de la tienda."""

    def is_admin(self) -> bool:
        """Indica que el usuario es administrador.

        Returns:
            bool: True siempre.
        """
        return True

    def __str__(self) -> str:
        """Devuelve representación en texto del administrador.

        Returns:
            str: Información del administrador.
        """
        return f"{super().__str__()} [ADMINISTRADOR]"