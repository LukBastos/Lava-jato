from flask import Blueprint, request, jsonify
from banco import get_db

veiculos_bp = Blueprint('veiculos', __name__)

@veiculos_bp.route('/veiculos', methods=['GET'])
def listar():
    db = get_db()
    veiculos = db.execute('''
        SELECT v.*, c.nome as cliente_nome
        FROM veiculos v
        JOIN clientes c ON v.cliente_id = c.id
        ORDER BY v.placa
    ''').fetchall()
    return jsonify([dict(v) for v in veiculos])

@veiculos_bp.route('/veiculos', methods=['POST'])
def cadastrar():
    data = request.json
    if not data.get('placa') or not data.get('modelo') or not data.get('cliente_id'):
        return jsonify({'erro': 'Placa, modelo e cliente são obrigatórios'}), 400
    try:
        db = get_db()
        cur = db.execute(
            'INSERT INTO veiculos (placa, modelo, cliente_id) VALUES (?, ?, ?)',
            (data['placa'].upper(), data['modelo'], data['cliente_id'])
        )
        db.commit()
        return jsonify({'mensagem': 'Veículo cadastrado!', 'id': cur.lastrowid}), 201
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@veiculos_bp.route('/veiculos/<int:id>', methods=['DELETE'])
def deletar(id):
    db = get_db()
    db.execute('DELETE FROM veiculos WHERE id = ?', (id,))
    db.commit()
    return jsonify({'mensagem': 'Veículo removido!'})
