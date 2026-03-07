from flask import Flask, jsonify
from flask_cors import CORS
import logging
from apscheduler.schedulers.background import BackgroundScheduler

from database import db_get_mice, db_delete
from scraper import sync_mice_data_job

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')

app = Flask(__name__)
CORS(app)

# Making the scheduler work in 00:00 in Israel timezone.
scheduler = BackgroundScheduler()
scheduler.add_job(func=sync_mice_data_job, trigger="cron", hour=0, minute=0, timezone="Asia/Jerusalem")
scheduler.start()


@app.route('/api/mice', methods=['GET'])
def api_get_mice():
    try:
        mice = db_get_mice()
        mice_amount = len(mice)
        logger.info(f'API Request: Successfully fetched {mice_amount} mice.')
        return jsonify(mice)
    except Exception as e:
        logger.exception(f'Error in GET /api/mice: {e}.')
        return jsonify({"error": "Failed to fetch mice."}), 500

@app.route('/api/mice/<int:mouse_id>', methods=['DELETE'])
def api_delete_mouse(mouse_id):
    try:
        db_delete(mouse_id)
        logger.info(f'API Request: Deleted mouse with ID {mouse_id}.')
        return '', 204
    except Exception as e:
        logger.exception(f'Error in DELETE /api/mice/{mouse_id}: {e}')
        return jsonify({"error": "Failed to delete mouse"}), 500

if __name__ == '__main__':
    logger.info("Starting Flask server...")
    app.run(debug=True, use_reloader=False)