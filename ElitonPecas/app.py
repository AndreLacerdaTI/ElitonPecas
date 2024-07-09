from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os
from bd_control import *

app = Flask(__name__)
app.secret_key = 'elitonbike'

# Diretorio para imagens de produtos
UPLOAD_FOLDER = './static/produtos/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Configuração do flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Usuário fictício para demonstração
class User(UserMixin):
    def __init__(self, id):
        self.id = id

users = {'eliton': {'password': 'Sollar1509'}}

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route('/')
def index():
    produtos = importar_produtos()
    return render_template('index.html', produtos=produtos)

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

@app.route('/contato')
def contato():
    return render_template('contato.html')

@app.route('/administrador')
def administrador():
    return render_template('login.html')

@app.route('/detalhe_produto', methods=['GET', 'POST'])
def detalhe_produto():
    id = request.form['id']
    print(id)
    produtos = importar_detalhes_produtos()
    for detalhe in produtos:
        print(detalhe[0])
        if detalhe[0]==int(id):
            detalhes = detalhe
            return render_template('index.html', detalhes=detalhes)
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['user']
        password = request.form['passwd']
        if username in users and users[username]['password'] == password:
            user = User(username)
            login_user(user)
            return redirect(url_for('admin'))
        else:
            flash('Login Inválido. Tente novamente.')
    return render_template('login.html')

@app.route('/teste_mensagem',  methods=['GET', 'POST'])
def teste_mensagem():
    flash('alerta')
    flash('Mensagem teste 1')
    flash('Mensagem teste 2')
    return render_template('admin.html')
@app.route('/admin')
@login_required
def admin():
    return render_template('admin.html')

@app.route('/form_admin',  methods=['GET', 'POST'])
def form_admin():
    if request.method == 'POST':
        if 'adicionar' in request.form:
            return render_template('admin.html',adicionar=True)
        elif 'selecionar_editar' in request.form:
            produtos = importar_detalhes_produtos()
            return render_template('admin.html',selecionar_editar=True, produtos=produtos)
        elif 'editar' in request.form:
            id = request.form['id']
            produto = select_produtos(id)
            return render_template('admin.html',editar=True, produto=produto)
        elif 'confirmar' in request.form:
            id = request.form['id']
            titulo = request.form['titulo']
            tamanho = request.form['tamanho']
            return render_template('admin.html', confirmar=True, titulo=titulo, tamanho=tamanho, id=id)
        elif 'excluir' in request.form:
            id = request.form['id']
            retorno = excluir_produto(id)
            flash(retorno)
            if retorno =='erro':
                flash('Não foi possivel excluir o produto!')  
            else:
                flash('Produto excluido do catálogo!')
            return render_template('admin.html')
        elif 'cancelar' in request.form:
            return render_template('admin.html')
@app.route('/alterar_produto',  methods=['GET', 'POST'])
def alterar_produto():
    if request.method == 'POST':
        if 'cancelar' in request.form:
            return render_template('admin.html')
        
    # (titulo, descricao, tamanho, marcha, freio, cor_primaria, cor_secundaria, imagem)
    id_produto = request.form['id']
    titulo = request.form['titulo']
    descricao = request.form['descricao']
    tamanho = request.form['tamanho']
    marcha = request.form['marcha']
    freio = request.form['freio']
    cor_primaria = request.form['cor_primaria']
    cor_secundaria = request.form['cor_secundaria']
    imagem = request.files['imagem']

    if imagem:
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], imagem.filename)
        imagem.save(image_path)
        """with open(image_path, 'rb') as file:
                image_blob = file.read()
        """
        imagem = imagem.filename
        
    else:
        imagem_antiga = request.form['imagem_antiga']
        imagem = imagem_antiga
        print(imagem)
    print(titulo, descricao, tamanho, marcha, freio, cor_primaria, cor_secundaria, imagem)
    retorno = salvar_alteracao(titulo, descricao, tamanho, marcha, freio, cor_primaria, cor_secundaria, imagem, id_produto)
    flash(retorno)
    flash('Produto alterado com sucesso!')
    flash(titulo + ' já está disponível no catálogo.')
    return render_template('admin.html')  


@app.route('/adicionar_produto',  methods=['GET', 'POST'])
def adicionar_produto():
    if request.method == 'POST':
        if 'cancelar' in request.form:
            return render_template('admin.html')
        
    # (titulo, descricao, tamanho, marcha, freio, cor_primaria, cor_secundaria, imagem)

    titulo = request.form['titulo']
    descricao = request.form['descricao']
    tamanho = request.form['tamanho']
    marcha = request.form['marcha']
    freio = request.form['freio']
    cor_primaria = request.form['cor_primaria']
    cor_secundaria = request.form['cor_secundaria']
    imagem = request.files['imagem']

    if imagem:
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], imagem.filename)
        imagem.save(image_path)
        """with open(image_path, 'rb') as file:
                image_blob = file.read()
        """
        imagem = imagem.filename
    print(titulo, descricao, tamanho, marcha, freio, cor_primaria, cor_secundaria, imagem)
    retorno = salvar(titulo, descricao, tamanho, marcha, freio, cor_primaria, cor_secundaria, imagem)
    flash(retorno)
    flash('Produto cadastrado com sucesso!')
    flash(titulo + ' já está disponível no catálogo.')
    return render_template('admin.html')

@app.route('/logout',methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
    #app.run(host='192.168.2.117')
