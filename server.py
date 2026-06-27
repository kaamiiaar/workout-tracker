#!/usr/bin/env python3
"""
Simple local server for Workout Tracker app with video streaming support.
Run: python3 server.py
Then open: http://localhost:8081
"""

import json
import os
import re
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, 'workout-db.json')

# Ensure static files are always served from this project folder,
# even if the server is started from Spotlight or another cwd.
os.chdir(BASE_DIR)

class WorkoutHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        
        # API endpoint to load data
        if parsed.path == '/api/load':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            if os.path.exists(DB_FILE):
                with open(DB_FILE, 'r') as f:
                    self.wfile.write(f.read().encode())
            else:
                # Return empty initial data
                self.wfile.write(json.dumps({
                    'completions': [],
                    'settings': {'darkMode': False, 'lastCompleted': 0}
                }).encode())
            return
        
        # Handle video files with Range request support for seeking
        if parsed.path.endswith('.mp4'):
            file_path = self.translate_path(parsed.path)
            if os.path.exists(file_path):
                return self.send_video_range(file_path)
        
        # Serve static files normally
        return SimpleHTTPRequestHandler.do_GET(self)
    
    def send_video_range(self, file_path):
        """Handle HTTP Range requests for video streaming with seek support."""
        file_size = os.path.getsize(file_path)
        range_header = self.headers.get('Range')
        
        if range_header:
            # Parse Range header (e.g., "bytes=0-1023")
            match = re.search(r'bytes=(\d+)-(\d*)', range_header)
            if match:
                start = int(match.group(1))
                end = int(match.group(2)) if match.group(2) else file_size - 1
                end = min(end, file_size - 1)
                length = end - start + 1
                
                self.send_response(206)  # Partial Content
                self.send_header('Content-Type', 'video/mp4')
                self.send_header('Content-Range', f'bytes {start}-{end}/{file_size}')
                self.send_header('Content-Length', str(length))
                self.send_header('Accept-Ranges', 'bytes')
                self.end_headers()
                
                with open(file_path, 'rb') as f:
                    f.seek(start)
                    self.wfile.write(f.read(length))
                return
        
        # No range request - send entire file
        self.send_response(200)
        self.send_header('Content-Type', 'video/mp4')
        self.send_header('Content-Length', str(file_size))
        self.send_header('Accept-Ranges', 'bytes')
        self.end_headers()
        
        with open(file_path, 'rb') as f:
            self.wfile.write(f.read())
    
    def do_POST(self):
        parsed = urlparse(self.path)
        
        # API endpoint to save data
        if parsed.path == '/api/save':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode())
                with open(DB_FILE, 'w') as f:
                    json.dump(data, f, indent=2)
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'success': True}).encode())
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode())
            return
        
        self.send_response(404)
        self.end_headers()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

if __name__ == '__main__':
    PORT = 8081
    server = HTTPServer(('localhost', PORT), WorkoutHandler)
    print(f'💪 Workout Tracker server running at http://localhost:{PORT}')
    print(f'📂 Serving files from: {BASE_DIR}')
    print(f'📁 Data will be saved to: {DB_FILE}')
    print('Press Ctrl+C to stop')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\n👋 Server stopped')
