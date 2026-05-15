import sqlite3
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'banco.db')

DB_PATH = 'banco.db'

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    db = get_db()
    db.executescript('''
        CREATE TABLE IF NOT EXISTS clientes (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            nome      TEXT NOT NULL,
            telefone  TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS veiculos (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            placa       TEXT NOT NULL UNIQUE,
            modelo      TEXT NOT NULL,
            cliente_id  INTEGER NOT NULL,
            FOREIGN KEY (cliente_id) REFERENCES clientes(id)
        );

        CREATE TABLE IF NOT EXISTS agendamentos (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            veiculo_id  INTEGER NOT NULL,
            servico     TEXT NOT NULL,
            data_hora   TEXT NOT NULL,
            status      TEXT DEFAULT 'agendado',
            FOREIGN KEY (veiculo_id) REFERENCES veiculos(id)
        );

        CREATE TABLE IF NOT EXISTS pagamentos (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            agendamento_id  INTEGER NOT NULL,
            valor           REAL NOT NULL,
            forma           TEXT NOT NULL,
            criado_em       TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (agendamento_id) REFERENCES agendamentos(id)
        );
    ''')
    db.commit()
    db.close()
