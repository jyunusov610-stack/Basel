from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <html>
    <head>
        <title>🐱 Basel Qidiruv</title>
        <style>
            body { font-family: Arial, sans-serif; text-align: center; margin-top: 80px; }
            input[type=text] {
                width: 60%;
                padding: 10px;
                border-radius: 25px;
                border: 1px solid #ccc;
                font-size: 16px;
            }
            button {
                padding: 10px 20px;
                border-radius: 25px;
                border: none;
                background: #4285F4;
                color: white;
                font-size: 16px;
                cursor: pointer;
            }
            button:hover { background: #3367D6; }
            a { display: block; margin-top: 20px; font-size: 18px; text-decoration: none; color: #333; }
            img { margin-top: 30px; border-radius: 20px; }
        </style>
    </head>
    <body>
        <h1>🐱 Basel Qidiruv</h1>
        <form action="/search">
            <input type="text" name="q" placeholder="Basel'da qidiring...">
            <button type="submit">Qidirish</button>
        </form>
        <a href="/ai">🤖 Basel Baqaloq AI</a>
        <br>
        <img src="https://placekitten.com/300/250"/>
    </body>
    </html>
    '''

@app.route('/search')
def search():
    query = request.args.get("q", "")
    if not query:
        return "<p>Hech narsa yozilmadi.</p><a href='/'>Orqaga</a>"
    
    return f"""
    <html>
    <head><title>Natijalar</title></head>
    <body>
        <h2>🔎 Basel natijalari: {query}</h2>
        <iframe src="https://www.google.com/search?q={query}" 
                style="width:100%; height:600px; border:none;"></iframe>
        <br><a href="/">🏠 Bosh sahifa</a>
    </body>
    </html>
    """

@app.route('/ai')
def ai():
    msg = request.args.get("msg", "").lower()
    if not msg:
        return '''
        <h2>🤖 Basel Baqaloq AI</h2>
        <form method="get">
            <input type="text" name="msg" placeholder="Savol yozing..." 
                   style="width:60%; padding:10px; border-radius:10px;"/>
            <button type="submit">Jo'nat</button>
        </form>
        <a href="/">🏠 Bosh sahifa</a>
        '''
    
    # Feyk javoblar
    if "salom" in msg:
        answer = "Qalaysiz, men Baqaloq mushukman 😺"
    elif "qalaysan" in msg:
        answer = "Yaxshiman, ammo qornim ochdi 😼"
    else:
        answer = "Ovqat bersangiz aytaman 😹"

    return f"""
    <h2>Basel Baqaloq javobi</h2>
    <p>{answer}</p>
    <br><a href='/ai'>Orqaga</a> | <a href='/'>Bosh sahifa</a>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
