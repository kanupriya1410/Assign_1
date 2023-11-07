##1.
from flask import Flask
app = Flask("kaka")
@app.route('/ping', methods=['GET'])
def ping():
    return 'Pong'
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
#%%
##2.
from flask import Flask, request, jsonify
app = Flask()
SECRET_KEY = 'your_secret_key'  # Replace with your secret key
@app.route('/authorize', methods=['POST'])
def authorize():
    # Get the provided secret key from the request header
    provided_key = request.headers.get('Authorization')
    # Check if the provided key matches the pre-shared key
    if provided_key == SECRET_KEY:
        return jsonify({'message': 'Authorized'})
    else:
        return jsonify({'message': 'Unauthorized'}), 401
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
#%%

from flask import Flask, request, jsonify
import sqlite3
app = Flask("aaa")
# Create an SQLite database and a table
conn = sqlite3.connect('data.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS data (key TEXT PRIMARY KEY, value TEXT)''')
conn.commit()
conn.close()
@app.route('/save', methods=['POST'])
def save_data():
    try:
        data = request.json  # Expect JSON data with 'key' and 'value'
        key = data['key']
        value = data['value']
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        c.execute('INSERT OR REPLACE INTO data (key, value) VALUES (?, ?)', (key, value))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Data saved successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400
@app.route('/get', methods=['GET'])
def get_data():
    try:
        key = request.args.get('key')
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        c.execute('SELECT value FROM data WHERE key = ?', (key,))
        result = c.fetchone()
        conn.close()
        if result:
            return jsonify({'value': result[0]})
        else:
            return jsonify({'message': 'Key not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400
@app.route('/delete', methods=['DELETE'])
def delete_data():
    try:
        key = request.args.get('key')
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        c.execute('DELETE FROM data WHERE key = ?', (key,))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Data deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

#%%
