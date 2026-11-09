"""Módulo de capa de servicios para la gestión de la tienda online."""

from typing import Dict, List, Optional
from models.Pedido import Pedido
from models.Producto import Producto
from models.Usuario import Administrador, Cliente, Usuario


class TiendaService:
    """Servicio que gestiona usuarios, productos, inventario y pedidos."""

    def __init__(self) -> None:
        """Inicializa la tienda con listas de productos, usuarios y pedidos."""
        self.productos: List[Producto] = []
        self.usuarios: List[Usuario] = []
        self.pedidos: List[Pedido] = []

    def registrar_usuario(
        self,
        nombre: str,
        email: str,
        tipo: str = "cliente",
        direccion: Optional[str] = None,
    ) -> Usuario:
        """Registra un nuevo usuario (cliente o administrador).

        Args:
            nombre (str): Nombre completo.
            email (str): Correo electrónico.
            tipo (str, optional): 'cliente' o 'administrador'. Defaults to
              "cliente".
            direccion (Optional[str], optional): Dirección postal si es
              cliente. Defaults to None.

        Returns:
            Usuario: Instancia del usuario creado.
        """
        if tipo.lower() == "administrador":
            usuario = Administrador(nombre, email)
        else:
            if not direccion:
                direccion = "Sin dirección"
            usuario = Cliente(nombre, email, direccion)

        self.usuarios.append(usuario)
        return usuario

    def anadir_producto(self, producto: Producto) -> None:
        """Añade un producto al inventario de la tienda.

        Args:
            producto (Producto): Objeto de tipo Producto a agregar.
        """
        self.productos.append(producto)

    def eliminar_producto(self, producto_id: str) -> bool:
        """Elimina un producto a partir de su ID.

        Args:
            producto_id (str): Identificador único del producto.

        Returns:
            bool: True si se eliminó correctamente, False si no se encontró.
        """
        for prod in self.productos:
            if prod.id == producto_id:
                self.productos.remove(prod)
                return True
        return False

    def listar_productos(self) -> List[Producto]:
        """Obtiene la lista de todos los productos del inventario.

        Returns:
            List[Producto]: Lista de productos.
        """
        return self.productos

    def realizar_pedido(
        self, usuario_id: str, productos_solicitados: Dict[str, int]
    ) -> Optional[Pedido]:
        """Realiza un pedido verificando existencia de usuario y stock suficiente.

        Args:
            usuario_id (str): ID del usuario que solicita la compra.
            productos_solicitados (Dict[str, int]): Diccionario con id_producto
              como clave y cantidad como valor.

        Returns:
            Optional[Pedido]: El pedido generado o None si fallan las
            validaciones.
        """
        # Validar usuario
        cliente = next(
            (u for u in self.usuarios if u.id == usuario_id and isinstance(u, Cliente)),
            None,
        )
        if not cliente:
            print(f"Error: Usuario con ID '{usuario_id}' no encontrado o no es un Cliente.")
            return None

        # Validar productos y stock
        items_pedido: Dict[Producto, int] = {}
        for prod_id, cantidad in productos_solicitados.items():
            producto = next((p for p in self.productos if p.id == prod_id), None)
            if not producto:
                print(f"Error: Producto con ID '{prod_id}' no existe.")
                return None
            if not producto.hay_stock(cantidad):
                print(f"Error: Stock insuficiente para '{producto.nombre}'. Requerido: {cantidad}, Disponible: {producto.stock}")
                return None
            items_pedido[producto] = cantidad

        # Descontar el stock de los productos
        for producto, cantidad in items_pedido.items():
            producto.actualizar_stock(-cantidad)

        # Crear y guardar el pedido
        nuevo_pedido = Pedido(cliente, items_pedido)
        self.pedidos.append(nuevo_pedido)
        return nuevo_pedido

    def listar_pedidos_usuario(self, usuario_id: str) -> List[Pedido]:
        """Devuelve los pedidos de un usuario ordenados por fecha.

        Args:
            usuario_id (str): ID del cliente.

        Returns:
            List[Pedido]: Lista de pedidos ordenados cronológicamente.
        """
        pedidos_cliente = [p for p in self.pedidos if p.cliente.id == usuario_id]
        pedidos_cliente.sort(key=lambda p: p.fecha)
        return pedidos_cliente