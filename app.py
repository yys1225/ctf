from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

# Initialize the database with Apple products and a hidden flag
def init_db():
    conn = sqlite3.connect('apple_products.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS apple_products (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    serial_number TEXT NOT NULL
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS secret_products (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    secret_serial_number TEXT NOT NULL
                )''')
    # Insert sample Apple products with serial numbers
    c.execute("INSERT OR IGNORE INTO apple_products (id, name, serial_number) VALUES (1, 'iPhone 15', 'SN1234567890')")
    c.execute("INSERT OR IGNORE INTO apple_products (id, name, serial_number) VALUES (2, 'MacBook Air M2', 'SN2345678901')")
    c.execute("INSERT OR IGNORE INTO apple_products (id, name, serial_number) VALUES (3, 'iPad Pro', 'SN3456789012')")
    c.execute("INSERT OR IGNORE INTO apple_products (id, name, serial_number) VALUES (4, 'Apple Watch Series 9', 'SN4567890123')")
    c.execute("INSERT OR IGNORE INTO apple_products (id, name, serial_number) VALUES (5, 'AirPods Pro', 'SN5678901234')")
    # Insert the flag into the secrets table
    c.execute("INSERT OR IGNORE INTO secret_products (id, name, secret_serial_number) VALUES (0, 'Secret Product', 'CTF{SQL_1nj3cti0n}')")
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Apple Vault</title>
            <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap" rel="stylesheet">
            <style>
                body {
                    font-family: 'Poppins', sans-serif;
                    background: linear-gradient(135deg, #f5f7fa, #c3cfe2);
                    margin: 0;
                    padding: 0;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    flex-direction: column;
                }
                h1 {
                    color: #333;
                    font-size: 2.5rem;
                    margin-bottom: 20px;
                    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
                }
                .container {
                    background: white;
                    padding: 40px;
                    border-radius: 15px;
                    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
                    max-width: 500px;
                    width: 100%;
                    text-align: center;
                }
                form {
                    margin: 20px 0;
                }
                input[type="text"] {
                    width: 80%;
                    padding: 12px;
                    margin: 10px 0;
                    border: 2px solid #ddd;
                    border-radius: 8px;
                    font-size: 16px;
                    transition: border-color 0.3s ease;
                }
                input[type="text"]:focus {
                    border-color: #007bff;
                    outline: none;
                }
                input[type="submit"] {
                    background-color: #007bff;
                    color: white;
                    padding: 12px 24px;
                    border: none;
                    border-radius: 8px;
                    font-size: 16px;
                    cursor: pointer;
                    transition: background-color 0.3s ease;
                }
                input[type="submit"]:hover {
                    background-color: #0056b3;
                }
                table {
                    margin: 20px auto;
                    width: 100%;
                    border-collapse: collapse;
                    text-align: left;
                    background: white;
                    border-radius: 8px;
                    overflow: hidden;
                    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
                }
                th, td {
                    padding: 12px;
                    border-bottom: 1px solid #ddd;
                }
                th {
                    background-color: #007bff;
                    color: white;
                }
                tr:hover {
                    background-color: #f1f1f1;
                }
                .hint {
                    color: #666;
                    font-style: italic;
                    margin-top: 20px;
                    font-size: 14px;
                }
                .error {
                    color: red;
                    margin-top: 20px;
                }
                a {
                    color: #007bff;
                    text-decoration: none;
                    transition: color 0.3s ease;
                }
                a:hover {
                    color: #0056b3;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Welcome to the Apple Vault</h2>
                <p>Search for Apple products in our database. Rumor has it that there's a <strong>Apple's secret product</strong> in the system. Can you find it?</p>
                <form method="GET" action="/search">
                    <input type="text" name="query" placeholder="Enter Apple product name" required>
                    <input type="submit" value="Search">
                </form>
                <p class="hint">Hint: What happens if you search for <code>' OR '1'='1</code>?</p>
            </div>
        </body>
        </html>
    '''

@app.route('/search')
def search():
    query = request.args.get('query', '')
    conn = sqlite3.connect('apple_products.db')
    c = conn.cursor()
    try:
        # Vulnerable SQL query
        sql = f"SELECT id, name, serial_number FROM apple_products WHERE name LIKE '%{query}%'"
        c.execute(sql)
        results = c.fetchall()
        output = "<table><tr><th>ID</th><th>Name</th><th>Serial Number</th></tr>"
        for row in results:
            output += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td></tr>"
        output += "</table>"
    except Exception as e:
        output = f"<div class='error'>Error: {str(e)}</div>"
    conn.close()
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Search Results</title>
            <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap" rel="stylesheet">
            <style>
                body {
                    font-family: 'Poppins', sans-serif;
                    background: linear-gradient(135deg, #f5f7fa, #c3cfe2);
                    margin: 0;
                    padding: 0;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    flex-direction: column;
                }
                .container {
                    background: white;
                    padding: 40px;
                    border-radius: 15px;
                    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
                    max-width: 800px;
                    width: 100%;
                    text-align: center;
                }
                table {
                    margin: 20px auto;
                    width: 100%;
                    border-collapse: collapse;
                    text-align: left;
                    background: white;
                    border-radius: 8px;
                    overflow: hidden;
                    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
                }
                th, td {
                    padding: 12px;
                    border-bottom: 1px solid #ddd;
                }
                th {
                    background-color: #007bff;
                    color: white;
                }
                tr:hover {
                    background-color: #f1f1f1;
                }
                .error {
                    color: red;
                    margin-top: 20px;
                }
                a {
                    color: #007bff;
                    text-decoration: none;
                    transition: color 0.3s ease;
                }
                a:hover {
                    color: #0056b3;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Search Results</h1>
                {{ output | safe }}
                <p><a href="/">Back to Search</a></p>
            </div>
        </body>
        </html>
    ''', output=output)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
