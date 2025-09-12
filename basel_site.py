from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <html>
    <head><title>Basel</title></head>
    <body style="text-align:center; font-family:Arial">
        <h1>🐱 Basel Qidiruv</h1>
        <form action="/search">
            <input type="text" name="q" placeholder="Qidiruv..." style="width:60%; padding:10px;"/>
            <button type="submit">Qidir</button>
        </form>
        <p><a href="/ai">🤖 Basel Baqaloq bilan suhbat</a></p>
    </body>
    </html>
    '''

@app.route('/search')
def search():
    query = request.args.get("q", "")
    if not query:
        return "Hech narsa yozmadingiz 😅"
    return f"<h2>Basel natija:</h2><p>Siz qidirdingiz: <b>{query}</b></p><p><a href='https://www.google.com/search?q={query}'>Google’da ko‘rish</a></p>"

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
        '''
    return f"<p>Basel Baqaloq javobi: '{msg}' haqida o'ylayapman... 😺</p><a href='/ai'>Orqaga</a>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
