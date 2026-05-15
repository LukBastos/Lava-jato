from flask import Blueprint, request, jsonify
from banco import get_db

pagamentos_bp = Blueprint('pagamentos', __name__)

@pagamentos_bp.route('/pagamentos', methods=['GET'])
def listar():
    db = get_db()
    pagamentos = db.execute('''
        SELECT p.*, c.nome as cliente_nome, v.placa, a.servico
        FROM pagamentos p
        JOIN agendamentos a ON p.agendamento_id = a.id
        JOIN veiculos v ON a.veiculo_id = v.id
        JOIN clientes c ON v.cliente_id = c.id
        ORDER BY p.criado_em DESC
    ''').fetchall()
    return jsonify([dict(p) for p in pagamentos])

@pagamentos_bp.route('/pagamentos', methods=['POST'])
def cadastrar():
    data = request.json
    if not data.get('agendamento_id') or not data.get('valor') or not data.get('forma'):
        return jsonify({'erro': 'Agendamento, valor e forma são obrigatórios'}), 400
    db = get_db()
    cur = db.execute(
        'INSERT INTO pagamentos (agendamento_id, valor, forma) VALUES (?, ?, ?)',
        (data['agendamento_id'], data['valor'], data['forma'])
    )
    db.commit()
    return jsonify({'mensagem': 'Pagamento registrado!', 'id': cur.lastrowid}), 201

@pagamentos_bp.route('/pagamentos/<int:id>', methods=['DELETE'])
def deletar(id):
    db = get_db()
    db.execute('DELETE FROM pagamentos WHERE id = ?', (id,))
    db.commit()
    return jsonify({'mensagem': 'Pagamento removido!'})
