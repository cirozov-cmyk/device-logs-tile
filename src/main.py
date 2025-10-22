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
        <!-- CSS_START -->
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
        <!-- CSS_END -->
        
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
