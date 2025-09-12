# basel_site.py
# Single-file Flask app with a professional UI + AI chat + AJAX search.
# IMPORTANT: Do NOT hardcode API keys. Set OPENAI_API_KEY, GOOGLE_API_KEY, GOOGLE_CX in environment.

from flask import Flask, request, jsonify, render_template_string, session
import os
import requests
import openai

# App
app = Flask(__name__)
app.secret_key = os.environ.get("BASEL_SECRET", "change_this_in_prod")

# Environment keys (must be set in hosting)
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_CX = os.getenv("GOOGLE_CX")

if OPENAI_KEY:
    openai.api_key = OPENAI_KEY

# Sample fallback search results
SAMPLE_RESULTS = [
    {"title": "Basel — Yangiliklar", "link": "#", "snippet": "Basel — sizning yangi qidiruv va yordamchingiz."},
    {"title": "Python rasmiy sayti", "link": "https://python.org", "snippet": "Python — kuchli va soddadil dasturlash tili."},
    {"title": "Mushuklar haqida maqola", "link": "#", "snippet": "Mushuklar — insonga yaqin va mehribon hayvonlar."}
]

# Small cat SVG logo (inline)
CAT_SVG = """
<svg width="56" height="56" viewBox="0 0 72 72" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <g transform="translate(6,6)">
    <ellipse fill="#FDEBD0" stroke="#5A4031" stroke-width="1.5" cx="30" cy="34" rx="24" ry="18"/>
    <circle fill="#FDEBD0" stroke="#5A4031" stroke-width="1.5" cx="18" cy="18" r="8"/>
    <circle fill="#FDEBD0" stroke="#5A4031" stroke-width="1.5" cx="42" cy="18" r="8"/>
    <circle cx="22" cy="34" r="3" fill="#5A4031"/>
    <circle cx="38" cy="34" r="3" fill="#5A4031"/>
    <path d="M24 42 Q30 46 36 42" stroke="#5A4031" stroke-width="1.6" fill="none" stroke-linecap="round"/>
  </g>
</svg>
"""

