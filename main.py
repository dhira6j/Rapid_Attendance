from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import random
import string
from art import *
from flask import render_template_string

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# User database (you might want to use a database like SQLite, PostgreSQL, etc.)
users = {}
admin_code = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users:
            return "User already exists! Please choose a different username."
        else:
            # Hash the password before saving
            hashed_password = generate_password_hash(password)
            users[username] = hashed_password
            return redirect('/login')

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username not in users:
            return "User does not exist! Please sign up."
        else:
            # Check if the password matches the hashed password in the database
            if check_password_hash(users[username], password):
                session['username'] = username
                return redirect('/profile')
            else:
                return "Incorrect password! Please try again."

    return render_template('login.html')

@app.route('/profile')
def profile():
    if 'username' in session:
        username = session['username']
        return render_template('profile.html', username=username)
    else:
        return redirect('/login')

@app.route('/mark_attendance')
def mark_attendance():
    return render_template('mark_attendance.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

@app.route('/generate_code')
def generate_code():
    global admin_code
    # Generate a new random 6-character alphanumeric code for the admin
    admin_code = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
    html_code = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Generated Code</title>
            <style>
                body {{
                    font-family: 'Times New Roman', Times, serif;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                    text-align: center;
                }}
                .code {{
                    font-size: 4vw; /* Responsive font size */
                    max-width: 80%; /* Limit maximum width */
                }}
            </style>
        </head>
        <body>
            <div class="code">New admin code generated: {admin_code}</div>
        </body>
        </html>
        """

    return html_code

@app.route('/authenticate', methods=['POST'])
def authenticate():
    student_code = request.form['code']

    # Check if the entered code matches the admin code
    if student_code == admin_code:
        session['is_admin'] = True
        return redirect("https://rajram.pythonanywhere.com/")
    else:
        return "Authentication failed. Please enter a valid code."

@app.route('/welcome')
def welcome():
    if session.get('is_admin'):
        return render_template('welcome.html')
    else:
        return redirect(url_for('index'))

@app.route('/admin')
def admin():
    if session.get('is_admin'):
        return render_template('admin.html', admin_code=admin_code)
    else:
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
