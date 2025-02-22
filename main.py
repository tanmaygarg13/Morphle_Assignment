from flask import Flask, render_template_string
import os
import subprocess

app = Flask(__name__)

@app.route('/htop')
def htop_endpoint():
    try:
        username = os.getlogin()
    except Exception:
        username = os.environ.get("USER", "Unknown")

    try:
        htop_output = subprocess.check_output(
            ["top", "-b", "-n", "1"],
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )

    except Exception as e:
        htop_output = f"Error running htop: {e}"

    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Htop Endpoint</title>
    </head>
    <body>
        <p>Name: Tanmay Garg</p>
        <p>user: {{ username }}</p>
        <p>Local Time: <span id="localTime"></span></p>
        <pre>{{ htop_output }}</pre>
        <script>
            // When the document loads, calculate local time in ISO-like format.
            document.addEventListener("DOMContentLoaded", function() {
                var now = new Date();
                var isoLocal = now.getFullYear() + '-' +
                               ('0' + (now.getMonth() + 1)).slice(-2) + '-' +
                               ('0' + now.getDate()).slice(-2) + 'T' +
                               ('0' + now.getHours()).slice(-2) + ':' +
                               ('0' + now.getMinutes()).slice(-2) + ':' +
                               ('0' + now.getSeconds()).slice(-2);
                document.getElementById("localTime").textContent = isoLocal;
            });
        </script>
    </body>
    </html>
    """
    return render_template_string(html_template, username=username, htop_output=htop_output)

if __name__ == '__main__':
    app.run(debug=True)
