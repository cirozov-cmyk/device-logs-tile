from flask import Flask, jsonify, request
import json
import time
from datetime import datetime
import logging
import requests
import threading

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Конфигурация
NODE_RED_URL = "https://ihost3.baarv.crazedns.ru/logs"
UPDATE_INTERVAL = 10  # секунд

class NodeRedLogsManager:
    def __init__(self):
        self.logs = []
        self.last_update = None
        self.add_system_log("🚀 Плитка журналов запущена")
        self.add_system_log("📡 Подключение к Node-RED...")
        
        # Запускаем фоновое обновление логов
        self.start_background_updater()
    
    def add_system_log(self, message):
        """Добавление системного сообщения"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = {
            "timestamp": timestamp,
            "message": message,
            "type": "system",
            "source": "tile"
        }
        self.logs.insert(0, log_entry)
        self.logs = self.logs[:50]  # Храним 50 последних записей
    
    def fetch_node_red_logs(self):
        """Получение логов из Node-RED"""
        try:
            response = requests.get(NODE_RED_URL, timeout=5)
            if response.status_code == 200:
                node_red_data = response.json()
                self.process_node_red_data(node_red_data)
                self.last_update = datetime.now()
                return True
            else:
                self.add_system_log("❌ Node-RED недоступен")
                return False
        except Exception as e:
            self.add_system_log(f"⚠️ Ошибка подключения: {str(e)}")
            return False
    
    def process_node_red_data(self, node_red_data):
        """Обработка данных из Node-RED"""
        # Адаптируем под ваш формат данных из Node-RED
        if isinstance(node_red_data, list):
            for item in node_red_data[-10:]:  # Берем 10 последних записей
                if isinstance(item, dict):
                    # Преобразуем формат Node-RED в наш формат
                    log_entry = {
                        "timestamp": item.get('timestamp', datetime.now().strftime("%H:%M:%S")),
                        "message": self.format_message(item),
                        "type": item.get('type', 'info'),
                        "source": 'node-red'
                    }
                    # Добавляем только если такой записи еще нет
                    if not any(log['message'] == log_entry['message'] for log in self.logs):
                        self.logs.insert(0, log_entry)
        elif isinstance(node_red_data, dict):
            # Если Node-RED возвращает объект
            log_entry = {
                "timestamp": datetime.now().strftime("%H:%M:%S"),
                "message": self.format_message(node_red_data),
                "type": node_red_data.get('type', 'info'),
                "source": 'node-red'
            }
            if not any(log['message'] == log_entry['message'] for log in self.logs):
                self.logs.insert(0, log_entry)
        
        # Ограничиваем общее количество логов
        self.logs = self.logs[:50]
    
    def format_message(self, data):
        """Форматирование сообщения из данных Node-RED"""
        if 'message' in data:
            return data['message']
        elif 'payload' in data:
            return str(data['payload'])
        elif 'topic' in data:
            return f"{data['topic']}: {data.get('payload', 'No data')}"
        else:
            return str(data)
    
    def get_recent_logs(self, count=8):
        """Получить последние записи для отображения"""
        return self.logs[:count]
    
    def start_background_updater(self):
        """Запуск фонового обновления логов"""
        def updater():
            while True:
                self.fetch_node_red_logs()
                time.sleep(UPDATE_INTERVAL)
        
        thread = threading.Thread(target=updater, daemon=True)
        thread.start()
    
    def get_tile_html(self):
        """Генерация HTML контента для плитки"""
        recent_logs = self.get_recent_logs(8)
        
        logs_html = ""
        for log in recent_logs:
            icon = self.get_icon_for_type(log.get('type', 'info'))
            source_badge = f"<span class='source {log.get('source', 'system')}'>{log.get('source', 'sys')}</span>"
            
            logs_html += f"""
            <div class="log-entry {log.get('type', 'info')}">
                <div class="log-header">
                    <span class="timestamp">{log['timestamp']}</span>
                    {source_badge}
                </div>
                <div class="message">
                    <span class="icon">{icon}</span>
                    {log['message']}
                </div>
            </div>
            """
        
        if not logs_html:
            logs_html = '<div class="log-entry">📭 Нет данных от устройств</div>'
        
        last_update = self.last_update.strftime("%H:%M:%S") if self.last_update else "--:--:--"
        
        return f"""
        <div class="device-logs-tile">
            <style>
                .device-logs-tile {{
                    padding: 10px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    border-radius: 12px;
                    color: white;
                    height: 100%;
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                    font-size: 11px;
                }}
                .tile-header {{
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                    margin-bottom: 8px;
                    border-bottom: 1px solid rgba(255, 255, 255, 0.3);
                    padding-bottom: 6px;
                }}
                .tile-title {{
                    font-size: 14px;
                    font-weight: 600;
                    margin: 0;
                }}
                .last-update {{
                    font-size: 9px;
                    opacity: 0.7;
                }}
                .logs-container {{
                    max-height: 130px;
                    overflow-y: auto;
                    scrollbar-width: thin;
                }}
                .logs-container::-webkit-scrollbar {{
                    width: 4px;
                }}
                .logs-container::-webkit-scrollbar-thumb {{
                    background: rgba(255, 255, 255, 0.3);
                    border-radius: 2px;
                }}
                .log-entry {{
                    padding: 3px 0;
                    border-bottom: 1px solid rgba(255, 255, 255, 0.15);
                }}
                .log-header {{
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 1px;
                }}
                .timestamp {{
                    opacity: 0.8;
                    font-size: 9px;
                }}
                .source {{
                    background: rgba(255, 255, 255, 0.2);
                    padding: 1px 4px;
                    border-radius: 3px;
                    font-size: 8px;
                    text-transform: uppercase;
                }}
                .source.node-red {{
                    background: rgba(34, 197, 94, 0.3);
                }}
                .source.tile {{
                    background: rgba(59, 130, 246, 0.3);
                }}
                .message {{
                    display: flex;
                    align-items: flex-start;
                    gap: 4px;
                    line-height: 1.2;
                }}
                .icon {{
                    flex-shrink: 0;
                    margin-top: 1px;
                }}
                .status-indicator {{
                    width: 6px;
                    height: 6px;
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
                <div class="status-indicator"></div>
            </div>
            
            <div class="last-update">Обновлено: {last_update}</div>
            
            <div class="logs-container">
                {logs_html}
            </div>
        </div>
        """
    
    def get_icon_for_type(self, log_type):
        """Получить иконку для типа лога"""
        icons = {
            'error': '❌',
            'warning': '⚠️',
            'success': '✅',
            'info': 'ℹ️',
            'system': '⚙️',
            'device': '📱'
        }
        return icons.get(log_type, '📝')

# Инициализация менеджера логов
logs_manager = NodeRedLogsManager()

@app.route('/')
def index():
    return """
    <html>
        <head><title>Device Logs Tile</title><meta charset="utf-8"></head>
        <body>
            <h1>🚀 Плитка журналов + Node-RED</h1>
            <p>Интеграция с: <a href="https://ihost3.baarv.crazedns.ru/logs">Node-RED Logs</a></p>
            <ul>
                <li><a href="/tile">/tile</a> - данные для плитки</li>
                <li><a href="/logs">/logs</a> - все логи (JSON)</li>
                <li><a href="/health">/health</a> - статус системы</li>
                <li><a href="/force-update">/force-update</a> - принудительное обновление</li>
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
                "refresh_interval": 15
            }
        }
        return jsonify(response_data)
    except Exception as e:
        logger.error(f"Error in tile endpoint: {e}")
        return jsonify({
            "template": "custom",
            "data": {
                "title": "❌ Ошибка",
                "content": f"<div style='padding:15px;color:red'>Ошибка: {str(e)}</div>",
                "refresh_interval": 30
            }
        })

