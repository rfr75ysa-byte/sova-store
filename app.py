
from flask import Flask, request, redirect, url_for, session, render_template_string, flash
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get(
    "SOVA_SECRET_KEY",
    "SOVA-change-this-secret-before-publishing"
)

WHATSAPP = "9647806364447"
DB_NAME = "sova_users.db"


def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            )
        """)


init_db()


STYLE = """
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&family=Playfair+Display:wght@500;700&display=swap');

* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
    margin: 0;
    background: #061629;
    color: #f5f8ff;
    font-family: Cairo, sans-serif;
}
a { color: inherit; text-decoration: none; }
button, input { font: inherit; }

header {
    position: sticky;
    top: 0;
    z-index: 10;
    background: #071d35ee;
    backdrop-filter: blur(12px);
    border-bottom: 1px solid #35b8ff33;
}
.nav {
    max-width: 1200px;
    margin: auto;
    padding: 15px 22px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 15px;
    flex-wrap: wrap;
}
.logo {
    font: 700 32px 'Playfair Display', serif;
    letter-spacing: 5px;
    color: #35b8ff;
}
.links {
    display: flex;
    gap: 15px;
    align-items: center;
    flex-wrap: wrap;
}
.links a:hover { color: #35b8ff; }

.pill, .btn {
    display: inline-block;
    padding: 10px 18px;
    border-radius: 25px;
    cursor: pointer;
}
.pill {
    border: 1px solid #35b8ff88;
    color: #35b8ff;
}
.btn {
    border: none;
    background: linear-gradient(110deg, #35b8ff, #9be7ff);
    color: #031827;
    font-weight: 800;
}
.btn:hover { filter: brightness(1.1); }
.secondary {
    background: transparent;
    color: white;
    border: 1px solid #35b8ff88;
}

.ocean {
    position: relative;
    isolation: isolate;
    overflow: hidden;
    background:
        radial-gradient(ellipse at 50% 0%, #145274, transparent 65%),
        linear-gradient(180deg, #082e48, #041827);
}
.ocean::before {
    content: "";
    position: absolute;
    z-index: -1;
    inset: -30%;
    background: repeating-conic-gradient(
        from 195deg at 50% 0%,
        transparent 0deg,
        transparent 10deg,
        #5bd4ff0b 12deg,
        transparent 17deg
    );
    animation: rays 20s linear infinite alternate;
}
@keyframes rays {
    from { transform: rotate(-8deg); }
    to { transform: rotate(8deg); }
}
.bubbles {
    position: absolute;
    inset: 0;
    overflow: hidden;
    pointer-events: none;
    z-index: -1;
}
.bubble {
    position: absolute;
    bottom: -60px;
    border: 1px solid #9eeaff77;
    border-radius: 50%;
    background: #c8f5ff0b;
    animation: rise linear infinite;
}
@keyframes rise {
    to { transform: translateY(-110vh); opacity: 0; }
}
.hero {
    min-height: 480px;
    padding: 80px 20px;
    display: grid;
    place-items: center;
    text-align: center;
}
.eyebrow {
    color: #35b8ff;
    letter-spacing: 5px;
    font-size: 13px;
}
.hero h1 {
    font: 700 clamp(60px, 11vw, 110px) 'Playfair Display', serif;
    letter-spacing: 8px;
    margin: 12px 0;
    text-shadow: 0 0 35px #35b8ff55;
}
.hero p { font-size: 21px; }

section {
    max-width: 1200px;
    margin: auto;
    padding: 65px 22px;
}
.section-head {
    text-align: center;
    margin-bottom: 32px;
}
.section-head small {
    color: #35b8ff;
    letter-spacing: 3px;
}
.section-head h2 { font-size: 30px; }
.section-head p, .about { color: #b6cad7; }
.about {
    max-width: 800px;
    margin: auto;
    text-align: center;
    line-height: 2;
}
.products {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 22px;
}
.product {
    overflow: hidden;
    border: 1px solid #35b8ff30;
    border-radius: 18px;
    background: linear-gradient(150deg, #102c47, #081727);
    transition: transform .25s;
}
.product:hover { transform: translateY(-5px); }
.product img {
    width: 100%;
    height: 240px;
    object-fit: contain;
    padding: 15px;
    background: #092238;
}
.product-info { padding: 17px; }
.product h3 { margin-top: 0; }
.product p {
    color: #b6cad7;
    min-height: 45px;
    line-height: 1.8;
}
.price {
    color: #d9c18a;
    font-weight: 800;
    margin: 12px 0;
}
.product-actions {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
}
.product-actions button, .product-actions a {
    flex: 1;
    text-align: center;
    font-size: 13px;
    padding: 10px;
    border-radius: 22px;
}

.cart-wrap, .form-card {
    background: linear-gradient(150deg, #102c47, #061827);
    border: 1px solid #35b8ff40;
    border-radius: 20px;
    padding: 22px;
}
.cart-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 12px;
    flex-wrap: wrap;
    padding: 13px 0;
    border-bottom: 1px solid #ffffff18;
}
.cart-item button {
    background: #123c53;
    border: 1px solid #35b8ff55;
    color: white;
    padding: 5px 10px;
    border-radius: 8px;
    cursor: pointer;
}
.cart-total {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 15px;
    margin-top: 20px;
}
.form-shell {
    max-width: 470px;
    margin: 55px auto;
    padding: 0 18px;
}
.form-card h1 {
    text-align: center;
    color: #35b8ff;
    font-family: 'Playfair Display', serif;
    letter-spacing: 4px;
}
.form-card .sub, .note {
    text-align: center;
    color: #b6cad7;
}
.form-card label {
    display: block;
    margin: 15px 0 6px;
}
.form-card input {
    width: 100%;
    padding: 12px;
    border: 1px solid #35b8ff55;
    border-radius: 10px;
    background: #031522;
    color: white;
}
.form-card .btn {
    width: 100%;
    margin-top: 22px;
}
.note { margin-top: 20px; }
.message {
    padding: 10px;
    margin: 12px 0;
    border-radius: 10px;
    background: #71343166;
}
footer {
    text-align: center;
    padding: 25px;
    color: #92acbd;
    border-top: 1px solid #35b8ff22;
}
@media(max-width:600px) {
    .nav, .links { justify-content: center; }
    .hero { min-height: 390px; }
}
"""


HOME_HTML = r"""
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>SOVA | عطور فاخرة</title>
<style>""" + STYLE + r"""</style>
</head>
<body>

<header>
<nav class="nav">
<a class="logo" href="#home">SOVA</a>
<div class="links">
<a href="#home">الرئيسية</a>
<a href="#about">من نحن</a>
<a href="#collection">عطورنا</a>
<a href="#cart">السلة <span id="cartCount">0</span></a>
{% if username %}
<span>هلا {{ username }}</span>
<a class="pill" href="{{ url_for('logout') }}">تسجيل الخروج</a>
{% else %}
<a class="pill" href="{{ url_for('login') }}">دخول / إنشاء حساب</a>
{% endif %}
</div>
</nav>
</header>

<div class="ocean" id="home">
<div class="bubbles" id="bubbles"></div>
<div class="hero">
<div>
<div class="eyebrow">THE ART OF PERFUMERY</div>
<h1>SOVA</h1>
<p>مو مجرد عطر، هذا حضور</p>
<a href="#collection" class="btn">اكتشف عطورنا</a>
</div>
</div>
</div>

<section id="about">
<div class="section-head">
<small>OUR STORY</small>
<h2>الفخامة تبدأ من التفاصيل</h2>
<p>اختيارات عطرية مميزة تناسب ذوقك وحضورك</p>
</div>
<p class="about">
في SOVA نؤمن أن العطر مو مجرد رائحة، بل جزء من شخصيتك وذكرى تبقى.
اختر عطرك المفضل وخلي حضورك يحچي عنك.
</p>
</section>

<section id="collection">
<div class="section-head">
<small>THE COLLECTION</small>
<h2>عطورنا</h2>
<p>اختار عطرك وأضفه للسلة أو اطلب مباشرة عبر واتساب</p>
</div>

<div class="products">

<div class="product">
<img src="{{ url_for('static', filename='images/afnan.jpg') }}" alt="Afnan 9 PM">
<div class="product-info">
<h3>Afnan 9 PM</h3>
<p>عطر مميز لمحبي الروائح الجذابة والحضور القوي</p>
<div class="price">65,000 د.ع</div>
<div class="product-actions">
<button class="btn" onclick="addToCart('Afnan 9 PM',65000)">أضف للسلة</button>
<a class="btn secondary" href="https://wa.me/{{ whatsapp }}?text={{ 'أريد طلب عطر Afnan 9 PM'|urlencode }}">اطلب الآن</a>
</div>
</div>
</div>

<div class="product">
<img src="{{ url_for('static', filename='images/asad.jpg') }}" alt="Lattafa Asad">
<div class="product-info">
<h3>Lattafa Asad</h3>
<p>عطر رجالي بطابع دافئ وجذاب</p>
<div class="price">45,000 د.ع</div>
<div class="product-actions">
<button class="btn" onclick="addToCart('Lattafa Asad',45000)">أضف للسلة</button>
<a class="btn secondary" href="https://wa.me/{{ whatsapp }}?text={{ 'أريد طلب عطر Lattafa Asad'|urlencode }}">اطلب الآن</a>
</div>
</div>
</div>

<div class="product">

<img src="{{ url_for('static', filename='images/FREEZE RIIFFS.jpg') }}" alt="FREEZE RIIFFS">
<div class="product-info">
<h3>FREEZE RIIFFS</h3>
<p>انتعاش مميز بطابع عصري</p>
<div class="price">50,000 د.ع</div>
<div class="product-actions">
<button class="btn" onclick="addToCart('FREEZE RIIFFS',50000)">أضف للسلة</button>
<a class="btn secondary" href="https://wa.me/{{ whatsapp }}?text={{ 'أريد طلب عطر FREEZE RIIFFS'|urlencode }}">اطلب الآن</a>
</div>
</div>
</div>

<div class="product">

<img src="{{ url_for('static', filename='images/FREEZE IN FLAMES RIIFFS.jpg') }}" alt="FREEZE IN FLAMES RIIFFS">

<div class="product-info">
<h3>FREEZE IN FLAMES RIIFFS</h3>
<p>توازن بين الانتعاش والطابع القوي</p>
<div class="price">50,000 د.ع</div>
<div class="product-actions">
<button class="btn" onclick="addToCart('FREEZE IN FLAMES RIIFFS',50000)">أضف للسلة</button>
<a class="btn secondary" href="https://wa.me/{{ whatsapp }}?text={{ 'أريد طلب عطر FREEZE IN FLAMES RIIFFS'|urlencode }}">اطلب الآن</a>
</div>
</div>
</div>

</div>
</section>

<section id="cart">
<div class="section-head">
<small>YOUR SELECTION</small>
<h2>سلة المشتريات</h2>
<p>راجع طلبك قبل الإرسال</p>
</div>
<div class="cart-wrap">
<div id="cartItems">السلة فارغة حالياً</div>
<div class="cart-total">
<strong>المجموع: <span id="cartTotal">0</span> د.ع</strong>
<button class="btn" onclick="checkout()">إكمال الطلب عبر واتساب</button>
</div>
</div>
</section>

<footer>© SOVA — مو مجرد عطر، هذا حضور</footer>

<script>
const WHATSAPP = {{ whatsapp|tojson }};
let cart = [];
try { cart = JSON.parse(localStorage.getItem('sova_cart') || '[]'); }
catch(e) { cart = []; }

function saveCart() {
    localStorage.setItem('sova_cart', JSON.stringify(cart));
    renderCart();
}
function addToCart(name, price) {
    const item = cart.find(x => x.name === name);
    if (item) item.qty++;
    else cart.push({name, price, qty:1});
    saveCart();
}
function changeQty(name, delta) {
    const item = cart.find(x => x.name === name);
    if (!item) return;
    item.qty += delta;
    if (item.qty <= 0) cart = cart.filter(x => x.name !== name);
    saveCart();
}
function removeItem(name) {
    cart = cart.filter(x => x.name !== name);
    saveCart();
}
function escapeHtml(value) {
    return String(value).replace(/[&<>"']/g, c => ({
        '&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;', "'":'&#39;'
    }[c]));
}
function renderCart() {
    const box = document.getElementById('cartItems');
    const count = cart.reduce((sum, x) => sum + x.qty, 0);
    const total = cart.reduce((sum, x) => sum + x.price * x.qty, 0);
    document.getElementById('cartCount').textContent = count;
    document.getElementById('cartTotal').textContent = total.toLocaleString('en-US');

    if (!cart.length) {
        box.textContent = 'السلة فارغة حالياً';
        return;
    }
    box.innerHTML = cart.map(x => `
        <div class="cart-item">
            <div><strong>${escapeHtml(x.name)}</strong><br>
            <small>${x.price.toLocaleString('en-US')} د.ع</small></div>
            <div>
                <button onclick="changeQty('${x.name}',-1)">−</button>
                ${x.qty}
                <button onclick="changeQty('${x.name}',1)">+</button>
                <button onclick="removeItem('${x.name}')">حذف</button>
            </div>
        </div>`).join('');
}
function checkout() {
    if (!cart.length) {
        alert('السلة فارغة، أضف عطراً أولاً');
        return;
    }
    const total = cart.reduce((sum, x) => sum + x.price * x.qty, 0);
    let msg = 'السلام عليكم، أريد طلب العطور التالية من SOVA:\n';
    cart.forEach(x => {
        msg += '\n- ' + x.name + ' × ' + x.qty + ' = ' +
            (x.price * x.qty).toLocaleString('en-US') + ' د.ع';
    });
    msg += '\n\nالمجموع: ' + total.toLocaleString('en-US') + ' د.ع';
    window.open('https://wa.me/' + WHATSAPP + '?text=' +
        encodeURIComponent(msg), '_blank');
}

const bubbles = document.getElementById('bubbles');
for (let i = 0; i < 25; i++) {
    const b = document.createElement('span');
    b.className = 'bubble';
    const size = 4 + Math.random() * 15;
    b.style.width = size + 'px';
    b.style.height = size + 'px';
    b.style.left = Math.random() * 100 + '%';
    b.style.animationDuration = (9 + Math.random() * 17) + 's';
    b.style.animationDelay = (-Math.random() * 20) + 's';
    bubbles.appendChild(b);
}
renderCart();
</script>
</body>
</html>
"""


AUTH_HTML = r"""
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{ title }} | SOVA</title>
<style>""" + STYLE + r"""</style>
</head>
<body>
<header>
<nav class="nav">
<a class="logo" href="{{ url_for('home') }}">SOVA</a>
<div class="links">
<a href="{{ url_for('home') }}">الرئيسية</a>
<a href="{{ url_for('login') }}">تسجيل الدخول</a>
<a href="{{ url_for('register') }}">إنشاء حساب</a>
</div>
</nav>
</header>

<div class="ocean">
<div class="bubbles" id="bubbles"></div>
<div class="form-shell">
<div class="form-card">
<h1>SOVA</h1>
<p class="sub">{{ title }}</p>

{% with messages = get_flashed_messages() %}
{% if messages %}
{% for message in messages %}
<div class="message">{{ message }}</div>
{% endfor %}
{% endif %}
{% endwith %}

<form method="post">
<label for="username">اسم المستخدم</label>
<input id="username" name="username" type="text"
minlength="3" maxlength="30" autocomplete="username"
required placeholder="اكتب اسم المستخدم">

<label for="password">كلمة المرور</label>
<input id="password" name="password" type="password"
minlength="6"
autocomplete="{{ 'new-password' if mode == 'register' else 'current-password' }}"
required placeholder="6 أحرف على الأقل">

{% if mode == 'register' %}
<label for="confirm">تأكيد كلمة المرور</label>
<input id="confirm" name="confirm" type="password"
minlength="6" autocomplete="new-password"
required placeholder="أعد كتابة كلمة المرور">
{% endif %}

<button class="btn" type="submit">{{ button }}</button>
</form>

<div class="note">
{% if mode == 'register' %}
عندك حساب؟
<a href="{{ url_for('login') }}" style="color:#35b8ff">سجّل دخولك</a>
{% else %}
ما عندك حساب؟
<a href="{{ url_for('register') }}" style="color:#35b8ff">أنشئ حساب جديد</a>
{% endif %}
</div>
</div>
</div>
</div>

<footer>© SOVA — مو مجرد عطر، هذا حضور</footer>
<script>
const bubbles = document.getElementById('bubbles');
for (let i = 0; i < 18; i++) {
    const b = document.createElement('span');
    b.className = 'bubble';
    const size = 4 + Math.random() * 15;
    b.style.width = size + 'px';
    b.style.height = size + 'px';
    b.style.left = Math.random() * 100 + '%';
    b.style.animationDuration = (9 + Math.random() * 17) + 's';
    b.style.animationDelay = (-Math.random() * 20) + 's';
    bubbles.appendChild(b);
}
</script>
</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(
        HOME_HTML,
        username=session.get("username"),
        whatsapp=WHATSAPP
    )


@app.route("/register", methods=["GET", "POST"])
def register():
    if session.get("username"):
        return redirect(url_for("home"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm", "")

        if len(username) < 3 or len(username) > 30:
            flash("اسم المستخدم لازم يكون بين 3 و30 حرف.")
        elif len(password) < 6:
            flash("كلمة المرور لازم تكون 6 أحرف على الأقل.")
        elif password != confirm:
            flash("كلمتا المرور غير متطابقتين.")
        else:
            try:
                with get_db() as conn:
                    conn.execute(
                        "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                        (username, generate_password_hash(password))
                    )
                session["username"] = username
                return redirect(url_for("home"))
            except sqlite3.IntegrityError:
                flash("اسم المستخدم مستخدم من قبل. اختار اسماً آخر.")

    return render_template_string(
        AUTH_HTML,
        title="إنشاء حساب جديد",
        button="إنشاء الحساب",
        mode="register"
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("username"):
        return redirect(url_for("home"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        with get_db() as conn:
            user = conn.execute(
                "SELECT username, password_hash FROM users WHERE username = ?",
                (username,)
            ).fetchone()

        if user and check_password_hash(user["password_hash"], password):
            session.clear()
            session["username"] = user["username"]
            return redirect(url_for("home"))

        flash("اسم المستخدم أو كلمة المرور غير صحيحة.")

    return render_template_string(
        AUTH_HTML,
        title="تسجيل الدخول",
        button="دخول",
        mode="login"
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
