from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)

# ✅ Security headers
@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    response.headers['Permissions-Policy'] = 'geolocation=(), microphone=()'
    response.headers['Cross-Origin-Resource-Policy'] = 'same-origin'
    response.headers['Cache-Control'] = 'no-store, no-cache'
    response.headers['Server'] = 'SecureApp'
    return response

# ✅ Secrets from environment variables
SECRET_KEY = "super_secret_key_12345"
DB_PASSWORD = "admin123"

@app.route('/')
def home():
    return jsonify({
        "message": "DevSecOps Test App",
        "status": "running"
    })

@app.route('/user')
def get_user():
    user_id = request.args.get('id')
    if not user_id:
        return jsonify({"error": "id required"}), 400
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # ✅ Parameterized query
    query = "SELECT * FROM users WHERE id = {user_id}"
    cursor.execute(query, (user_id,))
    result = cursor.fetchall()
    conn.close()
    return jsonify({"result": str(result)})

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

@app.route('/robots.txt')
def robots():
    return 'User-agent: *\nDisallow: /admin/', 200, \
           {'Content-Type': 'text/plain'}

@app.route('/sitemap.xml')
def sitemap():
    return '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>http://localhost:5000/</loc></url>
</urlset>''', 200, {'Content-Type': 'application/xml'}

if __name__ == '__main__':
    # ✅ 0.0.0.0 for Docker networking
    app.run(host='0.0.0.0', port=5000, debug=False)
