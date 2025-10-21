import requests
import json
import time
import os

class LogsTile:
    def __init__(self):
        self.config = self.load_config()
        
    def load_config(self):
        with open('/app/config.json', 'r') as f:
            return json.load(f)
    
    def get_logs_data(self):
        # Запрос к нашему Node-RED endpoint
        try:
            response = requests.get(self.config['log_source'], timeout=10)
            return response.text
        except Exception as e:
            return f"Error: {e}"
    
    def format_tile_data(self, logs_text):
        # Форматируем логи для отображения в плитке
        logs_lines = logs_text.strip().split('\n')[-self.config['max_entries']:]
        
        return {
            "template": "custom",
            "data": {
                "title": "Device Logs",
                "content": "\n".join(logs_lines),
                "refresh_interval": self.config['refresh_interval']
            }
        }
    
    def update_tile(self, tile_data):
        # Специфичный метод обновления плитки в iHost
        # Нужно изучить как именно погодная плитка обновляет данные
        print(f"Updating tile with: {json.dumps(tile_data, ensure_ascii=False)}")
        
        # Здесь будет вызов API iHost для обновления плитки
        # Пока просто логируем
        
    def run(self):
        while True:
            try:
                logs_data = self.get_logs_data()
                tile_data = self.format_tile_data(logs_data)
                self.update_tile(tile_data)
                
            except Exception as e:
                print(f"Error: {e}")
            
            time.sleep(self.config['refresh_interval'])

if __name__ == "__main__":
    tile = LogsTile()
    tile.run()
