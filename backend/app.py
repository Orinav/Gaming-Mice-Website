from flask import Flask, request, jsonify
from flask_cors import CORS
from database import (
    initialize_mice_database,
    get_mice_database,
    add_mouse_to_mice_database,
    delete_mouse_from_mice_database
)

app = Flask(__name__)
CORS(app)

initialize_mice_database()

@app.route('/api/mice', methods=['GET'])
def get_mice():
    db = get_mice_database()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM mice')
    all_mice = [dict(row) for row in cursor.fetchall()]
    db.close()
    return jsonify(all_mice)

@app.route('/api/mice', methods=['POST'])
def add_mouse():
    data = request.json
    add_mouse_to_mice_database(
        data['brand'], data['model'], data['weight_grams'],
        data['sensor'], data['image_url'], data['buy_url']
    )
    return jsonify({"message": "Mouse added!"}), 201

@app.route('/api/mice/<int:mouse_id>', methods=['DELETE'])
def delete_mouse(mouse_id):
    delete_mouse_from_mice_database(mouse_id)
    return jsonify({"message": "Mouse deleted!"}), 200

if __name__ == '__main__':
    app.run(debug=True)