import sqlite3


def importar_produtos():
    conn = sqlite3.connect('bd.db')
    cur = conn.cursor()
    cur.execute("SELECT id, titulo, descricao, imagem FROM produtos")
    rows = cur.fetchall()
    print(rows)
    return rows

def salvar(titulo, descricao, imagem):
    conn = sqlite3.connect('bd.db')
    with conn:
        sql = '''INSERT INTO produtos (titulo, descricao, imagem)
                    VALUES (?, ?, ?)'''
        cur = conn.cursor()
        cur.execute(sql, (titulo, descricao, imagem))
        conn.commit()
    return True

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
        imagem BLOB
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