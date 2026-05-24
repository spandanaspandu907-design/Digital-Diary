from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# DATABASE MODEL
class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

# HOME PAGE
@app.route('/')
def home():
    return render_template('index.html')

# LOGIN PAGE
@app.route('/login')
def login():
    return render_template('login.html')

# REGISTER PAGE
@app.route('/register')
def register():
    return render_template('register.html')

# DASHBOARD
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():

    if request.method == 'POST':

        diary_text = request.form['content']

        new_entry = Entry(content=diary_text)

        db.session.add(new_entry)

        db.session.commit()

        return redirect('/dashboard')

    entries = Entry.query.order_by(Entry.date.desc()).all()

    return render_template('dashboard.html', entries=entries)

# DELETE ENTRY
@app.route('/delete/<int:id>')
def delete(id):

    entry = Entry.query.get(id)

    db.session.delete(entry)

    db.session.commit()

    return redirect('/dashboard')

# EDIT ENTRY
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):

    entry = Entry.query.get(id)

    if request.method == 'POST':

        entry.content = request.form['content']

        db.session.commit()

        return redirect('/dashboard')

    return render_template('edit.html', entry=entry)

# PROFILE PAGE
@app.route('/profile')
def profile():
    return render_template('profile.html')

# LOGOUT
@app.route('/logout')
def logout():
    return redirect('/')

# RUN APP
if __name__ == '__main__':

    with app.app_context():
        db.create_all()

    app.run(debug=True)