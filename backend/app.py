from flask import Flask, render_template, jsonify
from flask_cors import CORS
from database import initialize_mice_database, insert_sample_mice, get_mice_database

app = Flask(__name__)
CORS(app)

initialize_mice_database()
insert_sample_mice()


@app.route('/')
def index():
    return render_template('index.html')


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
