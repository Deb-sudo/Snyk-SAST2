import os
import sqlite3
import pickle
from flask import Flask, request

app = Flask(__name__)

DATABASE = "users.db"

# ❌ 1. SQL Injection vulnerability
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    # Directly interpolating user input in SQL
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    cursor.execute(query)
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return "Login successful!"
    else:
        return "Invalid credentials!"

# ❌ 2. Arbitrary Code Execution via unsafe deserialization
@app.route('/load-data', methods=['POST'])
def load_data():
    data = request.data
    # Pickle is unsafe for untrusted input
    obj = pickle.loads(data)
    return f"Object loaded: {obj}"

# ❌ 3. Command injection
@app.route('/ping', methods=['GET'])
def ping():
    host = request.args.get('host', '127.0.0.1')
    # User input used in shell command
    os.system(f"ping -c 1 {host}")
    return f"Pinged {host}"

# ❌ 4. Information disclosure
@app.route('/debug')
def debug():
    # Exposes sensitive environment details
    return str(dict(os.environ))

# ❌ 5. Insecure file write
@app.route('/upload', methods=['POST'])
def upload():
    filename = request.args.get('file', 'output.txt')
    content = request.data.decode('utf-8')
    # Does not sanitize path
    with open(filename, 'w') as f:
        f.write(content)
    return f"File {filename} written."

if __name__ == '__main__':
    app.run(debug=True)
