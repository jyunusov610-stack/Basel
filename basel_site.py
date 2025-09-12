from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html lang="uz">
    <head>
        <meta charset="UTF-8">
        <title>Basel</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: linear-gradient(135deg, #f9f9f9, #e3f2fd);
                text-align: center;
                padding: 50px;
            }
            h1 {
                font-size: 48px;
                margin-bottom: 20px;
                color: #1565c0;
            }
            img {
                width: 120px;
                margin-bottom: 20px;
            }
            form {
                margin-top: 20px;
            }
            input[type="text"] {
                width: 60%;
                padding: 12px;
                border-radius: 25px;
                border: 1px solid #90caf9;
                font-size: 16px;
            }
            button {
                padding: 12px 20px;
                margin-left: 10px;
                border: none;
                border-radius: 25px;
                background-color: #1565c0;
                color: white;
                font-size: 16px;
                cursor: pointer;
            }
            button:hover {
                background-color: #0d47a1;
            }
            .link {
                margin-top: 30px;
                display: block;
                font-size: 18px;
                color: #1565c0;
                text-decoration: none;
            }
            .link:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <img src="https://cdn-icons-png.flaticon.com/512/616/616408.png" alt="Mushukcha">
        <h1>🐱 Basel Qidiruv</h1>
        <form action="/search">
            <input type="text" name="q" placeholder="Qidiruv..."/>
            <button type="submit">Qidir</button>
        </form>
        <a href="/ai" class="link">🤖 Basel Baqaloq bilan suhbat</a>
    </body>
    </html>
    '''

@app.route('/search')
def search():
    query = request.args.get("q", "")
    if not query:
        return "<p>Hech narsa yozmadingiz 😅</p><a href='/'>Orqaga</a>"
    return f"""
    <h2>🔎 Basel natija</h2>
    <p>Siz qidirdingiz: <b>{query}</b></p>
    <p><a href='https://www.google.com/search?q={query}' target='_blank'>👉 Google’da ko‘rish</a></p>
    <br><a href='/'>🏠 Bosh sahifa</a>
    """

@app.route('/ai')
def ai():
    msg = request.args.get("msg", "")
    if not msg:
        return '''
        <h2>🤖 Basel Baqaloq AI</h2>
        <form method="get">
            <input type="text" name="msg" placeholder="Savol yozing..." style="width:60%; padding:10px;"/>
            <button type="submit">Jo'nat</button>
        </form>
        <a href="/">🏠 Bosh sahifa</a>
        '''
    return f"<p>Basel Baqaloq javobi: '{msg}' haqida o'ylayapman... 😺</p><br><a href='/ai'>Orqaga</a> | <a href='/'>Bosh sahifa</a>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
