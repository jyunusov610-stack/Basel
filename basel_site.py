# basel_site.py
from flask import Flask, request, render_template_string, redirect, jsonify
import random

app = Flask(__name__)

# =======================
# Feyk AI javoblari (o'zbekcha + inglizcha)
# =======================
AI_RESPONSES = {
    "salom":[
        ("Salom! Men Baqaloq mushukman 😸","Hello! I am Baqaloq the cat 😸"),
        ("Assalomu alaykum! Qalaysiz?","Peace be upon you! How are you?")
    ],
    "qalaysan":[
        ("Yaxshiman, ammo qornim ochdi 🐟","I’m fine, but I’m hungry 🐟"),
        ("Zo‘rman, sizchi?","I’m great, how about you?")
    ],
    "hazil":[
        ("Mushuk kompyuterni nega yaxshi ko‘radi? Chunki sichqon bor 😂","Why do cats love computers? Because they have a mouse 😂"),
        ("Keyingi safar baliq olib keling 😹","Next time you see me, bring a fish 😹")
    ],
    "ovqat":[
        ("Menga baliq bering 🐟","Give me fish 🐟"),
        ("Pishloq ham yomon bo‘lmasdi 🧀","Cheese wouldn’t be bad either 🧀")
    ],
    "fact":[
        ("Mushuklar internetni ixtiro qilgan! 🐱","Cats invented the internet! 🐱"),
        ("Mushuklar uyquda ham ishlashadi 😼","Cats work even while sleeping 😼")
    ],
    "default":[
        ("Hmm... bu savol qiyin ekan 🤔","Hmm... that’s a tough question 🤔"),
        ("Ovqat bersangiz aytaman 🍗","I’ll tell you if you give me food 🍗"),
        ("Men hali mushukchaman 😿","I’m still a kitten 😿")
    ]
}

