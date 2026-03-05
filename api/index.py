from flask import Flask, request, render_template_string
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

try:
    from GhostTR import track_ip, track_phone, track_username
except ImportError:
    def track_ip(ip): return f"Tracking IP {ip} (placeholder - perlu implementasi dari GhostTR.py)"
    def track_phone(phone): return f"Tracking phone {phone} (placeholder)"
    def track_username(username): return f"Tracking username {username} (placeholder)"

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <title>GhostTrack Web</title>
    <style>
        body { font-family: Arial, sans-serif; background: #0d1117; color: #c9d1d9; margin: 0; padding: 20px; }
        h1 { color: #58a6ff; text-align: center; }
        .container { max-width: 800px; margin: 0 auto; }
        .warning { color: #ffa657; text-align: center; font-weight: bold; }
        form { background: #161b22; padding: 20px; border-radius: 8px; margin: 20px 0; border: 1px solid #30363d; }
        select, input[type="text"], button { padding: 12px; margin: 10px 0; font-size: 16px; width: 100%; box-sizing: border-box; border-radius: 6px; border: 1px solid #30363d; background: #0d1117; color: #c9d1d9; }
        button { background: #238636; color: white; border: none; cursor: pointer; }
        button:hover { background: #2ea043; }
        pre { background: #0d1117; padding: 15px; border: 1px solid #30363d; border-radius: 6px; white-space: pre-wrap; overflow-x: auto; color: #c9d1d9; }
    </style>
</head>
<body>
    <div class="container">
        <h1>GhostTrack Web</h1>
        <p class="warning">Untuk tujuan edukasi saja. Jangan disalahgunakan!</p>

        <form method="POST">
            <select name="tool">
                <option value="ip">IP Tracker</option>
                <option value="phone">Phone Tracker</option>
                <option value="username">Username Tracker</option>
            </select>
            <input type="text" name="target" placeholder="Masukkan target (IP / nomor telepon / username)" required>
            <button type="submit">Track</button>
        </form>

        {% if result %}
        <h3>Hasil:</h3>
        <pre>{{ result }}</pre>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    if request.method == "POST":
        tool = request.form.get("tool")
        target = request.form.get("target", "").strip()

        if tool == "ip":
            result = track_ip(target)
        elif tool == "phone":
            result = track_phone(target)
        elif tool == "username":
            result = track_username(target)
        else:
            result = "Pilihan tidak valid."

    return render_template_string(HTML, result=result)
