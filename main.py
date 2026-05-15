from flask import Flask
from flask_cors import CORS
from banco import init_db

from clientes import clientes_bp
from veiculos import veiculos_bp
from agendamento import agendamentos_bp
from pagamento import pagamentos_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(clientes_bp)
app.register_blueprint(veiculos_bp)
app.register_blueprint(agendamentos_bp)
app.register_blueprint(pagamentos_bp)

init_db()
app.run(debug=True, port=5000)
