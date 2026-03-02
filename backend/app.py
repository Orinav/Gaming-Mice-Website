from flask import Flask, render_template, jsonify, request
from flask_cors import CORS

from backend.database import add_mouse_to_mice_database, delete_mouse_from_mice_database
from database import initialize_mice_database, insert_sample_mice, get_mice_database

app = Flask(__name__)
CORS(app)

initialize_mice_database()
insert_sample_mice()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/mice', methods=['POST'])
def add_mouse():
    data = request.json
    try:
        (add_mouse_to_mice_database
            (
                data['brand'], data['model'], data['weight_grams'],
                data['grip_style'], data['sensor'], data['image_url'], data['buy_url']
            )
        )
        return jsonify({"message": "Mouse added!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/mice/<int:mouse_id>', methods=['DELETE'])
def delete_mouse(mouse_id):
    try:
        delete_mouse_from_mice_database(mouse_id)
        return jsonify({"message": "Mouse deleted!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/mice')
def get_mice():
    mice_database = get_mice_database()
    cursor = mice_database.cursor()
    cursor.execute('SELECT * FROM mice')

    all_mice = [dict(row) for row in cursor.fetchall()]
    mice_database.close()

    return jsonify(all_mice)


if __name__ == '__main__':
    app.run(debug=True)
