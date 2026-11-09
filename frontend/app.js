function getUrl() {
    return document.getElementById('apiUrl').value;
}

async function cargarProductos() {
    const res = await fetch(`${getUrl()}/productos`);
    const data = await res.json();
    const ul = document.getElementById('listaProductos');
    ul.innerHTML = data.map(p => `<li>[#${p.id}] ${p.nombre} - $${p.precio} (Stock: ${p.stock})</li>`).join('');
}

async function crearProducto(e) {
    e.preventDefault();
    const body = {
        nombre: document.getElementById('pNombre').value,
        precio: parseFloat(document.getElementById('pPrecio').value),
        stock: parseInt(document.getElementById('pStock').value),
        tipo: document.getElementById('pTipo').value
    };
    const res = await fetch(`${getUrl()}/productos`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
    });
    if (res.ok) { alert('Producto creado!'); cargarProductos(); }
    else { alert('Error al crear el producto'); }
}

async function cargarUsuarios() {
    const res = await fetch(`${getUrl()}/usuarios`);
    const data = await res.json();
    const ul = document.getElementById('listaUsuarios');
    ul.innerHTML = data.map(u => `<li>[#${u.id}] ${u.nombre} (${u.email})</li>`).join('');
}

async function crearPedido(e) {
    e.preventDefault();
    const body = {
        cliente_id: parseInt(document.getElementById('pedCliente').value),
        items: [{
            producto_id: parseInt(document.getElementById('pedProd').value),
            cantidad: parseInt(document.getElementById('pedCant').value)
        }]
    };
    const res = await fetch(`${getUrl()}/pedidos`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
    });
    const data = await res.json();
    if (res.ok) { alert(`Pedido realizado! Total: $${data.total}`); cargarProductos(); }
    else { alert(`Error: ${data.detail}`); }
}

async function cargarPedidos() {
    const cid = document.getElementById('buscarCliente').value;
    if (!cid) return;
    const res = await fetch(`${getUrl()}/usuarios/${cid}/pedidos`);
    const data = await res.json();
    const ul = document.getElementById('listaPedidos');
    if (res.ok) {
        ul.innerHTML = data.map(p => `<li>Pedido #${p.id} - Total: $${p.total}</li>`).join('');
    } else {
        ul.innerHTML = `<li>Error: ${data.detail}</li>`;
    }
}