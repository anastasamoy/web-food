from flask import Flask, jsonify, request
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app, origins="*")

@app.route('/api/recipes', methods=['GET'])
def get_recipes():
    # Пример данных
    return jsonify({"recipes": [
        {"id": 1, "title": "Борщ"},
        {"id": 2, "title": "Плов"}
    ]})

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    # Логика регистрации (заглушка)
    return jsonify({"success": True})

if __name__ == '__main__':
    app.run(debug=True)
