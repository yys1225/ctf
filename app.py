from flask import Flask, request, render_template_string, redirect, url_for

app = Flask(__name__)

# SQLite database setup
import sqlite3
conn = sqlite3.connect('ctf.db', check_same_thread=False)
cursor = conn.cursor()

# Create a users table
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT,
                    password TEXT)''')
conn.commit()

# Add a sample admin user
cursor.execute("INSERT OR IGNORE INTO users (username, password) VALUES ('admin', 'str0ng_passw0rd')")
conn.commit()

@app.route('/')
def login_page(error=None):
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Login</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                }
                .login-container {
                    background-color: #fff;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                    text-align: center;
                    width: 300px;
                }
                .login-container h1 {
                    margin-bottom: 20px;
                }
                .login-container input[type="text"],
                .login-container input[type="password"] {
                    width: 80%;
                    padding: 10px;
                    margin: 10px 0;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                }
                .login-container input[type="submit"] {
                    width: 50%;
                    padding: 10px;
                    background-color: #28a745;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                }
                .login-container input[type="submit"]:hover {
                    background-color: #218838;
                }
                .error-message {
                    color: red;
                    margin-top: 10px;
                }
                .hint {
                    font-size: 12px;
                    color: #666;
                    margin-top: 10px;
                }
            </style>
        </head>
        <body>
            <div class="login-container">
                <h1>Login</h1>
                                  
                <form method="POST" action="/login">
                                  <p>Login as admin to get the flag.</p>
                    <input type="text" name="username" placeholder="Username" required><br>
                    <input type="password" name="password" placeholder="Password" required><br>
                        <div class="hint">
                            
                            <p>Hint: Think about how SQL queries are constructed.</p>
                            <p>What happens if you input something unexpected?</p>
                         </div>
                    <input type="submit" value="Submit">
                </form>

                {% if error %}
                    <div class="error-message">{{ error }}</div>
                {% endif %}
            </div>
        </body>
        </html>
    ''', error=error)

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # Check if the username exists
    cursor.execute(f"SELECT * FROM users WHERE username='{username}'")
    user = cursor.fetchone()

    if user:
        # Check if the password is correct
        cursor.execute(f"SELECT * FROM users WHERE username='{username}' AND password='{password}'")
        user = cursor.fetchone()
        if user:
            if user[1] == 'admin':
                # Redirect to the /flag route for admin
                return redirect(url_for('flag', role='admin'))
            else:
                # Redirect to the /flag route for regular users
                return redirect(url_for('flag', role='user'))
        else:
            # Password is incorrect
            return login_page(error="Invalid password. Please try again.")
    else:
        # Username does not exist
        return login_page(error="Invalid username. Please try again.")

@app.route('/flag')
def flag():
    role = request.args.get('role', 'user')  # Default to 'user' if role is not provided
    username = request.args.get('username', 'guest')  # Default to 'guest' if username is not provided

    if role == 'admin':
        message = f"Welcome!\n\nFlag: CTF{{SQL1nj3ct10n}}"
    else:
        message = f"Welcome!"

    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Flag</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    font-size: 8px;
                    background-color: #f4f4f4;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                }
                .message-container {
                    background-color: #fff;
                    padding: 30px;
                    border-radius: 8px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                    text-align: center;
                    width: 300px;
                    white-space: pre-wrap;
                }
                .message-container h1 {
                    margin-bottom: 20px;
                }
            </style>
        </head>
        <body>
            <div class="message-container">
                <h1>{{ message }}</h1>
            </div>
        </body>
        </html>
    ''', message=message)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
