# Ricardo F Carmo RU - 369001

# Importa os módulos necessários do Flask
from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps  # Para criar o decorador

# Criação da aplicação Flask
app = Flask(__name__)
app.secret_key = 'vida_plus_segura'  # Chave secreta para manter sessões seguras

# Dicionário de usuários para login (usuário: senha)
usuarios = {'admin': 'senha123'}

# Listas para armazenar os pacientes e as consultas em memória
pacientes = []
consultas = []
contador_id = 1  # ID sequencial para cada novo paciente

# Decorador para verificar se o usuário está logado
def login_requerido(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Rota de login
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':  # Se o formulário for enviado
        usuario = request.form['usuario']
        senha = request.form['senha']
        # Verifica se as credenciais são válidas
        if usuario in usuarios and usuarios[usuario] == senha:
            session['usuario'] = usuario  # Inicia a sessão do usuário    
            flash('Acesso autorizado com sucesso!')
            return redirect(url_for('dashboard'))  # Redireciona para o painel              
        else:
            # Se falhar, exibe a página de login com mensagem de erro   
            flash('Usuário ou senha incorretos')
    return render_template('login.html')  # Exibe a tela de login inicialmente

# Rota da tela principal (dashboard)
@app.route('/dashboard')
@login_requerido
def dashboard():
    return render_template('dashboard.html')

# Rota de cadastro de paciente
@app.route('/cadastrar', methods=['GET', 'POST'])
@login_requerido
def cadastrar():
    global contador_id
    mensagem = ''
    if request.method == 'POST':  # Quando o formulário é enviado
        # Coleta os dados do formulário
        nome = request.form['nome']
        cpf = request.form['cpf']
        data_nascimento = request.form['data_nascimento']
        email = request.form['email']
        # Cria um dicionário com os dados do paciente
        paciente = {
            'id': contador_id,
            'nome': nome,
            'cpf': cpf,
            'data_nascimento': data_nascimento,
            'email': email
        }
        pacientes.append(paciente)  # Adiciona à lista de pacientes
        contador_id += 1  # Incrementa o ID para o próximo paciente
        flash('Cadastro realizado com sucesso!')
    return render_template('cadastrar.html', mensagem=mensagem)

# Rota para editar os dados de um paciente
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_requerido
def editar(id):
    # Procura o paciente pelo ID
    paciente = next((p for p in pacientes if p['id'] == id), None)
    if not paciente:
        return 'Paciente não encontrado', 404
    if request.method == 'POST':
        # Atualiza os dados do paciente com os dados do formulário
        paciente['nome'] = request.form['nome']
        paciente['cpf'] = request.form['cpf']
        paciente['data_nascimento'] = request.form['data_nascimento']
        paciente['email'] = request.form['email']
        return redirect(url_for('editar_excluir'))
    return render_template('editar.html', paciente=paciente)

# Rota para excluir um paciente
@app.route('/excluir/<int:id>')
@login_requerido
def excluir(id):
    global pacientes
    # Remove o paciente da lista pelo ID
    pacientes = [p for p in pacientes if p['id'] != id]
    flash('Dados do Paciente excluido com sucesso')
    return redirect(url_for('editar_excluir'))

# Rota para listar os pacientes com botões de editar/excluir
@app.route('/editar_excluir')
@login_requerido
def editar_excluir():
    return render_template('editar_excluir.html', pacientes=pacientes)

# Rota para listar todos os pacientes
@app.route('/listar')
@login_requerido
def listar():
    return render_template('listar.html', pacientes=pacientes)

# Rota para agendar uma nova consulta
@app.route('/agendar', methods=['GET', 'POST'])
@login_requerido
def agendar():
    mensagem = ''
    if request.method == 'POST':
        paciente_id = int(request.form['paciente_id'])
        data = request.form['data']
        hora = request.form['hora']
        # Busca o paciente pelo ID
        paciente = next((p for p in pacientes if p['id'] == paciente_id), None)
        if paciente:
            # Cria o registro da consulta e adiciona à lista
            consulta = {
                'id': len(consultas) + 1,
                'paciente': paciente,
                'data': data,
                'hora': hora
            }
            consultas.append(consulta)
            flash('Consulta agendada com sucesso!')
    return render_template('agendar.html', pacientes=pacientes, mensagem=mensagem)

# Rota para visualizar todas as consultas agendadas
@app.route('/consultas')
@login_requerido
def consultas_agendadas():
    return render_template('consultas.html', consultas=consultas)

# Rota para logout (encerra a sessão do usuário)
@app.route('/logout')
def logout():
    session.pop('usuario', None)  # Remove o usuário da sessão
    return redirect(url_for('login'))  # Redireciona para a tela de login

# Inicia a aplicação em modo debug
if __name__ == '__main__':
    app.run(debug=True)
