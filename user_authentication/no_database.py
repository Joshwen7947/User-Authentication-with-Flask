from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

# Dummy database for demonstration (replace with actual database)
users = {'user1': generate_password_hash('password1')}

@app.route('/')
def home():
    """Displays a Page based on the session of the current user

    Returns:
        html template: Returns the Dashboard or Index
    """
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Confirms username and password then log into session

    Returns:
        html template: Directs the user to a page matching their login info
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and check_password_hash(users[username], password):
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template('index.html', error='Invalid username or password.')
    return redirect(url_for('home'))


@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            return render_template('register.html', error='Username already exists.')
        else:
            users[username] = generate_password_hash(password)
            session['username'] = username
            return redirect(url_for('dashboard'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