# HTML template (Jinja)
BASE_HTML = """
<!doctype html>
<html lang="uz">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>Basel — Qidiruv & AI</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
<style>
  :root{
    --bg1:#f6f9ff; --bg2:#eef7f9; --accent:#0b63d9; --muted:#6b7280;
    --card:#ffffff; --glass:rgba(255,255,255,0.7);
  }
  html,body{height:100%;margin:0;font-family:Inter,system-ui,Segoe UI,Roboto,Arial; background:linear-gradient(135deg,var(--bg1),var(--bg2)); color:#0f172a;}
  .topbar{display:flex;align-items:center;gap:14px;padding:18px 28px;border-bottom:1px solid rgba(15,23,42,0.05);backdrop-filter:blur(6px);position:sticky;top:0;background:linear-gradient(180deg,rgba(255,255,255,0.6),transparent);}
  .brand{display:flex;align-items:center;gap:12px}
  .brand h1{margin:0;font-size:20px}
  .container{max-width:980px;margin:34px auto;padding:0 18px}
  .hero{display:flex;gap:28px;align-items:center;padding:28px;border-radius:16px;background:linear-gradient(180deg, rgba(255,255,255,0.9), rgba(255,255,255,0.82));box-shadow:0 10px 30px rgba(12,15,20,0.06);}
  .searchbox{flex:1}
  .searchbox form{display:flex;gap:10px;align-items:center}
  .search-input{flex:1;padding:14px 18px;border-radius:999px;border:1px solid rgba(15,23,42,0.08);font-size:16px;box-shadow:inset 0 1px 0 rgba(255,255,255,0.6)}
  .search-btn{padding:12px 18px;border-radius:999px;background:var(--accent);color:white;border:0;font-weight:600;cursor:pointer}
  .small{color:var(--muted);font-size:13px}
  .results{margin-top:18px;display:grid;gap:12px}
  .card{background:var(--card);padding:14px;border-radius:12px;box-shadow:0 6px 18px rgba(12,15,20,0.05);border:1px solid rgba(12,15,20,0.02)}
  .result-title{color:#1a0dab;font-weight:600;margin:0}
  .result-link{color:#006621;font-size:13px;margin-top:6px}
  .result-snippet{color:var(--muted);margin-top:8px}
  /* Chat widget */
  .chat-widget{position:fixed;right:18px;bottom:18px;width:360px;max-width:calc(100% - 36px)}
  .chat{background:linear-gradient(180deg,#fff,#fbfdff);border-radius:12px;overflow:hidden;box-shadow:0 12px 36px rgba(2,6,23,0.12)}
  .chat-head{display:flex;gap:10px;align-items:center;padding:10px 12px;border-bottom:1px solid rgba(15,23,42,0.06)}
  .chat-body{height:300px;overflow:auto;padding:12px;background:linear-gradient(180deg, rgba(246,249,255,0.4), rgba(255,255,255,0.4))}
  .chat-input{display:flex;padding:10px;border-top:1px solid rgba(15,23,42,0.03)}
  textarea{flex:1;padding:10px;border-radius:8px;border:1px solid rgba(12,15,20,0.06);resize:none}
  .send-btn{margin-left:8px;padding:8px 12px;border-radius:8px;background:var(--accent);color:#fff;border:0}
  .msg{margin-bottom:8px}
  .msg.user{text-align:right}
  .badge{display:inline-block;padding:6px 10px;border-radius:999px;background:linear-gradient(90deg,#e6f0ff,#e9fff7);color:#0b63d9;font-weight:600}
  footer{margin-top:24px;text-align:center;color:var(--muted);font-size:13px}
  @media(max-width:720px){ .hero{flex-direction:column} .chat-widget{right:12px;left:12px;width:auto} }
</style>
</head>
<body>
  <div class="topbar">
    <div class="brand">
      <div style="width:52px; height:52px;">{{ cat_svg|safe }}</div>
      <div>
        <h1>Basel</h1>
        <div class="small">Sizning shaxsiy qidiruv va AI yordamchingiz</div>
      </div>
    </div>
    <div style="margin-left:auto" class="small">Basel — not Google ✨</div>
  </div>

  <main class="container">
    <div class="hero">
      <div class="searchbox">
        <h2 style="margin:0 0 8px 0">Qidiruv</h2>
        <form id="searchForm" onsubmit="return doSearch();">
          <input id="q" class="search-input" type="text" placeholder="Nimani izlamoqchisiz? (Masalan: futbol, retsept, tarix)" />
          <button class="search-btn" type="submit">Qidir</button>
        </form>
        <div class="small" style="margin-top:8px">Basel Baqaloq bilan suhbat uchun pastdagi chat oynasidan foydalaning.</div>
        <div id="results" class="results" style="margin-top:14px"></div>
      </div>
      <div style="width:260px;text-align:center;">
        <div style="font-size:14px;color:var(--muted);margin-bottom:10px">Basel · Tez va xushbo'y</div>
        <div style="background:linear-gradient(180deg,#ffffff,#f7fbff); padding:14px;border-radius:12px;box-shadow:0 8px 24px rgba(12,15,20,0.06)">
          <div style="width:120px;margin:0 auto">{{ cat_svg|safe }}</div>
          <h3 style="margin:10px 0 4px 0">Basel Baqaloq</h3>
          <p class="small">Yordamchi — savollarga tez javob beradi va maslahatlar beradi.</p>
          <div style="margin-top:10px"><span class="badge">Onlayn</span></div>
        </div>
      </div>
    </div>

    <footer>Made with ❤️ — Basel. Sizga xos shaxsiy qidiruv.</footer>
  </main>

  <!-- Chat widget -->
  <div class="chat-widget">
    <div class="chat">
      <div class="chat-head">
        <div style="width:36px">{{ cat_svg|safe }}</div>
        <div>
          <div style="font-weight:700">Basel Baqaloq</div>
          <div class="small">Sun'iy intellekt yordamchi</div>
        </div>
      </div>
      <div id="chatBody" class="chat-body"><div class="small">Salom — savolingizni yozing!</div></div>
      <div class="chat-input">
        <textarea id="chatText" rows="1" placeholder="Savolingiz... (Enter yuboradi)"></textarea>
        <button id="sendBtn" class="send-btn">Yubor</button>
      </div>
    </div>
  </div>

<script>
async function doSearch(){
  const q = document.getElementById('q').value.trim();
  if(!q) return false;
  const resDiv = document.getElementById('results');
  resDiv.innerHTML = '<div class="card small">Qidirilmoqda...</div>';
  try{
    const r = await fetch('/api/search?q='+encodeURIComponent(q));
    const js = await r.json();
    if(!js.ok){ resDiv.innerHTML = '<div class="card small">Xatolik: '+(js.error||'nomaʼlum')+'</div>'; return false; }
    const hits = js.results;
    if(hits.length===0){ resDiv.innerHTML = '<div class="card small">Hech narsa topilmadi.</div>'; return false; }
    let html = '';
    for(const it of hits){
      html += `<div class="card"><a class="result-title" href="${it.link}" target="_blank">${it.title}</a><div class="result-link">${it.link}</div><div class="result-snippet">${it.snippet||''}</div></div>`;
    }
    resDiv.innerHTML = html;
  }catch(e){
    resDiv.innerHTML = '<div class="card small">Server bilan bogʻlanishda xatolik.</div>';
  }
  return false;
}

// Chat handling
const chatBody = document.getElementById('chatBody');
const chatText = document.getElementById('chatText');
const sendBtn = document.getElementById('sendBtn');

function appendMsg(role, text){
  const d = document.createElement('div');
  d.className = 'msg ' + (role==='user' ? 'user' : 'bot');
  d.innerHTML = `<div style="display:inline-block; max-width:88%; padding:8px 12px; border-radius:12px; background:${role==='user'?'#0b63d9':'#f3f7ff'}; color:${role==='user'?'#fff':'#072b77'}">${text}</div>`;
  chatBody.appendChild(d);
  chatBody.scrollTop = chatBody.scrollHeight;
}

async function sendChat(){
  const text = chatText.value.trim();
  if(!text) return;
  appendMsg('user', text);
  chatText.value='';
  appendMsg('bot', 'Javob kutilyapti...');
  try{
    const r = await fetch('/api/chat', {
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({message:text})
    });
    const js = await r.json();
    // remove the last "waiting" bot message
    chatBody.removeChild(chatBody.lastChild);
    if(js.ok){
      appendMsg('bot', js.reply);
    } else {
      appendMsg('bot', 'Xatolik: ' + (js.error||'nomaʼlum'));
    }
  }catch(e){
    chatBody.removeChild(chatBody.lastChild);
    appendMsg('bot','Serverga ulanib bo\'lmadi.');
  }
}

sendBtn.addEventListener('click', sendChat);
chatText.addEventListener('keydown', function(e){ if(e.key==='Enter' && !e.shiftKey){ e.preventDefault(); sendChat(); } });
</script>
</body>
</html>
"""

