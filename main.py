# Importar
from flask import Flask, render_template, request, redirect
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
import os
import time
# Importando a biblioteca de banco de dados
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
# Conectando ao SQLite
# Use an absolute path inside the project so the DB is always created in the app folder
db_path = os.path.join(app.root_path, 'diary.db')
# Add timeout and relax threading checks for SQLite (helps avoid transient 'database is locked')
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}?timeout=30"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'connect_args': {'check_same_thread': False, 'timeout': 30}}
# Criando um Banco de Dados (DB)
db = SQLAlchemy(app)

# Drop 'image' column if it exists (SQLite requires table recreation to drop a column)
def drop_image_column_if_exists():
    try:
        res = db.session.execute(text("PRAGMA table_info(card);"))
        cols = [row[1] if isinstance(row, (tuple, list)) else row['name'] for row in res]
        if 'image' in cols:
            # Create a new table without the image column, copy data, replace
            db.session.execute(text(
                "CREATE TABLE IF NOT EXISTS card_new (id INTEGER PRIMARY KEY, title VARCHAR(100) NOT NULL, subtitle VARCHAR(200) NOT NULL, text TEXT NOT NULL);"
            ))
            db.session.execute(text(
                "INSERT INTO card_new (id, title, subtitle, text) SELECT id, title, subtitle, text FROM card;"
            ))
            db.session.execute(text("DROP TABLE card;"))
            db.session.execute(text("ALTER TABLE card_new RENAME TO card;"))
            db.session.commit()
    except Exception:
        db.session.rollback()


def commit_with_retry(session, retries=5, base_delay=0.1):
    """Commit the session with small retries for transient SQLite locks."""
    for attempt in range(retries):
        try:
            session.commit()
            return
        except OperationalError:
            session.rollback()
            if attempt < retries - 1:
                time.sleep(base_delay * (attempt + 1))
            else:
                raise

# Run the drop migration immediately to remove image column if it exists
with app.app_context():
    drop_image_column_if_exists()



# Tarefa #1. Criar uma tabela no Banco de Dados
class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    subtitle = db.Column(db.String(200), nullable=False)
    text = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Card {self.title}>'

# Ensure DB tables exist
with app.app_context():
    db.create_all()







# Executando a página com conteúdo
@app.route('/')
def index():
    # Exibindo os objetos do Banco de Dados
    # Tarefa #2. Exibir os objetos do Banco de Dados no index.html
    cards = Card.query.all()
    return render_template('index.html', cards=cards) 

# Executando a página com o cartão
@app.route('/card/<int:id>')
def card(id):
    # Tarefa #2. Exibir o cartão correto pelo seu id
    card = Card.query.get_or_404(id)
    return render_template('card.html', card=card)

@app.route('/card/<int:id>/delete', methods=['POST'])
def delete_card(id):
    # Remove the card from the database and redirect to index
    card = Card.query.get_or_404(id)
    db.session.delete(card)
    commit_with_retry(db.session)
    return redirect('/')

# Edit an existing card (GET shows form, POST saves changes)
@app.route('/card/<int:id>/edit', methods=['GET','POST'])
def edit_card(id):
    card = Card.query.get_or_404(id)
    if request.method == 'POST':

        # Normal save
        card.title = request.form['title']
        card.subtitle = request.form['subtitle']
        card.text = request.form['text']
        commit_with_retry(db.session)
        return redirect(f"/card/{card.id}")
    return render_template('edit_card.html', card=card)

# Executando a página e criando o cartão
@app.route('/create')
def create():
    return render_template('create_card.html')

# O formulário do cartão
@app.route('/form_create', methods=['GET','POST'])
def form_create():
    if request.method == 'POST':
        title =  request.form['title']
        subtitle =  request.form['subtitle']
        text =  request.form['text']

        # Tarefa #2. Criar uma forma de armazenar dados no Banco de Dados
        new_card = Card(title=title, subtitle=subtitle, text=text)
        db.session.add(new_card)
        commit_with_retry(db.session)
        




        return redirect('/')
    else:
        return render_template('create_card.html')


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
