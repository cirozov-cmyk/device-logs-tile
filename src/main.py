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
        # Простой HTML без сложного CSS
        logs_html = "".join([
            f'<div style="padding:2px 0;border-bottom:1px solid rgba(255,255,255,0.2);font-size:11px;">'
            f'<span style="opacity:0.7;font-size:10px;">{log["timestamp"]}</span> '
            f'{log["message"]}'
            f'</div>'
            for log in logs[:5]
        ])
        
        tile_content = f'''
        <div style="
            padding:12px;
            background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);
            border-radius:10px;
            color:white;
            height:100%;
            font-family:Arial,sans-serif;
        ">
            <h3 style="margin:0 0 8px 0;font-size:14px;">📊 Журналы</h3>
            <div style="max-height:120px;overflow-y:auto;">
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
                "content": f"<div style='padding:15px;color:red'>Ошибка: {str(e)}</div>",
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
    print("✅ Starting simple device logs tile...")
    print("📍 Port: 8080")
    print("📍 Tile endpoint: /tile")
    app.run(host='0.0.0.0', port=8080, debug=False)
