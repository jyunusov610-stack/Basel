from flask import Flask, request
import openai
import os

app = Flask(__name__)

# 🔑 OpenAI API kalitini Render yoki kompyuterdan olish
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html lang="uz">
    <head>
        <meta charset="UTF-8">
        <title>Basel</title>
        <style>
            body { font-family: Arial, sans-serif; text-align: center; padding: 50px; background: #f0f4f8; }
            h1 { color: #1565c0; }
            input[type="text"] { width: 60%; padding: 12px; border-radius: 25px; border: 1px solid #90caf9; }
            button { padding: 12px 20px; border-radius: 25px; background: #1565c0; color: white; border: none; }
            button:hover { background: #0d47a1; }
            a { text-decoration: none; color: #1565c0; }
        </style>
    </head>
    <body>
        <h1>🐱 Basel Qidiruv</h1>
        <form action="/search">
            <input type="text" name="q" placeholder="Qidiruv..."/>
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
    
    try:
        # 🔥 AI so‘rov yuborish
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": msg}],
            max_tokens=500,
            temperature=0.7
        )
        answer = response.choices[0].message["content"].strip()
    except Exception as e:
        answer = f"Xatolik yuz berdi: {str(e)}"

    return f"""
    <h2>Basel Baqaloq javobi</h2>
    <p>{answer}</p>
    <br><a href='/ai'>Orqaga</a> | <a href='/'>Bosh sahifa</a>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
