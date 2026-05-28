from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = "secret123"

# DATABASE CONFIGURATION
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# USER DATABASE TABLE
class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(100), nullable=False)

    password = db.Column(db.String(100), nullable=False)

# DIARY ENTRY TABLE
class Entry(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    content = db.Column(db.Text, nullable=False)

    date = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id')
    )

# HOME PAGE
@app.route('/')
def home():

    return render_template('index.html')

# REGISTER PAGE
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        username = request.form['username']

        email = request.form['email']

        password = request.form['password']

        new_user = User(
            username=username,
            email=email,
            password=password
        )

        db.session.add(new_user)

        db.session.commit()

        return redirect('/login')

    return render_template('register.html')

# LOGIN PAGE
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user:

            if user.password == password:

                session['user_id'] = user.id    

                return redirect('/dashboard')

        else:

            return "Invalid Email or Password"

    return render_template('login.html')

# DASHBOARD PAGE
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():

    if 'user_id' not in session:

        return redirect('/login')

    if request.method == 'POST':

        diary_text = request.form['content']

        new_entry = Entry(
            content=diary_text,
            user_id=session['user_id']
            )

        db.session.add(new_entry)

        db.session.commit()

        return redirect('/dashboard')

    entries = Entry.query.filter_by(
        user_id=session['user_id']
        ).order_by(
        Entry.date.desc()
    ).all()

    return render_template(
        'dashboard.html',
        entries=entries
    )

# DELETE ENTRY
@app.route('/delete/<int:id>')
def delete(id):

    entry = db.session.get(Entry, id)

    db.session.delete(entry)

    db.session.commit()

    return redirect('/dashboard')

# EDIT ENTRY
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):

    entry = db.session.get(Entry, id)

    if request.method == 'POST':

        entry.content = request.form['content']

        db.session.commit()

        return redirect('/dashboard')

    return render_template(
        'edit.html',
        entry=entry
    )

# PROFILE PAGE
@app.route('/profile')
def profile():

    if 'user_id' not in session:

        return redirect('/login')

    user = db.session.get(
        User,
        session['user_id']
    )

    return render_template(
        'profile.html',
        user=user
    )

# LOGOUT
@app.route('/logout')
def logout():

    session.pop('user_id', None)

    return redirect('/')

# RUN APP
if __name__ == '__main__':

    with app.app_context():

        db.create_all()

    app.run(host='0.0.0.0', port=5000,
        debug=True)
    