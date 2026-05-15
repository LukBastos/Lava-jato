from flask import Blueprint, request, jsonify
from banco import get_db

clientes_bp = Blueprint('clientes', __name__)

@clientes_bp.route('/clientes', methods=['GET'])
def listar():
    db = get_db()
    clientes = db.execute('SELECT * FROM clientes ORDER BY nome').fetchall()
    return jsonify([dict(c) for c in clientes])

@clientes_bp.route('/clientes', methods=['POST'])
def cadastrar():
    data = request.json
    if not data.get('nome') or not data.get('telefone'):
        return jsonify({'erro': 'Nome e telefone são obrigatórios'}), 400
    try:
        db = get_db()
        cur = db.execute(
            'INSERT INTO clientes (nome, telefone) VALUES (?, ?)',
            (data['nome'], data['telefone'])
        )
        db.commit()
        return jsonify({'mensagem': 'Cliente cadastrado!', 'id': cur.lastrowid}), 201
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@clientes_bp.route('/clientes/<int:id>', methods=['DELETE'])
def deletar(id):
    db = get_db()
    db.execute('DELETE FROM clientes WHERE id = ?', (id,))
    db.commit()
    return jsonify({'mensagem': 'Cliente removido!'})
