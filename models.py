
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150))
    cpf = db.Column(db.String(11), unique=True)
    email = db.Column(db.String(150))
    senha_hash = db.Column(db.String(200))
    nascimento = db.Column(db.String(10))
    estado = db.Column(db.String(100))
    area_estudo = db.Column(db.String(200))
    curso_preparatorio = db.Column(db.String(200))
    is_admin = db.Column(db.Boolean, default=False)

class Law(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200))
    articles = db.relationship('Article', backref='law', lazy=True)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(50))
    text = db.Column(db.Text)
    law_id = db.Column(db.Integer, db.ForeignKey('law.id'), nullable=False)
    questions = db.relationship('Question', backref='article', lazy=True)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    enunciado = db.Column(db.Text)
    resposta = db.Column(db.String(200))
    tipo = db.Column(db.String(50))
    dificuldade = db.Column(db.String(50))
    law_id = db.Column(db.Integer, db.ForeignKey('law.id'))
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    correta = db.Column(db.Boolean)
    timestamp = db.Column(db.DateTime)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    text = db.Column(db.Text)
    timestamp = db.Column(db.DateTime)

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
