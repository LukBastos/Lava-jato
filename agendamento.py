from flask import Blueprint, request, jsonify
from banco import get_db

agendamentos_bp = Blueprint('agendamentos', __name__)

@agendamentos_bp.route('/agendamentos', methods=['GET'])
def listar():
    db = get_db()
    agendamentos = db.execute('''
        SELECT a.*, c.nome as cliente_nome, v.placa, v.modelo
        FROM agendamentos a
        JOIN veiculos v ON a.veiculo_id = v.id
        JOIN clientes c ON v.cliente_id = c.id
        ORDER BY a.data_hora DESC
    ''').fetchall()
    return jsonify([dict(a) for a in agendamentos])

@agendamentos_bp.route('/agendamentos', methods=['POST'])
def cadastrar():
    data = request.json
    if not data.get('veiculo_id') or not data.get('servico') or not data.get('data_hora'):
        return jsonify({'erro': 'Veículo, serviço e data são obrigatórios'}), 400
    db = get_db()
    cur = db.execute(
        'INSERT INTO agendamentos (veiculo_id, servico, data_hora, status) VALUES (?, ?, ?, ?)',
        (data['veiculo_id'], data['servico'], data['data_hora'], 'agendado')
    )
    db.commit()
    return jsonify({'mensagem': 'Agendamento criado!', 'id': cur.lastrowid}), 201

@agendamentos_bp.route('/agendamentos/<int:id>', methods=['DELETE'])
def deletar(id):
    db = get_db()
    db.execute('DELETE FROM agendamentos WHERE id = ?', (id,))
    db.commit()
    return jsonify({'mensagem': 'Agendamento removido!'})
