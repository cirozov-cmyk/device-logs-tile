from flask import Flask, jsonify, request
import json
import time
from datetime import datetime
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Хранилище логов
device_logs = []

class DeviceLogsManager:
    def __init__(self):
        self.logs = []
        self.add_log("🚀 Плитка журналов запущена")
        self.add_log("📡 Мониторинг устройств активирован")
        self.add_log("✅ Система готова к работе")
    
    def add_log(self, message, device="system"):
        """Добавление новой записи в журнал"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = {
            "timestamp": timestamp,
            "message": message,
            "device": device
        }
        self.logs.insert(0, log_entry)
        # Храним только последние 20 записей
        self.logs = self.logs[:20]
        logger.info(f"New log: {message}")
    
    def get_recent_logs(self, count=5):
        """Получить последние записи"""
        return self.logs[:count]
    
    def get_tile_html(self):
        """Генерация HTML контента для плитки"""
        recent_logs = self.get_recent_logs(5)
        
        logs_html = ""
        for log in recent_logs:
            logs_html += f"""
            <div class="log-entry">
                <span class="timestamp">{log['timestamp']}</span>
                <span class="message">{log['message']}</span>
            </div>
            """
        
        if not logs_html:
            logs_html = '<div class="log-entry">Нет данных</div>'
        
        return f"""
        <div class="device-logs-tile">
            <style>
                .device-logs-tile {{
                    padding: 12px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    border-radius: 12px;
                    color: white;
                    height: 100%;
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                }}
                .tile-header {{
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                    margin-bottom: 10px;
                    border-bottom: 1px solid rgba(255, 255, 255, 0.3);
                    padding-bottom: 8px;
                }}
                .tile-title {{
                    font-size: 16px;
                    font-weight: 600;
                    margin: 0;
                }}
                .logs-container {{
                    max-height: 120px;
                    overflow-y: auto;
                }}
                .log-entry {{
                    display: flex;
                    justify-content: space-between;
                    align-items: flex-start;
                    padding: 4px 0;
                    border-bottom: 1px solid rgba(255, 255, 255, 0.2);
                    font-size: 11px;
                    line-height: 1.3;
                }}
                .timestamp {{
                    opacity: 0.8;
                    min-width: 40px;
                    font-size: 10px;
                }}
                .message {{
                    flex: 1;
                    margin-left: 8px;
                    word-break: break-word;
                }}
                .status-indicator {{
                    width: 8px;
                    height: 8px;
                    border-radius: 50%;
                    background: #4ade80;
                    animation: pulse 2s infinite;
                }}
                @keyframes pulse {{
                    0% {{ opacity: 1; }}
                    50% {{ opacity: 0.5; }}
                    100% {{ opacity: 1; }}
                }}
            </style>
            
            <div class="tile-header">
                <h3 class="tile-title">📊 Журналы</h3>
                <div class="status-indicator" title="Система активна"></div>
            </div>
            
            <div class="logs-container">
                {logs_html}
            </div>
        </div>
        """

# Инициализация менеджера логов
logs_manager = DeviceLogsManager()

# Добавляем тестовые логи
logs_manager.add_log("🔌 Устройство #1 подключено", "device_001")
logs_manager.add_log("🌡️ Температура в норме", "sensor_001")
logs_manager.add_log("💡 Свет выключен", "light_001")

@app.route('/')
def index():
    """Главная страница"""
    return """
    <html>
        <head>
            <title>Device Logs Tile</title>
            <meta charset="utf-8">
        </head>
        <body>
            <h1>🚀 Плитка журналов устройств</h1>
            <p>Сервер работает корректно. Endpoints:</p>
            <ul>
                <li><a href="/tile">/tile</a> - данные для плитки iHost</li>
                <li><a href="/health">/health</a> - проверка здоровья</li>
                <li><a href="/logs">/logs</a> - все логи (JSON)</li>
                <li><a href="/manifest.json">/manifest.json</a> - манифест</li>
            </ul>
        </body>
    </html>
    """

@app.route('/tile')
def tile_endpoint():
    """Основной endpoint для плитки iHost"""
    try:
        response_data = {
            "template": "custom",
            "data": {
                "title": "📊 Журналы",
                "content": logs_manager.get_tile_html(),
                "refresh_interval": 10
            }
        }
        logger.info("Tile data requested")
        return jsonify(response_data)
    except Exception as e:
        logger.error(f"Error in tile endpoint: {e}")
        return jsonify({
            "template": "custom",
            "data": {
                "title": "❌ Ошибка",
                "content": "<div style='padding:20px;color:red'>Ошибка загрузки</div>",
                "refresh_interval": 30
            }
        })

@app.route('/health')
def health_check():
    """Проверка здоровья сервиса"""
    return jsonify({
        "status": "healthy",
        "service": "device-logs-tile",
        "timestamp": datetime.now().isoformat(),
        "logs_count": len(logs_manager.logs)
    })

@app.route('/logs')
def get_logs():
    """API для получения всех логов"""
    return jsonify({
        "status": "success",
        "logs": logs_manager.logs,
        "total": len(logs_manager.logs)
    })

@app.route('/add_log', methods=['POST'])
def add_log():
    """API для добавления нового лога"""
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({"status": "error", "message": "No message provided"}), 400
        
        message = data['message']
        device = data.get('device', 'unknown')
        
        logs_manager.add_log(message, device)
        
        return jsonify({
            "status": "success", 
            "message": "Log added",
            "total_logs": len(logs_manager.logs)
        })
    except Exception as e:
        logger.error(f"Error adding log: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/manifest.json')
def manifest():
    """Манифест для iHost"""
    return jsonify({
        "name": "device-logs-tile",
        "version": "1.0.0",
        "description": "Мониторинг журналов устройств в реальном времени",
        "type": "tile",
        "entry": "http://localhost:8088/tile",
        "config": {
            "width": 2,
            "height": 2,
            "title": "📊 Журналы",
            "refresh_interval": 10
        }
    })

@app.route('/test')
def test_page():
    """Тестовая страница для отладки"""
    return f"""
    <html>
        <head><title>Test Tile</title></head>
        <body>
            <h1>Тест плитки</h1>
            <div style="width: 200px; height: 150px;">
                {logs_manager.get_tile_html()}
            </div>
            <p>Всего записей: {len(logs_manager.logs)}</p>
            <button onclick="addTestLog()">Добавить тестовый лог</button>
            <script>
                function addTestLog() {{
                    fetch('/add_log', {{
                        method: 'POST',
                        headers: {{'Content-Type': 'application/json'}},
                        body: JSON.stringify({{message: '🔄 Тестовое событие ' + new Date().toLocaleTimeString()}})
                    }}).then(r => r.json()).then(console.log);
                }}
            </script>
        </body>
    </html>
    """

if __name__ == '__main__':
    logger.info("🚀 Запуск плитки журналов устройств...")
    logger.info("📍 Порт: 8080")
    logger.info("📍 Основной endpoint: /tile")
    logger.info("📍 Проверка здоровья: /health")
    logger.info("📍 Все логи: /logs")
    
    # Запуск Flask приложения
    app.run(
        host='0.0.0.0', 
        port=8080, 
        debug=False,
        threaded=True
    )