# =======================
# HTML & CSS Template
# =======================
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="uz">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Basel Interactive</title>
<style>
body {font-family:'Poppins',sans-serif; background:var(--bg); color:var(--text); margin:0; padding:0; text-align:center; transition:0.3s;}
:root{--bg:#f9f9f9;--text:#222;--card:#fff;}
body.dark{--bg:#181818;--text:#f1f1f1;--card:#222;}
header{background:linear-gradient(90deg,#4facfe,#00f2fe);padding:20px;color:white;font-size:28px;font-weight:bold;}
.container{max-width:700px;margin:auto;padding:20px;}
.search-box{display:flex;margin:20px 0;}
input[type=text]{flex:1;padding:12px;border-radius:10px 0 0 10px;border:none;font-size:16px;}
button{padding:12px 20px;border:none;border-radius:0 10px 10px 0;background:#4facfe;color:white;font-size:16px;cursor:pointer;}
button:hover{background:#00c6ff;}
.chat-box{margin-top:30px;text-align:left;background:var(--card);padding:20px;border-radius:15px;box-shadow:0 4px 10px rgba(0,0,0,0.1);max-height:400px;overflow-y:auto;}
.chat{margin:10px 0;padding:10px;border-radius:10px;animation:fade 0.5s ease;white-space:pre-line; background:linear-gradient(120deg,#e0e0e0,#ffffff);}
.user{background:linear-gradient(120deg,#4facfe,#00f2fe); color:white; text-align:right;}
.ai{background:linear-gradient(120deg,#ffe0b2,#fff3e0);}
body.dark .ai{background:linear-gradient(120deg,#333,#444); color:#f1f1f1;}
.avatar{font-size:30px;margin-right:10px;}
@keyframes fade{from{opacity:0;}to{opacity:1;}}
.toggle-mode{margin:10px;cursor:pointer;padding:8px 15px;border-radius:20px;background:#444;color:white;font-size:14px;}
.emoji-btn{cursor:pointer;margin:0 5px;font-size:20px;}
/* RESPONSIVE */
@media only screen and (max-width:768px){header{font-size:24px;padding:15px;}input[type=text]{font-size:14px;padding:10px;}button{font-size:14px;padding:10px;}.chat-box{padding:15px; max-height:300px;}.chat{font-size:14px;padding:8px;}}
@media only screen and (max-width:480px){header{font-size:20px;padding:12px;}input[type=text]{font-size:13px;padding:8px;}button{font-size:13px;padding:8px;}.chat-box{padding:10px; max-height:250px;}.chat{font-size:12px;padding:6px;}}
</style>
</head>
<body>
<header>🐱 Basel Interactive</header>
<div class="container">
<button onclick="toggleMode()" class="toggle-mode">Dark/Light</button>
<form action="/search" method="get" class="search-box">
<input type="text" name="q" placeholder="Basel’da qidiring..." required>
<button type="submit">Qidir</button>
</form>

<div class="chat-box" id="chat-box">
<div class="chat ai"><span class="avatar">🐱</span>Salom! Men Baqaloq, siz bilan suhbatlashaman.</div>
</div>

<form onsubmit="sendMessage(event)">
<input type="text" id="user-input" placeholder="Savol yozing..." style="width:80%;padding:10px;border-radius:10px;border:1px solid #aaa;">
<button type="submit">Yubor</button>
</form>
<div style="margin-top:10px;">
<button class="emoji-btn" onclick="sendQuick('ovqat')">🐟 Ovqat ber</button>
<button class="emoji-btn" onclick="sendQuick('hazil')">😂 Hazil qil</button>
<button class="emoji-btn" onclick="sendQuick('fact')">ℹ️ Fakt</button>
</div>

</div>

<script>
// Dark/Light toggle
function toggleMode(){document.body.classList.toggle("dark");}

// Type effect
function typeEffect(el,text,speed=40){let i=0;function t(){if(i<text.length){el.innerHTML+=text.charAt(i);i++;setTimeout(t,speed);}}t();}

// Speech synthesis
function speak(uz,en){
 let voices=speechSynthesis.getVoices();
 let uzv=voices.find(v=>v.lang.startsWith("uz")&&v.name.toLowerCase().includes("male"));
 let env=voices.find(v=>v.lang.startsWith("en")&&v.name.toLowerCase().includes("male"));
 let u=new SpeechSynthesisUtterance(uz); u.lang="uz-UZ"; if(uzv) u.voice=uzv;
 let e=new SpeechSynthesisUtterance(en); e.lang="en-US"; if(env) e.voice=env;
 speechSynthesis.speak(u); speechSynthesis.speak(e);
}

// Append message to chat
function appendMessage(text,className){
 let box=document.getElementById("chat-box");
 let div=document.createElement("div");
 div.className="chat "+className;
 div.innerHTML="<span class='avatar'>🐱</span>"+text;
 box.appendChild(div); box.scrollTop=box.scrollHeight;
}

// Send chat message
function sendMessage(e){
 e.preventDefault();
 let input=document.getElementById("user-input"); let msg=input.value.trim();
 if(!msg) return;
 appendMessage(msg,"user");
 fetch("/chat?q="+encodeURIComponent(msg)).then(res=>res.json()).then(data=>{
   let aiDiv=document.createElement("div"); aiDiv.className="chat ai"; aiDiv.innerHTML="<span class='avatar'>🐱</span>"; document.getElementById("chat-box").appendChild(aiDiv);
   typeEffect(aiDiv," "+data.uz);
   speak(data.uz,data.en);
   document.getElementById("chat-box").scrollTop=document.getElementById("chat-box").scrollHeight;
 });
 input.value="";
}

// Quick buttons
function sendQuick(key){appendMessage(key,"user"); fetch("/chat?q="+encodeURIComponent(key)).then(res=>res.json()).then(data=>{
   let aiDiv=document.createElement("div"); aiDiv.className="chat ai"; aiDiv.innerHTML="<span class='avatar'>🐱</span>"; document.getElementById("chat-box").appendChild(aiDiv);
   typeEffect(aiDiv," "+data.uz); speak(data.uz,data.en);
 });}
</script>
</body>
</html>
"""

# =======================
# Flask routes
# =======================
@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route("/search")
def search():
    query=request.args.get("q")
    if not query:
        return redirect("/")
    return redirect(f"https://www.google.com/search?q={query}")

@app.route("/chat")
def chat():
    user_msg=request.args.get("q","").lower()
    for key in AI_RESPONSES:
        if key in user_msg:
            uz,en=random.choice(AI_RESPONSES[key])
            return jsonify({"uz":uz,"en":en})
    uz,en=random.choice(AI_RESPONSES["default"])
    return jsonify({"uz":uz,"en":en})

if __name__=="__main__":
    app.run(debug=True)
