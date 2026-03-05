from flask import Flask, request, render_template_string
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

try:
    from GhostTR import track_ip, track_phone, track_username
except ImportError:
    def track_ip(ip): return f"[Placeholder] Tracking IP: {ip}\nImplementasikan fungsi track_ip di GhostTR.py"
    def track_phone(phone): return f"[Placeholder] Tracking Phone: {phone}\nImplementasikan fungsi track_phone di GhostTR.py"
    def track_username(username): return f"[Placeholder] Tracking Username: {username}\nImplementasikan fungsi track_username di GhostTR.py"

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GhostTrack Web</title>
    <style>
        :root {
            --bg: #0d1117;
            --text: #c9d1d9;
            --accent: #58a6ff;
            --accent-hover: #79c0ff;
            --card: #161b22;
            --border: #30363d;
            --warning: #ffa657;
            --success: #238636;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: var(--bg);
            color: var(--text);
            margin: 0;
            padding: 20px;
            line-height: 1.6;
        }
        .container {
            max-width: 900px;
            margin: 0 auto;
        }
        h1 {
            color: var(--accent);
            text-align: center;
            margin-bottom: 10px;
        }
        .warning {
            color: var(--warning);
            text-align: center;
            font-weight: bold;
            margin-bottom: 30px;
        }
        form {
            background: var(--card);
            padding: 25px;
            border-radius: 12px;
            border: 1px solid var(--border);
            margin-bottom: 30px;
        }
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
        }
        select, input[type="text"] {
            width: 100%;
            padding: 12px;
            margin-bottom: 15px;
            background: var(--bg);
            color: var(--text);
            border: 1px solid var(--border);
            border-radius: 6px;
            font-size: 16px;
            box-sizing: border-box;
        }
        button {
            width: 100%;
            padding: 14px;
            background: var(--success);
            color: white;
            border: none;
            border-radius: 6px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: background 0.2s;
        }
        button:hover {
            background: #2ea043;
        }
        .result {
            background: var(--card);
            padding: 20px;
            border-radius: 12px;
            border: 1px solid var(--border);
            white-space: pre-wrap;
            overflow-x: auto;
            font-family: 'Courier New', monospace;
        }
        footer {
            text-align: center;
            margin-top: 40px;
            color: #8b949e;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>GhostTrack Web</h1>
        <p class="warning">Untuk tujuan edukasi dan penelitian saja. Jangan digunakan untuk aktivitas ilegal!</p>

        <form method="POST">
            <label for="tool">Pilih Jenis Tracking:</label>
            <select name="tool" id="tool" required>
                <option value="" disabled selected>-- Pilih satu --</option>
                <option value="ip">IP Address Tracker</option>
                <option value="phone">Nomor Telepon Tracker</option>
                <option value="username">Username/Sosmed Tracker</option>
            </select>

            <label for="target">Target (contoh: 8.8.8.8 / +6281234567890 / nexforgecom):</label>
            <input type="text" name="target" id="target" placeholder="Masukkan target di sini..." required>

            <button type="submit">Jalankan Tracking</button>
        </form>

        {% if result %}
        <div class="result">
            <strong>Hasil Tracking:</strong><br><br>
            {{ result | safe }}
        </div>
        {% endif %}

        <footer>
            Powered by GhostTrack • Deployed on Vercel • 2026
        </footer>
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

        if not target:
            result = "Error: Target tidak boleh kosong."
        elif tool == "ip":
            result = track_ip(target)
        elif tool == "phone":
            result = track_phone(target)
        elif tool == "username":
            result = track_username(target)
        else:
            result = "Error: Pilihan tool tidak valid."

    return render_template_string(HTML, result=result)

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
