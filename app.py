import os
from flask import Flask, render_template, redirect, url_for, request, flash, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# Safe import of admin_tools
try:
    from admin_tools.importer import generate_and_import_questions
except ImportError:
    def generate_and_import_questions(text, count=10):
        return

from utils.pdf_exporter import export_questions_pdf
from utils.stats import get_stats
from models import db, User, Law, Article, Question, Answer, Comment, Favorite

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_secret')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gabarite.db'
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        nome = request.form['nome']; cpf = request.form['cpf']
        email = request.form['email']; nasc = request.form['nascimento']
        estado = request.form['estado']; area = request.form['area']
        curso = request.form['curso']; senha = request.form['senha']
        if User.query.filter_by(cpf=cpf).first():
            flash('CPF já cadastrado'); return redirect(url_for('signup'))
        user = User(nome=nome, cpf=cpf, email=email, nascimento=nasc,
                    estado=estado, area_estudo=area, curso_preparatorio=curso,
                    senha_hash=generate_password_hash(senha))
        db.session.add(user); db.session.commit()
        flash('Cadastro realizado! Faça login.')
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        cpf = request.form['cpf']; senha = request.form['senha']
        user = User.query.filter_by(cpf=cpf).first()
        if user and check_password_hash(user.senha_hash, senha):
            login_user(user); return redirect(url_for('dashboard'))
        flash('Credenciais inválidas')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    laws = Law.query.all()
    return render_template('dashboard.html', laws=laws)

@app.route('/questions')
@login_required
def questions():
    return render_template('questions.html')

@app.route('/admin', methods=['GET','POST'])
@login_required
def admin_panel():
    if not hasattr(current_user, 'is_admin') or not current_user.is_admin:
        flash('Acesso negado'); return redirect(url_for('dashboard'))
    if request.method == 'POST':
        text = request.form['law_text']; count = int(request.form.get('count', 10))
        generate_and_import_questions(text, count)
        flash('Questões importadas!')
    return render_template('admin.html')

@app.route('/export')
@login_required
def export_pdf():
    return export_questions_pdf(current_user.id)

@app.route('/stats')
@login_required
def stats():
    stats_data = get_stats(current_user.id)
    return render_template('stats.html', stats=stats_data)

if __name__=='__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
