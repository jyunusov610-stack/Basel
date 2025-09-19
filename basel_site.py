from flask import Flask, render_template, request, redirect, url_for, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from meilisearch import Client
from transformers import pipeline
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this!

# Flask-Login setup (user login)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin):
    id = 1

@login_manager.user_loader
def load_user(user_id):
    return User()

# MeiliSearch setup (search system)
client = Client('http://127.0.0.1:7700')
index = client.index('items')
index.add_documents([
    {'id': 1, 'title': 'Mahsulot 1', 'desc': 'Bu test mahsulot'},
    {'id': 2, 'title': 'Mahsulot 2', 'desc': 'AI integratsiyasi'}
])  # Add your data here

# AI Chatbot (Hugging Face)
chatbot = pipeline('conversational', model='distilbert-base-uncased')

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    dark_mode = session.get('dark_mode', False)
    search_results = []
    ai_response = None
    if request.method == 'POST':
        query = request.form.get('query')
        if query:
            search_results = index.search(query)['hits']
            ai_response = chatbot(query)
    return render_template('index.html', dark_mode=dark_mode, results=search_results, ai=ai_response)

@app.route('/toggle_dark')
def toggle_dark():
    session['dark_mode'] = not session.get('dark_mode', False)
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Simple login (username: user, password: pass)
        if request.form['username'] == 'user' and request.form['password'] == 'pass':
            user = User()
            login_user(user)
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
