from flask import Flask
import json
import time
import logging
from threading import Thread
import requests

app = Flask(__name__)

# Конфигурация
CONFIG = {
    "port": 5000,
    "refresh_interval": 30
}

class TileManager:
    def __init__(self):
        self.tile_data = {
            "template": "custom", 
            "data": {
                "title": "Device Logs",
                "content": self.generate_html(),
                "refresh_interval": CONFIG["refresh_interval"]
            }
        }
    
    def generate_html(self):
        """Генерация полного HTML контента"""
        return """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Device Logs</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background: #f5f5f5;
        }
        .container {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .log-entry {
            padding: 10px;
            border-bottom: 1px solid #eee;
            margin: 5px 0;
        }
        .timestamp {
            color: #666;
            font-size: 12px;
        }
        .message {
            color: #333;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>📊 Device Logs Monitor</h2>
        <div id="logs">
            <div class="log-entry">
                <span class="timestamp">2025-10-22 11:15:02</span>
                <span class="message">✅ Tile successfully started</span>
            </div>
            <div class="log-entry">
                <span class="timestamp">2025-10-22 11:15:02</span>
                <span class="message">🔄 Auto-refresh every 30 seconds</span>
            </div>
            <div class="log-entry">
                <span class="timestamp">2025-10-22 11:15:02</span>
                <span class="message">📡 Monitoring device activities...</span>
            </div>
        </div>
    </div>
    
    <script>
        // Автообновление каждые 30 секунд
        setTimeout(() => {
            window.location.reload();
        }, 30000);
        
        // Можно добавить динамическое обновление логов
        console.log("Device Logs Tile is running...");
    </script>
</body>
</html>
        """
    
    def update_tile(self):
        """Обновление данных tile"""
        self.tile_data["data"]["content"] = self.generate_html()
        # Здесь будет логика отправки данных в iHost
        print(f"Updating tile with: {json.dumps(self.tile_data)}")
        return self.tile_data

# Глобальный экземпляр
tile_manager = TileManager()

@app.route('/')
def index():
    return tile_manager.generate_html()

@app.route('/api/tile')
def get_tile_data():
    return json.dumps(tile_manager.update_tile())

def run_tile_updater():
    """Фоновая задача для обновления tile"""
    while True:
        try:
            tile_manager.update_tile()
            time.sleep(CONFIG["refresh_interval"])
        except Exception as e:
            print(f"Error in tile updater: {e}")
            time.sleep(10)

if __name__ == '__main__':
    # Запускаем фоновое обновление
    updater_thread = Thread(target=run_tile_updater)
    updater_thread.daemon = True
    updater_thread.start()
    
    # Запускаем Flask
    print("Starting Device Logs Tile...")
    app.run(host='0.0.0.0', port=CONFIG["port"], debug=False)
