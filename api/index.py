from flask import Flask, request, render_template_string
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

try:
    from GhostTR import track_ip, track_phone, track_username
except ImportError:
    def track_ip(ip): return f"[Placeholder] IP Tracking for {ip}\nImplement track_ip function from GhostTR.py"
    def track_phone(phone): return f"[Placeholder] Phone Tracking for {phone}\nImplement track_phone function from GhostTR.py"
    def track_username(username): return f"[Placeholder] Username Tracking for {username}\nImplement track_username function from GhostTR.py"

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GhostTrack - OSINT Tool</title>
    <style>
        body {
            background: #000;
            color: #0f0;
            font-family: 'Courier New', Courier, monospace;
            margin: 0;
            padding: 20px;
            line-height: 1.4;
        }
        .container {
            max-width: 900px;
            margin: 0 auto;
        }
        h1 {
            color: #00ff00;
            text-align: center;
            margin-bottom: 10px;
        }
        .warning {
            color: #ff9900;
            text-align: center;
            font-weight: bold;
            margin-bottom: 20px;
        }
        form {
            background: #111;
            padding: 20px;
            border: 1px solid #0f0;
            border-radius: 4px;
            margin-bottom: 20px;
        }
        label {
            color: #0f0;
            display: block;
            margin: 10px 0 5px;
        }
        select, input[type="text"] {
            width: 100%;
            padding: 10px;
            background: #000;
            color: #0f0;
            border: 1px solid #0f0;
            font-family: 'Courier New', monospace;
            font-size: 16px;
            box-sizing: border-box;
        }
        button {
            width: 100%;
            padding: 12px;
            background: #003300;
            color: #0f0;
            border: 1px solid #0f0;
            font-family: 'Courier New', monospace;
            font-size: 16px;
            cursor: pointer;
            margin-top: 10px;
        }
        button:hover {
            background: #004400;
        }
        .result {
            background: #000;
            padding: 15px;
            border: 1px solid #0f0;
            white-space: pre-wrap;
            overflow-x: auto;
            color: #00ff00;
            font-family: 'Courier New', monospace;
        }
        footer {
            text-align: center;
            color: #555;
            margin-top: 30px;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>GhostTrack</h1>
        <p class="warning">For educational and research purposes only. Do not use for illegal activities!</p>

        <form method="POST">
            <label for="tool">Select Tracking Type:</label>
            <select name="tool" id="tool" required>
                <option value="" disabled selected>-- Select one --</option>
                <option value="ip">IP Tracker</option>
                <option value="phone">Phone Number Tracker</option>
                <option value="username">Username Tracker</option>
            </select>

            <label for="target">Target (e.g., 8.8.8.8 / +6281234567890 / nexforgecom):</label>
            <input type="text" name="target" id="target" placeholder="Enter target here..." required>

            <button type="submit">Run Tracking</button>
        </form>

        {% if result %}
        <div class="result">
            <strong>Tracking Result:</strong><br><br>
            {{ result | safe }}
        </div>
        {% endif %}

        <footer>
            Powered by GhostTrack • CLI-inspired Web Version • Deployed on Vercel
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
            result = "Error: Target cannot be empty."
        elif tool == "ip":
            result = track_ip(target)
        elif tool == "phone":
            result = track_phone(target)
        elif tool == "username":
            result = track_username(target)
        else:
            result = "Error: Invalid tool selection."

    return render_template_string(HTML, result=result)

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
