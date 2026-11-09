import requests

BASE_URL = "http://127.0.0.1:8000"


def ejecutar_pruebas():
    # 1. Crear Usuario
    print("=== 1. Registro de Usuario ===")
    u_resp = requests.post(
        f"{BASE_URL}/usuarios",
        json={
            "nombre": "Manuel López Varela",
            "email": "manuel.lopez@estudiante.es",
            "tipo": "cliente",
            "direccion": "Calle Universidad 12",
        },
    )
    print("Status:", u_resp.status_code, "Respuesta:", u_resp.json())
    usuario_id = u_resp.json()["id"]

    # 2. Consultar Usuarios
    print("\n=== 2. Listado de Usuarios ===")
    list_u = requests.get(f"{BASE_URL}/usuarios")
    print("Status:", list_u.status_code, "Usuarios:", list_u.json())

    # 3. Crear Producto
    print("\n=== 3. Registro de Producto ===")
    p_resp = requests.post(
        f"{BASE_URL}/productos",
        json={
            "nombre": "Teclado Mecánico RGB",
            "precio": 89.99,
            "stock": 15,
            "tipo": "electronico",
            "meses_garantia": 24,
        },
    )
    print("Status:", p_resp.status_code, "Respuesta:", p_resp.json())
    producto_id = p_resp.json()["id"]

    # 4. Consultar Productos
    print("\n=== 4. Catálogo de Productos ===")
    list_p = requests.get(f"{BASE_URL}/productos")
    print("Status:", list_p.status_code, "Productos:", list_p.json())

    # 5. Crear Pedido
    print("\n=== 5. Generar Pedido ===")
    ped_resp = requests.post(
        f"{BASE_URL}/pedidos",
        json={
            "cliente_id": usuario_id,
            "items": [{"producto_id": producto_id, "cantidad": 2}],
        },
    )
    print("Status:", ped_resp.status_code, "Respuesta Pedido:", ped_resp.json())

    # 6. Consultar Pedidos del Usuario
    print("\n=== 6. Historial de Pedidos por Cliente ===")
    ped_user = requests.get(f"{BASE_URL}/usuarios/{usuario_id}/pedidos")
    print("Status:", ped_user.status_code, "Pedidos:", ped_user.json())


if __name__ == "__main__":
    ejecutar_pruebas()