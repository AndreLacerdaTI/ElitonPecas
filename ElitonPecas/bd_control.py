import sqlite3

def importar_detalhes_produtos():
    conn = sqlite3.connect('bd.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM produtos")
    rows = cur.fetchall()
    #print(rows)
    return rows


def importar_produtos():
    conn = sqlite3.connect('bd.db')
    cur = conn.cursor()
    cur.execute("SELECT id, titulo, tamanho, imagem FROM produtos")
    rows = cur.fetchall()
    #print(rows)
    return rows

def select_produtos(id):
    conn = sqlite3.connect('bd.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM produtos WHERE id = %s" % id)
    rows = cur.fetchall()
    #print(rows)
    return rows[0]

def salvar_alteracao(titulo, descricao, tamanho, marcha, freio, cor_primaria, cor_secundaria, imagem, id_produto):
    conn = sqlite3.connect('bd.db')
    with conn:
        sql = '''UPDATE produtos SET titulo = ?, descricao = ?, tamanho = ?, marcha = ?, freio = ?, cor_primaria = ?, cor_secundaria = ?, imagem  = ? WHERE id = ?;'''
        cur = conn.cursor()
        cur.execute(sql, (titulo, descricao, tamanho, marcha, freio, cor_primaria, cor_secundaria, imagem, id_produto))
        try:
            conn.commit()
            return 'sucesso'
        except:
            return 'erro'

def excluir_produto(id):
    conn = sqlite3.connect('bd.db')
    cur = conn.cursor()
    cur.execute(f"DELETE FROM produtos WHERE id = {id}")
    try:
        conn.commit()
        return 'sucesso'
    except:
        return 'erro'

def salvar(titulo, descricao, tamanho, marcha, freio, cor_primaria, cor_secundaria, imagem):
    conn = sqlite3.connect('bd.db')
    with conn:
        sql = '''INSERT INTO produtos (titulo, descricao, tamanho, marcha, freio, cor_primaria, cor_secundaria, imagem)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''
        cur = conn.cursor()
        cur.execute(sql, (titulo, descricao, tamanho, marcha, freio, cor_primaria, cor_secundaria, imagem))
        try:
            conn.commit()
            return 'sucesso'
        except:
            return 'erro'

"""

def create_connection():
    conn = sqlite3.connect('bd.db')
    return conn

def create_table(conn):
    create_table_sql = '''
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        descricao TEXT NOT NULL,
        tamanho INTEGER,
        marcha TEXT,
        freio TEXT,
        cor_primaria TEXT,
        cor_secundaria TEXT,
        imagem TEXT
    );
    '''
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        print(e)

def main():
    conn = create_connection()
    if conn is not None:
        create_table(conn)
        conn.close()
    else:
        print("Error! Cannot create the database connection.")

if __name__ == '__main__':
    main()
"""