@app.route('/health')
def health_check():
    """Проверка здоровья сервиса"""
    return jsonify({
        "status": "healthy",
        "service": "device-logs-tile",
        "node_red_connected": logs_manager.last_update is not None,
        "last_update": logs_manager.last_update.isoformat() if logs_manager.last_update else None,
        "total_logs": len(logs_manager.logs)
    })

@app.route('/logs')
def get_logs():
    """API для получения всех логов"""
    return jsonify({
        "status": "success",
        "logs": logs_manager.logs,
        "total": len(logs_manager.logs),
        "last_update": logs_manager.last_update.isoformat() if logs_manager.last_update else None
    })

@app.route('/force-update')
def force_update():
    """Принудительное обновление логов"""
    success = logs_manager.fetch_node_red_logs()
    return jsonify({
        "status": "success" if success else "error",
        "message": "Logs updated" if success else "Update failed",
        "last_update": logs_manager.last_update.isoformat() if logs_manager.last_update else None
    })

@app.route('/manifest.json')
def manifest():
    """Манифест для iHost"""
    return jsonify({
        "name": "device-logs-tile",
        "version": "1.1.0",
        "description": "Мониторинг журналов устройств из Node-RED",
        "type": "tile",
        "entry": "http://localhost:8088/tile",
        "config": {
            "width": 2,
            "height": 2,
            "title": "📊 Журналы",
            "refresh_interval": 15
        }
    })

if __name__ == '__main__':
    logger.info("🚀 Запуск плитки журналов с интеграцией Node-RED...")
    logger.info(f"📍 Подключение к Node-RED: {NODE_RED_URL}")
    logger.info("📍 Основной endpoint: /tile")
    
    app.run(host='0.0.0.0', port=8080, debug=False, threaded=True)
