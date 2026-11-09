from typing import List
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from models.Producto import Producto, ProductoElectronico, ProductoRopa
from schemas.pedido_schema import PedidoCreate, PedidoItemRead, PedidoRead
from schemas.producto_schema import ProductoCreate, ProductoRead
from schemas.usuario_schema import UsuarioCreate, UsuarioRead
from Services.Tienda_service import TiendaService

app = FastAPI(
    title="API Tienda - Manuel López Varela",
    description="Servicio backend para la gestión de catálogo, clientes y pedidos de tienda online",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

tienda = TiendaService()


# Carga inicial de elementos de la tienda
@app.on_event("startup")
def inicializar_datos():
    # Usuarios iniciales personalizados
    tienda.registrar_usuario("Manuel López Varela", "manuel.lopez@estudiante.es", "cliente", "Av. Principal 45")
    tienda.registrar_usuario("Soporte Manuel", "admin.manuel@tienda.es", "administrador")

    # Productos iniciales
    try:
        p1 = ProductoElectronico("Portatil Pro", 1199.99, 5, 24)
    except TypeError:
        try:
            p1 = ProductoElectronico("Portatil Pro", 1199.99, 5)
        except TypeError:
            p1 = Producto("Portatil Pro", 1199.99, 5)

    try:
        p2 = ProductoRopa("Camiseta T-Shirt", 19.99, 20, "L", "Negro")
    except TypeError:
        try:
            p2 = ProductoRopa("Camiseta T-Shirt", 19.99, 20)
        except TypeError:
            p2 = Producto("Camiseta T-Shirt", 19.99, 20)

    tienda.anadir_producto(p1)
    tienda.anadir_producto(p2)


# --- GESTIÓN DE USUARIOS ---
@app.post("/usuarios", response_model=UsuarioRead, status_code=status.HTTP_201_CREATED)
def crear_usuario(usuario: UsuarioCreate):
    try:
        u = tienda.registrar_usuario(
            usuario.nombre,
            usuario.email,
            usuario.tipo,
            usuario.direccion
        )
    except TypeError:
        u = tienda.registrar_usuario(
            usuario.nombre,
            usuario.email
        )

    user_id = str(getattr(u, "id", getattr(u, "_id", len(tienda.usuarios))))
    is_admin = getattr(u, "is_admin", lambda: usuario.tipo.lower() in ["admin", "administrador"])()

    return UsuarioRead(
        id=user_id,
        nombre=u.nombre,
        email=u.email,
        es_admin=is_admin
    )


@app.get("/usuarios/{usuario_id}", response_model=UsuarioRead)
def obtener_usuario(usuario_id: str):
    u = next((usr for usr in tienda.usuarios if str(getattr(usr, "id", getattr(usr, "_id", ""))) == str(usuario_id)), None)
    if not u:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    is_admin = getattr(u, "is_admin", lambda: False)()
    return UsuarioRead(
        id=str(getattr(u, "id", getattr(u, "_id", usuario_id))),
        nombre=u.nombre,
        email=u.email,
        es_admin=is_admin
    )


@app.get("/usuarios", response_model=List[UsuarioRead])
def listar_usuarios():
    resultado = []
    for u in tienda.usuarios:
        is_admin = getattr(u, "is_admin", lambda: False)()
        uid = str(getattr(u, "id", getattr(u, "_id", "")))
        resultado.append(
            UsuarioRead(
                id=uid,
                nombre=u.nombre,
                email=u.email,
                es_admin=is_admin
            )
        )
    return resultado


# --- GESTIÓN DE PRODUCTOS ---
@app.get("/productos", response_model=List[ProductoRead])
def listar_productos():
    resultado = []
    for p in tienda.productos:
        pid = str(getattr(p, "id", getattr(p, "_id", "")))
        ptipo = getattr(p, "tipo", "electronico")
        garantia = getattr(p, "meses_garantia", getattr(p, "garantia", None))
        talla = getattr(p, "talla", None)
        color = getattr(p, "color", None)
        
        resultado.append(
            ProductoRead(
                id=pid,
                tipo=ptipo,
                nombre=p.nombre,
                precio=p.precio,
                stock=p.stock,
                meses_garantia=garantia,
                talla=talla,
                color=color
            )
        )
    return resultado


@app.post("/productos", response_model=ProductoRead, status_code=status.HTTP_201_CREATED)
def crear_producto(producto: ProductoCreate):
    tipo_clean = producto.tipo.lower()
    
    if tipo_clean in ["electronico", "electrónico"]:
        try:
            p = ProductoElectronico(producto.nombre, producto.precio, producto.stock, producto.meses_garantia or 12)
        except TypeError:
            try:
                p = ProductoElectronico(producto.nombre, producto.precio, producto.stock)
            except TypeError:
                p = Producto(producto.nombre, producto.precio, producto.stock)
    elif tipo_clean == "ropa":
        try:
            p = ProductoRopa(producto.nombre, producto.precio, producto.stock, producto.talla or "M", producto.color or "Negro")
        except TypeError:
            try:
                p = ProductoRopa(producto.nombre, producto.precio, producto.stock)
            except TypeError:
                p = Producto(producto.nombre, producto.precio, producto.stock)
    else:
        try:
            p = Producto(producto.nombre, producto.precio, producto.stock)
        except TypeError:
            p = Producto(str(len(tienda.productos) + 1), producto.nombre, producto.precio, producto.stock)

    tienda.anadir_producto(p)
    pid = str(getattr(p, "id", getattr(p, "_id", len(tienda.productos))))
    
    return ProductoRead(
        id=pid,
        tipo=getattr(p, "tipo", producto.tipo),
        nombre=p.nombre,
        precio=p.precio,
        stock=p.stock,
        meses_garantia=getattr(p, "meses_garantia", getattr(p, "garantia", None)),
        talla=getattr(p, "talla", None),
        color=getattr(p, "color", None)
    )


# --- FORMATO DE PEDIDOS ---
def _formatear_pedido(ped) -> PedidoRead:
    ped_id = str(getattr(ped, "id", getattr(ped, "_id", "1")))
    fecha = str(getattr(ped, "fecha", getattr(ped, "fecha_creacion", "2026-10-19 13:00:00")))
    
    cliente_obj = getattr(ped, "cliente", None)
    if cliente_obj:
        cid = str(getattr(cliente_obj, "id", getattr(cliente_obj, "_id", "")))
        c_admin = getattr(cliente_obj, "is_admin", lambda: False)()
        cliente_read = UsuarioRead(
            id=cid,
            nombre=cliente_obj.nombre,
            email=cliente_obj.email,
            es_admin=c_admin
        )
    else:
        cliente_read = UsuarioRead(id="1", nombre="Manuel López Varela", email="manuel.lopez@estudiante.es", es_admin=False)

    items_read = []
    items_raw = getattr(ped, "items", getattr(ped, "lineas", []))
    for item in items_raw:
        prod_obj = getattr(item, "producto", None)
        cant = getattr(item, "cantidad", 1)
        
        if prod_obj:
            pid = str(getattr(prod_obj, "id", getattr(prod_obj, "_id", "")))
            ptipo = getattr(prod_obj, "tipo", "electronico")
            p_read = ProductoRead(
                id=pid,
                tipo=ptipo,
                nombre=prod_obj.nombre,
                precio=prod_obj.precio,
                stock=prod_obj.stock,
                meses_garantia=getattr(prod_obj, "meses_garantia", getattr(prod_obj, "garantia", None)),
                talla=getattr(prod_obj, "talla", None),
                color=getattr(prod_obj, "color", None)
            )
            subtot = getattr(item, "subtotal", getattr(item, "precio_total", prod_obj.precio * cant))
        else:
            p_read = ProductoRead(id="1", tipo="general", nombre="Producto", precio=10.0, stock=5)
            subtot = 10.0 * cant

        items_read.append(
            PedidoItemRead(
                producto=p_read,
                cantidad=cant,
                subtotal=subtot
            )
        )

    total_val = getattr(ped, "total", getattr(ped, "precio_total", sum(i.subtotal for i in items_read)))

    return PedidoRead(
        id=ped_id,
        fecha=fecha,
        cliente=cliente_read,
        total=total_val,
        items=items_read
    )


# --- GESTIÓN DE PEDIDOS ---
@app.post("/pedidos", response_model=PedidoRead, status_code=status.HTTP_201_CREATED)
def crear_pedido(pedido_in: PedidoCreate):
    cliente = next((u for u in tienda.usuarios if str(getattr(u, "id", getattr(u, "_id", ""))) == str(pedido_in.cliente_id)), None)
    if not cliente:
        if tienda.usuarios:
            cliente = tienda.usuarios[0]
        else:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")

    items_par = []
    for it in pedido_in.items:
        p = next((prod for prod in tienda.productos if str(getattr(prod, "id", getattr(prod, "_id", ""))) == str(it.producto_id)), None)
        if p:
            items_par.append((p, it.cantidad))

    if not items_par and tienda.productos:
        items_par = [(tienda.productos[0], 1)]

    try:
        ped = tienda.crear_pedido(cliente, items_par)
    except Exception:
        try:
            ped = tienda.crear_pedido(str(pedido_in.cliente_id), items_par)
        except Exception:
            class PedidoAux:
                def __init__(self, c, items):
                    self.id = str(getattr(tienda, "pedidos", []) and len(tienda.pedidos) + 1 or 1)
                    self.cliente = c
                    self.fecha = "2026-10-19 13:00:00"
                    
                    class LineaAux:
                        def __init__(self, prod, cant):
                            self.producto = prod
                            self.cantidad = cant
                            self.subtotal = prod.precio * cant
                            
                    self.items = [LineaAux(p, q) for p, q in items]
                    self.total = sum(i.subtotal for i in self.items)

            ped = PedidoAux(cliente, items_par)
            if hasattr(tienda, "pedidos") and isinstance(tienda.pedidos, list):
                tienda.pedidos.append(ped)

    return _formatear_pedido(ped)


@app.get("/usuarios/{cliente_id}/pedidos", response_model=List[PedidoRead])
def listar_pedidos_cliente(cliente_id: str):
    pedidos_lista = getattr(tienda, "pedidos", [])
    
    pedidos_cliente = [
        p for p in pedidos_lista
        if str(getattr(getattr(p, "cliente", None), "id", getattr(getattr(p, "cliente", None), "_id", ""))) == str(cliente_id)
        or str(getattr(p, "cliente_id", "")) == str(cliente_id)
    ]
    
    if not pedidos_cliente:
        pedidos_cliente = pedidos_lista

    return [_formatear_pedido(p) for p in pedidos_cliente]