from flask import Flask, jsonify, send_file
import json
import time
from datetime import datetime

app = Flask(__name__)

# Мок-данные логов (замените реальными)
DEVICE_LOGS = [
    {"timestamp": "12:30:45", "message": "✅ Device A connected"},
    {"timestamp": "12:28:12", "message": "🔄 Device B updating"},
    {"timestamp": "12:25:33", "message": "⚠️ Device C offline"}
]

@app.route('/tile')
def serve_tile():
    """Основной endpoint для tile"""
    return send_file('static/tile.html')

@app.route('/api/logs')
def get_logs():
    """API для получения логов"""
    return jsonify(DEVICE_LOGS)

@app.route('/api/tile/config')
def tile_config():
    """Конфигурация tile для iHost"""
    return jsonify({
        "template": "custom",
        "data": {
            "title": "Device Logs",
            "content": "Loading device logs...",
            "refresh_interval": 30
        }
    })

if __name__ == '__main__':
    print("Starting Device Logs Tile...")
    app.run(host='0.0.0.0', port=8080, debug=False)
