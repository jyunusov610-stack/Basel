from flask import Flask, request
import openai

app = Flask(name)

# 🔑 OpenAI API kalitingizni shu yerga yozasiz
openai.api_key = "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"

@app.route('/')
def home():
    return '''
    <h1>🐱 Basel Qidiruv</h1>
    <form action="/search">
        <input type="text" name="q" placeholder="Basel'da qidiring..." style="width:60%; padding:10px;">
        <button type="submit">Qidirish</button>
    </form>
    <br>
    <a href="/ai">🤖 Basel Baqaloq AI</a>
    <br><br>
    <img src="https://placekitten.com/250/250"/>
    '''

@app.route('/search')
def search():
    query = request.args.get("q", "")
    if not query:
        return "<p>Hech narsa yozilmadi.</p><a href='/'>Orqaga</a>"
    
    # Shunchaki Google linkiga yuborish o‘rniga Basel ichida chiqaramiz
    return f"""
    <h2>🔎 Basel natijalari:</h2>
    <p>Hozircha faqat Google'dan foydalanmoqda, keyinchalik o‘zimiznikini qo‘shamiz 😉</p>
    <iframe src="https://www.google.com/search?q={query}" style="width:100%; height:600px;"></iframe>
    <br><a href="/">🏠 Bosh sahifa</a>
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
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": msg}],
            max_tokens=500,
            temperature=0.7
        )
        answer = response.choices[0].message["content"].strip()
    except Exception as e:
        answer = f"Xatolik yuz berdi: {str(e)}"

    return f"<h2>Basel Baqaloq javobi</h2><p>{answer}</p><br><a href='/ai'>Orqaga</a> | <a href='/'>Bosh sahifa</a>"

if name == "main":
    app.run(host="0.0.0.0", port=5000)
