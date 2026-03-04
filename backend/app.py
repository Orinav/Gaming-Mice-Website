from flask import Flask, request, jsonify
from flask_cors import CORS
from database import (
    initialize_mice_database,
    get_mice_database,
    add_mouse_to_mice_database,
    delete_mouse_from_mice_database,
    add_to_favorites,
    remove_from_favorites,
    get_user_favorites
)

app = Flask(__name__)
CORS(app)

initialize_mice_database()

DEFAULT_USER_ID = 1

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

@app.route('/api/favorites', methods=['GET'])
def get_favorites():
    favs = get_user_favorites(DEFAULT_USER_ID)
    return jsonify(favs)

@app.route('/api/favorites', methods=['POST'])
def add_favorite():
    data = request.json
    mouse_id = data.get('mouse_id')
    add_to_favorites(DEFAULT_USER_ID, mouse_id)
    return jsonify({"message": "Added to favorite"}), 201

@app.route('/api/favorites/<int:mouse_id>', methods=['DELETE'])
def remove_favorite(mouse_id):
    remove_from_favorites(DEFAULT_USER_ID, mouse_id)
    return jsonify({"message": "Removed from favorite"}), 200

if __name__ == '__main__':
    app.run(debug=True)