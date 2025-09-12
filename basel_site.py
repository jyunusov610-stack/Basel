from flask import Flask, request, render_template_string, redirect
import random

app = Flask(__name__)

# Juda ko‘p feyk AI javoblari
AI_RESPONSES = {
    "salom": [
        "Salom! Men Baqaloq mushukman 😸",
        "Assalomu alaykum! Qalaysiz?",
        "Salom! Sizni ko‘rib xursandman 😺"
    ],
    "qalaysan": [
        "Yaxshiman, ammo qornim ochdi 🐟",
        "Zo‘rman, sizchi?",
        "Charchadim, lekin gaplashishga tayyorman 😸"
    ],
    "isming nima": [
        "Mening ismim Basel Baqaloq 🤖",
        "Basel Baqaloq mushukman 😺"
    ],
    "nechi yoshsan": [
        "Men hali mushukchaman, lekin aqlliman 🐾",
        "Mening yoshim cheksiz! 😸"
    ],
    "kayfiyat": [
        "Bugun kayfiyatim zo‘r! 🎉",
        "Bir oz charchadim, lekin gaplashsak yaxshilanadi 😺",
        "Menga bir dona baliq olib keling, kayfiyatim ko‘tariladi 🐟"
    ],
    "ovqat": [
        "Menga baliq bering 🐟",
        "Mushukchalar ovqatni yaxshi ko‘radi 😸",
        "Pishloq ham bo‘lsa yomon bo‘lmasdi 🧀"
    ],
    "hazil": [
        "Mushuk kompyuterni nega yaxshi ko‘radi? Chunki sichqon bor 😂",
        "Meni ko‘rsangiz, keyingi safar baliq olib keling 😹",
        "Mushuklar internetni ixtiro qilgan, shuning uchun hamma joyda mushuklar bor! 🐱"
    ],
    "default": [
        "Hmm... bu savol qiyin ekan 🤔",
        "Ovqat bersangiz aytaman 🍗",
        "Men hali kichkina mushukchaman, hamma narsani bilmayman 😿",
        "Bu haqida o‘ylab ko‘raman... 😼",
        "Keyinroq aytaman, hozir ovqat yeyapman 🐟"
    ]
}

# HTML shablon
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Basel</title>
  <style>
    body {
      font-family: 'Poppins', sans-serif;
      background: var(--bg);
      color: var(--text);
      margin: 0; padding: 0;
      text-align: center;
      transition: 0.3s;
    }
    :root {
      --bg: #f9f9f9;
      --text: #222;
      --card: #fff;
    }
    body.dark {
      --bg: #181818;
      --text: #f1f1f1;
      --card: #222;
    }
    header {
      background: linear-gradient(90deg, #4facfe, #00f2fe);
      padding: 20px;
      color: white;
      font-size: 28px;
      font-weight: bold;
    }
    .container {
      max-width: 700px;
      margin: auto;
      padding: 20px;
    }
    .search-box {
      display: flex;
      margin: 20px 0;
    }
    input[type=text] {
      flex: 1;
      padding: 12px;
      border-radius: 10px 0 0 10px;
      border: none;
      font-size: 16px;
    }
    button {
      padding: 12px 20px;
      border: none;
      border-radius: 0 10px 10px 0;
      background: #4facfe;
      color: white;
      font-size: 16px;
      cursor: pointer;
    }
    button:hover {
      background: #00c6ff;
    }
    .chat-box {
      margin-top: 30px;
      text-align: left;
      background: var(--card);
      padding: 20px;
      border-radius: 15px;
      box-shadow: 0 4px 10px rgba(0,0,0,0.1);
      max-height: 400px;
      overflow-y: auto;
    }
    .chat {
      margin: 10px 0;
      padding: 10px;
      border-radius: 10px;
      animation: fade 0.5s ease;
      white-space: pre-line;
    }
    .user { background: #4facfe; color: white; text-align: right; }
    .ai { background: #eee; color: #222; }
    body.dark .ai { background: #333; color: #f1f1f1; }
    .avatar {
      font-size: 30px;
      margin-right: 10px;
    }
    @keyframes fade {
      from {opacity:0;}
      to {opacity:1;}
    }
    .toggle-mode {
      margin: 10px;
      cursor: pointer;
      padding: 8px 15px;
      border-radius: 20px;
      background: #444;
      color: white;
      font-size: 14px;
    }
  </style>
</head>
<body>
  <header>🐱 Basel Search & AI</header>
  <div class="container">
    <!-- Dark mode toggle -->
    <button onclick="toggleMode()" class="toggle-mode">Dark/Light</button>

    <!-- Qidiruv -->
    <form action="/search" method="get" class="search-box">
      <input type="text" name="q" placeholder="Basel’da qidiring..." required>
      <button type="submit">Qidir</button>
    </form>

    <!-- Chat -->
    <div class="chat-box" id="chat-box">
      <div class="chat ai"><span class="avatar">🐱</span>Salom! Men Baqaloq, siz bilan suhbatlashaman.</div>
    </div>
    <form onsubmit="sendMessage(event)">
      <input type="text" id="user-input" placeholder="Savol yozing..." style="width:80%;padding:10px;border-radius:10px;border:1px solid #aaa;">
      <button type="submit">Yubor</button>
    </form>
  </div>

  <script>
    function toggleMode(){
      document.body.classList.toggle("dark");
    }

    function typeEffect(element, text, speed=40) {
      let i = 0;
      function typing() {
        if (i < text.length) {
          element.innerHTML += text.charAt(i);
          i++;
          setTimeout(typing, speed);
        }
      }
      typing();
    }

    function speak(text){
      const utter = new SpeechSynthesisUtterance(text);
      utter.lang = "uz-UZ";
      speechSynthesis.speak(utter);
    }

    function sendMessage(e){
      e.preventDefault();
      let input = document.getElementById("user-input");
      let message = input.value.trim();
      if(!message) return;

      let box = document.getElementById("chat-box");

      // User message
      let userDiv = document.createElement("div");
      userDiv.className = "chat user";
      userDiv.innerText = message;
      box.appendChild(userDiv);

      // AI javobi
      fetch("/chat?q=" + encodeURIComponent(message))
        .then(res => res.text())
        .then(data => {
          let aiDiv = document.createElement("div");
          aiDiv.className = "chat ai";
          aiDiv.innerHTML = "<span class='avatar'>🐱</span>";
          box.appendChild(aiDiv);
          typeEffect(aiDiv, " " + data); // typing effect
          speak(data); // ovoz chiqarish
          box.scrollTop = box.scrollHeight;
        });

      input.value = "";
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
            return random.choice(AI_RESPONSES[key])
    return random.choice(AI_RESPONSES["default"])

if __name__ == "__main__":
    app.run(debug=True)
