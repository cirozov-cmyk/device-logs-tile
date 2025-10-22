from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/')
def index():
    return "Device Logs Tile is running!"

@app.route('/tile')
def tile():
    """Простой endpoint для tile"""
    return jsonify({
        "template": "custom", 
        "data": {
            "title": "Device Logs",
            "content": "<div style='padding:20px;background:#667eea;color:white;border-radius:10px;'><h3>📊 Device Logs</h3><p>✅ Tile is working!</p></div>",
            "refresh_interval": 30
        }
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    print("✅ Starting Flask server...")
    print("📍 Port: 8080")
    print("📍 Endpoints: /tile, /health")
    
    # Явно указываем host и port
    app.run(host='0.0.0.0', port=8080, debug=False, threaded=True)
