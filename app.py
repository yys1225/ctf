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
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    text-align: center;
                    padding: 50px;
                }
                h1 {
                    color: #333;
                }
                form {
                    margin: 20px auto;
                    width: 300px;
                }
                input[type="text"] {
                    width: 100%;
                    padding: 10px;
                    margin: 10px 0;
                    border: 1px solid #ccc;
                    border-radius: 5px;
                }
                input[type="submit"] {
                    background-color: #007bff;
                    color: white;
                    padding: 10px 20px;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                }
                input[type="submit"]:hover {
                    background-color: #0056b3;
                }
                table {
                    margin: 20px auto;
                    width: 50%;
                    border-collapse: collapse;
                    text-align: left;
                }
                th, td {
                    padding: 10px;
                    border: 1px solid #ccc;
                }
                th {
                    background-color: #007bff;
                    color: white;
                }
                .hint {
                    color: #666;
                    font-style: italic;
                    margin-top: 20px;
                }
            </style>
        </head>
        <body>
            <h1>Welcome to the Apple</h1>
            <p>Search for Apple products in our database. Rumor has it that there's a <strong>Apple's secret product</strong> in the system. Can you find?</p>
            <form method="GET" action="/search">
                <input type="text" name="query" placeholder="Enter Apple product name" required>
                <input type="submit" value="Search">
            </form>
            <p class="hint">Hint: What happens if you search for <code>' OR '1'='1</code>?</p>
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
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    text-align: center;
                    padding: 50px;
                }
                table {
                    margin: 20px auto;
                    width: 50%;
                    border-collapse: collapse;
                    text-align: left;
                }
                th, td {
                    padding: 10px;
                    border: 1px solid #ccc;
                }
                th {
                    background-color: #007bff;
                    color: white;
                }
                .error {
                    color: red;
                }
            </style>
        </head>
        <body>
            <h1>Search Results</h1>
            {{ output | safe }}
            <p><a href="/">Back to Search</a></p>
        </body>
        </html>
    ''', output=output)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
