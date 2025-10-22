from flask import Flask, jsonify
import time
from datetime import datetime

app = Flask(__name__)

# Простое хранилище логов
logs = [
    {"timestamp": datetime.now().strftime("%H:%M:%S"), "message": "🚀 Плитка запущена", "type": "system"},
    {"timestamp": datetime.now().strftime("%H:%M:%S"), "message": "✅ Система готова", "type": "success"},
    {"timestamp": datetime.now().strftime("%H:%M:%S"), "message": "📡 Ожидание данных", "type": "info"}
]

@app.route('/')
def index():
    return "Device Logs Tile is running!"

@app.route('/tile')
def tile_endpoint():
    """Простой endpoint для плитки"""
    try:
        # ОЧЕНЬ ПРОСТОЙ HTML без CSS который может сломаться
        logs_html = "".join([
            f'<div>{log["timestamp"]} {log["message"]}</div>'
            for log in logs[:5]
        ])
        
        tile_content = f'''
        <div>
            <h3>📊 Журналы</h3>
            <div>
                {logs_html}
            </div>
        </div>
        '''
        
        return jsonify({
            "template": "custom",
            "data": {
                "title": "📊 Журналы",
                "content": tile_content,
                "refresh_interval": 30
            }
        })
        
    except Exception as e:
        return jsonify({
            "template": "custom", 
            "data": {
                "title": "❌ Ошибка",
                "content": f"<div>Ошибка: {str(e)}</div>",
                "refresh_interval": 60
            }
        })

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

@app.route('/logs')
def get_logs():
    return jsonify({"logs": logs, "total": len(logs)})

@app.route('/manifest.json') 
def manifest():
    return jsonify({
        "name": "device-logs-tile",
        "version": "1.0.0",
        "description": "Мониторинг журналов устройств",
        "type": "tile", 
        "entry": "http://localhost:8088/tile",
        "config": {
            "width": 2,
            "height": 2,
            "title": "📊 Журналы",
            "refresh_interval": 30
        }
    })

if __name__ == '__main__':
    print("✅ Starting SUPER SIMPLE device logs tile...")
    print("📍 Port: 8080")
    print("📍 Tile endpoint: /tile")
    app.run(host='0.0.0.0', port=8080, debug=False)
