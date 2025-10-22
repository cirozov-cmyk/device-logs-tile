from flask import Flask, jsonify, send_file, request
import json
import time
import os
from datetime import datetime

app = Flask(__name__)

class DeviceLogsTile:
    def __init__(self):
        self.logs = []
        
    def add_log(self, message):
        """Добавление лога"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.logs.insert(0, {
            "timestamp": timestamp,
            "message": message
        })
        # Храним только последние 50 логов
        self.logs = self.logs[:50]
    
    def get_tile_data(self):
        """Данные для tile в формате iHost"""
        logs_html = "".join([
            f'<div class="log-item"><span class="timestamp">{log["timestamp"]}</span><div>{log["message"]}</div></div>'
            for log in self.logs[:5]  # Показываем последние 5 логов
        ])
        
        return {
            "template": "custom",
            "data": {
                "title": "📊 Device Logs",
                "content": f'''
                <div class="device-logs-tile">
                    <style>
                        .device-logs-tile {{ 
                            padding: 12px; 
                            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                            border-radius: 10px;
                            color: white;
                            height: 100%;
                            font-family: Arial, sans-serif;
                        }}
                        .log-item {{ 
                            padding: 4px 0; 
                            border-bottom: 1px solid rgba(255,255,255,0.2);
                            font-size: 12px;
                        }}
                        .timestamp {{ 
                            font-size: 10px; 
                            opacity: 0.8;
                            display: block;
                        }}
                        h3 {{ margin: 0 0 8px 0; font-size: 14px; }}
                    </style>
                    <h3>📊 Device Logs</h3>
                    <div id="logs">
                        {logs_html if logs_html else '<div class="log-item">No logs yet</div>'}
                    </div>
                </div>
                ''',
                "refresh_interval": 10  # Обновление каждые 10 секунд
            }
        }

# Глобальный экземпляр
tile_manager = DeviceLogsTile()

# Добавляем тестовые логи
tile_manager.add_log("✅ Tile started successfully")
tile_manager.add_log("🔄 Monitoring devices...")
tile_manager.add_log("📡 Connected to iHost")

@app.route('/')
def index():
    return "Device Logs Tile is running!"

@app.route('/tile')
def tile_endpoint():
    """Основной endpoint для tile в iHost"""
    return jsonify(tile_manager.get_tile_data())

@app.route('/api/logs')
def api_logs():
    """API для получения логов (JSON)"""
    return jsonify(tile_manager.logs)

@app.route('/api/add_log', methods=['POST'])
def api_add_log():
    """API для добавления лога"""
    data = request.json
    if data and 'message' in data:
        tile_manager.add_log(data['message'])
        return jsonify({"status": "success"})
    return jsonify({"status": "error"})

@app.route('/health')
def health_check():
    """Health check для iHost"""
    return jsonify({"status": "healthy", "service": "device-logs-tile"})

if __name__ == '__main__':
    print("🚀 Starting Device Logs Tile for iHost...")
    print("📍 Tile API: http://0.0.0.0:8080/tile")
    print("📍 Health check: http://0.0.0.0:8080/health")
    
    app.run(host='0.0.0.0', port=8080, debug=False)
