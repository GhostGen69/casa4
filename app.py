import os
from flask import Flask, render_template, request, redirect, url_for
from supabase import create_client, Client
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Cria a aplicação Flask
app = Flask(__name__)

# --- CONFIGURAÇÃO DO SUPABASE ---
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# --- ROTAS DA APLICAÇÃO ---

# Rota para a página de Início (pode ser a principal do site)
@app.route('/')
@app.route('/inicio')
def pagina_inicial():
    # A função render_template procura por arquivos na pasta 'templates'
    return render_template('inicio.html')

# Rota para a tela de Login
@app.route('/login')
def pagina_login():
    return render_template('login.html')

# Rota para a página de Inventário
@app.route('/inventario')
def pagina_inventario():
    # Exemplo de como buscar dados da tabela 'produtos'
    # Ordenar por nome para uma exibição consistente
    response = supabase.table('produtos').select("*").order('nome', desc=False).execute()
    # Os dados estarão em response.data
    produtos = response.data
    return render_template('inventario.html', produtos=produtos)

# Rota para adicionar um novo produto (via formulário)
@app.route('/adicionar_produto', methods=['POST'])
def adicionar_produto():
    # Pega os dados do formulário que foram enviados via POST
    nome = request.form.get('nome')
    quantidade = request.form.get('quantidade')
    preco = request.form.get('preco')

    # Insere os dados na tabela 'produtos' do Supabase
    if nome and quantidade and preco:
        supabase.table('produtos').insert({
            'nome': nome,
            'quantidade': int(quantidade),
            'preco': float(preco)
        }).execute()

    # Redireciona o usuário de volta para a página de inventário
    return redirect(url_for('pagina_inventario'))

# Rota para a página do Caixa
@app.route('/caixa')
def pagina_caixa():
    return render_template('caixa.html')


# --- EXECUÇÃO DO APP ---

# Permite que você execute o arquivo diretamente
if __name__ == '__main__':
    app.run(debug=True)