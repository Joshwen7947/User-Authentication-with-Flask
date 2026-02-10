from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'your_secret_key'  

# Configuring SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    """User Model

    Args:
        db (_type_): Model from SQL Alchemy

    Returns:
        string: Only check_password returns, else used to store user info
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)



@app.route('/')
def home():
    """Displays a Page based on the session of the current user

    Returns:
        html template: Returns the Dashboard or Index
    """
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/settings')
def settings():
    if 'username' not in session:
        return redirect(url_for('home'))
    else:

        user = User.query.filter_by(username=session['username']).first()

        return render_template(
            'settings.html',
            username=user.username
        )

@app.route('/login', methods=['POST'])
def login():
    """Confirms username and password in the database using the model

    Returns:
        html template: Directs the user to a page matching their login info
    """
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    else:
        return render_template('index.html', error='Invalid username or password.')

@app.route('/register', methods=['POST'])
def register():
    """Registers a new user within the SQL Alchemy DB

    Returns:
        html template: Creates a session with the new user
    """
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()
    if user:
        return render_template('index.html', error='Username already exists.')
    else:
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        session['username'] = username
        return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ in '__main__':
    # Create a db and table
    with app.app_context():
        db.create_all()
    app.run(debug=True)
