from flask import Flask, request, render_template_string, redirect, jsonify
import random

app = Flask(__name__)

# Feyk AI javoblari (o‘zbekcha + inglizcha)
AI_RESPONSES = {
    "salom": [
        ("Salom! Men Baqaloq mushukman 😸", "Hello! I am Baqaloq the cat 😸"),
        ("Assalomu alaykum! Qalaysiz?", "Peace be upon you! How are you?"),
        ("Salom! Sizni ko‘rib xursandman 😺", "Hi! I’m happy to see you 😺")
    ],
    "qalaysan": [
        ("Yaxshiman, ammo qornim ochdi 🐟", "I’m fine, but I’m hungry 🐟"),
        ("Zo‘rman, sizchi?", "I’m great, how about you?"),
        ("Charchadim, lekin gaplashishga tayyorman 😸", "I’m tired, but ready to chat 😸")
    ],
    "isming nima": [
        ("Mening ismim Basel Baqaloq 🤖", "My name is Basel Baqaloq 🤖"),
        ("Basel Baqaloq mushukman 😺", "I’m Basel Baqaloq the cat 😺")
    ],
    "nechi yoshsan": [
        ("Men hali mushukchaman, lekin aqlliman 🐾", "I’m still a kitten, but very smart 🐾"),
        ("Mening yoshim cheksiz! 😸", "My age is infinite! 😸")
    ],
    "kayfiyat": [
        ("Bugun kayfiyatim zo‘r! 🎉", "My mood is great today! 🎉"),
        ("Bir oz charchadim, lekin gaplashsak yaxshilanadi 😺", "I’m a bit tired, but chatting will cheer me up 😺"),
        ("Menga baliq olib keling, kayfiyatim ko‘tariladi 🐟", "Bring me a fish, and my mood will get better 🐟")
    ],
    "ovqat": [
        ("Menga baliq bering 🐟", "Give me fish 🐟"),
        ("Mushukchalar ovqatni yaxshi ko‘radi 😸", "Kittens love food 😸"),
        ("Pishloq ham bo‘lsa yomon bo‘lmasdi 🧀", "Cheese wouldn’t be bad either 🧀")
    ],
    "hazil": [
        ("Mushuk kompyuterni nega yaxshi ko‘radi? Chunki sichqon bor 😂", "Why do cats love computers? Because they have a mouse 😂"),
        ("Meni ko‘rsangiz, keyingi safar baliq olib keling 😹", "Next time you see me, bring a fish 😹"),
        ("Mushuklar internetni ixtiro qilgan! 🐱", "Cats invented the internet! 🐱")
    ],
    "default": [
        ("Hmm... bu savol qiyin ekan 🤔", "Hmm... that’s a tough question 🤔"),
        ("Ovqat bersangiz aytaman 🍗", "I’ll tell you if you give me food 🍗"),
        ("Men hali mushukchaman, hamma narsani bilmayman 😿", "I’m still a kitten, I don’t know everything 😿"),
        ("Bu haqida o‘ylab ko‘raman... 😼", "I’ll think about it... 😼"),
        ("Keyinroq aytaman, hozir ovqat yeyapman 🐟", "I’ll tell you later, I’m eating now 🐟")
    ]
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="uz">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Basel</title>
<style>
body {font-family: 'Poppins', sans-serif; background: var(--bg); color: var(--text); margin:0; padding:0; text-align:center; transition:0.3s;}
:root{--bg:#f9f9f9;--text:#222;--card:#fff;}
body.dark{--bg:#181818;--text:#f1f1f1;--card:#222;}
header{background:linear-gradient(90deg,#4facfe,#00f2fe);padding:20px;color:white;font-size:28px;font-weight:bold;}
.container{max-width:700px;margin:auto;padding:20px;}
.search-box{display:flex;margin:20px 0;}
input[type=text]{flex:1;padding:12px;border-radius:10px 0 0 10px;border:none;font-size:16px;}
button{padding:12px 20px;border:none;border-radius:0 10px 10px 0;background:#4facfe;color:white;font-size:16px;cursor:pointer;}
button:hover{background:#00c6ff;}
.chat-box{margin-top:30px;text-align:left;background:var(--card);padding:20px;border-radius:15px;box-shadow:0 4px 10px rgba(0,0,0,0.1);max-height:400px;overflow-y:auto;}
.chat{margin:10px 0;padding:10px;border-radius:10px;animation:fade 0.5s ease;white-space:pre-line;}
.user{background:#4facfe;color:white;text-align:right;}
.ai{background:#eee;color:#222;}
body.dark .ai{background:#333;color:#f1f1f1;}
.avatar{font-size:30px;margin-right:10px;}
@keyframes fade{from{opacity:0;}to{opacity:1;}}
.toggle-mode{margin:10px;cursor:pointer;padding:8px 15px;border-radius:20px;background:#444;color:white;font-size:14px;}

/* --- RESPONSIVE --- */
@media only screen and (max-width: 768px) {
    header {font-size:24px; padding:15px;}
    input[type=text]{font-size:14px;padding:10px;}
    button{font-size:14px;padding:10px;}
    .chat-box{padding:15px; max-height:300px;}
    .chat{font-size:14px;padding:8px;}
}
@media only screen and (max-width: 480px) {
    header {font-size:20px; padding:12px;}
    input[type=text]{font-size:13px;padding:8px;}
    button{font-size:13px;padding:8px;}
    .chat-box{padding:10px; max-height:250px;}
    .chat{font-size:12px;padding:6px;}
}
</style>
</head>
<body>
<header>🐱 Basel Search & AI</header>
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
</div>

<script>
function toggleMode(){document.body.classList.toggle("dark");}

function typeEffect(element,text,speed=40){let i=0;function typing(){if(i<text.length){element.innerHTML+=text.charAt(i);i++;setTimeout(typing,speed);}}typing();}

function speak(uzText,enText){
let voices = speechSynthesis.getVoices();
let uzVoice = voices.find(v=>v.lang.startsWith("uz") && v.name.toLowerCase().includes("male"));
let enVoice = voices.find(v=>v.lang.startsWith("en") && v.name.toLowerCase().includes("male"));
let uz = new SpeechSynthesisUtterance(uzText); uz.lang="uz-UZ"; if(uzVoice) uz.voice=uzVoice;
let en = new SpeechSynthesisUtterance(enText); en.lang="en-US"; if(enVoice) en.voice=enVoice;
speechSynthesis.speak(uz); speechSynthesis.speak(en);
}

function sendMessage(e){
e.preventDefault();
let input=document.getElementById("user-input");
let message=input.value.trim(); if(!message) return;
let box=document.getElementById("chat-box");
let userDiv=document.createElement("div"); userDiv.className="chat user"; userDiv.innerText=message; box.appendChild(userDiv);
fetch("/chat?q="+encodeURIComponent(message)).then(res=>res.json()).then(data=>{
let aiDiv=document.createElement("div"); aiDiv.className="chat ai"; aiDiv.innerHTML="<span class='avatar'>🐱</span>"; box.appendChild(aiDiv);
typeEffect(aiDiv," "+data.uz);
speak(data.uz,data.en);
box.scrollTop=box.scrollHeight;});
input.value="";
}
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route("/search")
def search():
    query = request.args.get("q")
    if not query:
        return redirect("/")
    return redirect(f"https://www.google.com/search?q={query}")

@app.route("/chat")
def chat():
    user_msg = request.args.get("q", "").lower()
    for key in AI_RESPONSES:
        if key in user_msg:
            uz,en = random.choice(AI_RESPONSES[key])
            return jsonify({"uz":uz,"en":en})
    uz,en = random.choice(AI_RESPONSES["default"])
    return jsonify({"uz":uz,"en":en})

if __name__ == "__main__":
    app.run(debug=True)
