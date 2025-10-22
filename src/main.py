from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/')
def index():
    return "Device Logs Tile is running!"

@app.route('/tile')
def tile():
    """Endpoint для iHost tile"""
    print("📨 Request received for /tile endpoint")
    
    return jsonify({
        "template": "custom", 
        "data": {
            "title": "📊 Device Logs",
            "content": """
            <div style="
                padding: 15px; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 10px; 
                color: white; 
                height: 100%;
                font-family: Arial, sans-serif;
            ">
                <h3 style="margin: 0 0 10px 0;">📊 Device Logs</h3>
                <div style="font-size: 12px;">
                    <div>✅ Tile is working!</div>
                    <div>🔄 Real-time monitoring</div>
                    <div>📡 Connected to devices</div>
                </div>
            </div>
            """,
            "refresh_interval": 10
        }
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "service": "device-logs-tile"})

if __name__ == '__main__':
    print("🚀 Starting Device Logs Tile...")
    print("📍 Endpoint /tile should return JSON for iHost")
    app.run(host='0.0.0.0', port=8080, debug=False)
