import os
import openai
from models import db, Law, Article, Question

openai.api_key = os.environ.get('OPENAI_API_KEY')

def generate_and_import_questions(law_text, count=10):
    return
