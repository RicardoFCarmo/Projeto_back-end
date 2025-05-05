from flask import Flask, render_template, request, redirect, url_for, session 

app = Flask(__name__)
app.secret_key = 'vida_plus_segura'

usuarios = {'admin': 'senha123'}

pacientes = []
contador_id = 1

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']
        if usuario in usuarios and usuarios[usuario] == senha:
            session['usuario'] = usuario
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', erro='Usuário ou senha incorretos')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    global contador_id
    mensagem = ''
    if request.method == 'POST':
        nome = request.form['nome']
        cpf = request.form['cpf']
        paciente = {
            'id': contador_id,
            'nome': nome,
            'cpf': cpf
        }
        pacientes.append(paciente)
        contador_id += 1
        mensagem = 'Cadastro realizado com sucesso!'
    return render_template('cadastrar.html', mensagem=mensagem)

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    paciente = next((p for p in pacientes if p['id'] == id), None)
    if not paciente:
        return 'Paciente não encontrado', 404
    if request.method == 'POST':
        paciente['nome'] = request.form['nome']
        paciente['cpf'] = request.form['cpf']
        return redirect(url_for('editar_excluir'))
    return render_template('editar.html', paciente=paciente)

@app.route('/excluir/<int:id>')
def excluir(id):
    global pacientes
    pacientes = [p for p in pacientes if p['id'] != id]
    return redirect(url_for('editar_excluir'))

@app.route('/editar_excluir')
def editar_excluir():
    return render_template('editar_excluir.html', pacientes=pacientes)

@app.route('/listar')
def listar():
    return render_template('listar.html', pacientes=pacientes)

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