# ------------------------------------------------
# API endpoints for search and chat
# ------------------------------------------------
@app.route('/api/search')
def api_search():
    q = (request.args.get('q') or '').strip()
    if not q:
        return jsonify(ok=False, error="Empty query")
    # Try Google Custom Search if configured
    if GOOGLE_API_KEY and GOOGLE_CX:
        try:
            params = {'key': GOOGLE_API_KEY, 'cx': GOOGLE_CX, 'q': q, 'num': 8}
            r = requests.get('https://www.googleapis.com/customsearch/v1', params=params, timeout=8)
            data = r.json()
            items = data.get('items', []) or []
            results = [{'title': it.get('title'), 'link': it.get('link'), 'snippet': it.get('snippet')} for it in items]
            return jsonify(ok=True, results=results)
        except Exception as e:
            # log but fallback
            print("Google CSE error:", e)
    # Fallback: simple local matching
    qlow = q.lower()
    results = [r for r in SAMPLE_RESULTS if qlow in r['title'].lower() or qlow in r['snippet'].lower()]
    if not results:
        results = SAMPLE_RESULTS
    return jsonify(ok=True, results=results)

@app.route('/api/chat', methods=['POST'])
def api_chat():
    data = request.get_json() or {}
    message = (data.get('message') or '').strip()
    if not message:
        return jsonify(ok=False, error="Empty message")
    # Save simple session history (short)
    history = session.get('history', [])
    history.append({'role':'user','content':message})
    session['history'] = history[-12:]
    # If OpenAI key present, call API
    if OPENAI_KEY:
        try:
            resp = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role":"system","content":"Siz 'Basel Baqaloq' — do'stona va foydali yordamchisiz. Javoblarni o'zbek tilida tushunarli qilib yozing."}] + [{'role':m['role'],'content':m['content']} for m in session['history']],
                max_tokens=600,
                temperature=0.6
            )
            reply = resp.choices[0].message['content'].strip()
        except Exception as e:
            print("OpenAI error:", e)
            return jsonify(ok=False, error=str(e))
    else:
        # Fallback canned responses
        ml = message.lower()
        if any(x in ml for x in ['salom','assalomu','hello']):
            reply = "Salom! Men Basel Baqaloq — qanday yordam bera olaman?"
        elif 'qanday' in ml:
            reply = "Yaxshi! Sizga nima bo‘yicha yordam kerak?"
        else:
            reply = "Men hozir oddiy rejimdaman. OpenAI API kaliti o'rnatilgan bo'lsa, aniqroq javob bera olaman."
    history.append({'role':'assistant','content':reply})
    session['history'] = history[-12:]
    return jsonify(ok=True, reply=reply)

# ------------------------------------------------
# Main routes
# ------------------------------------------------
@app.route('/')
def index():
    return render_template_string(BASE_HTML, cat_svg=CAT_SVG)

# Optional pages for direct browse (not strictly required)
@app.route('/ai')
def ai_page():
    # Simple redirect to main page where chat is present
    return render_template_string("<p>Chat widget sahifaga joylangan. <a href='/'>Bosh sahifa</a></p>")

# Run
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
