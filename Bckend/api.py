from flask import Flask, jsonify, request
from flask_cors import CORS
from conexion_detalle_compra import ConexionDetalleCompraaa  

app = Flask(__name__)
CORS(app)

@app.route('/api/pedidos/<int:pedido_id>/items', methods=['GET'])
def get_items(pedido_id):
    db = ConexionDetalleCompra()
    items = db.obtener_items_por_pedido(pedido_id)
    db.cerrar()
    return jsonify(items)

@app.route('/api/items', methods=['POST'])
def crear_item():
    payload = request.json
    db = ConexionDetalleCompra()
    item_id = db.insertar_item(
        payload['pedido_id'], payload['producto_id'], payload['nombre_producto'],
        payload.get('descripcion', ''), payload['cantidad_solicitada'], payload['precio_unitario']
    )
    db.cerrar()
    return jsonify({'item_id': item_id}), 201

@app.route('/api/items/<int:item_id>', methods=['PUT'])
def actualizar_item(item_id):
    payload = request.json
    db = ConexionDetalleCompra()
    ok = db.actualizar_item(
        item_id,
        payload.get('cantidad_solicitada'),
        payload.get('precio_unitario'),
        payload.get('nombre_producto'),
        payload.get('descripcion')
    )
    db.cerrar()
    return jsonify({'ok': bool(ok)})

@app.route('/api/items/<int:item_id>', methods=['DELETE'])
def eliminar_item(item_id):
    db = ConexionDetalleCompra()
    ok = db.eliminar_item(item_id)
    db.cerrar()
    return jsonify({'ok': bool(ok)})

@app.route('/api/pedidos/<int:pedido_id>/calcular_total', methods=['GET'])
def calcular_total(pedido_id):
    db = ConexionDetalleCompra()
    total = db.calcular_total_pedido(pedido_id)
    db.cerrar()
    return jsonify({'total': total})

@app.route('/api/pedidos/<int:pedido_id>/recibir', methods=['POST'])
def recibir(pedido_id):
    payload = request.json
    db = ConexionDetalleCompra()
    db.recibir_materiales(pedido_id, payload.get('items', []), payload.get('usuario', 'sistema'))
    db.cerrar()
    return jsonify({'ok': True})


if __name__ == '__main__':
    app.run(debug=True, port=5000)
