from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    produtos = []
    produto = ['Ravok Aro 29','27 Marchas','produto1']
    produtos.append(produto)
    produto = ['Bike Aro 26','27 Marchas','produto2']
    produtos.append(produto)
    produto = ['Bike Aro 16','Com rodinhas','produto3']
    produtos.append(produto)
    print(produtos)
    return render_template('index.html', produtos=produtos)

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

@app.route('/contato')
def contato():
    return render_template('contato.html')

if __name__ == '__main__':
    app.run(debug=True)
