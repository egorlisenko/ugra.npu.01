from flask import Flask, render_template, request, redirect, session, url_for, abort
from pathlib import Path
import json

BASE = Path(__file__).parent

NEWS_FILE = BASE / "news.json"
USERS_FILE = BASE / "users.json"
TASKS_FILE = BASE / "tasks.json"

app = Flask(__name__)
app.secret_key = "replace_this_with_a_random_secret_in_production"

def load_json(path, default):
    try:
        if not path.exists():
            path.write_text(json.dumps(default, ensure_ascii=False, indent=2), encoding="utf-8")
            return default
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        # якщо файл пошкоджений — відновлюємо
        path.write_text(json.dumps(default, ensure_ascii=False, indent=2), encoding="utf-8")
        return default

def save_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

# Ініціалізація файлів (якщо порожні)
news = load_json(NEWS_FILE, [])
users = load_json(USERS_FILE, [
    {
        "username": "admin_egor",   # ім'я акаунту
        "login": "14092025",       # login поле
        "password": "14092025",    # пароль (як ти просив)
        "role": "superadmin"       # superadmin може створювати адміністраторів
    }
])
tasks = load_json(TASKS_FILE, [])

def current_user():
    if "user" in session:
        return session["user"]
    return None

def require_login():
    if "user" not in session:
        return False
    return True

@app.route("/")
def index():
    # показати всі новини
    global news
    news = load_json(NEWS_FILE, news)
    return render_template("index.html", news=news, user=current_user())

@app.route("/login", methods=["GET", "POST"])
def login():
    global users
    users = load_json(USERS_FILE, users)
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        login_val = request.form.get("login", "").strip()
        password = request.form.get("password", "").strip()
        for u in users:
            if u.get("username") == username and u.get("login") == login_val and u.get("password") == password:
                # зберігаємо тільки потрібні поля в сесії
                session["user"] = {"username": u["username"], "role": u.get("role", "user")}
                return redirect(url_for("dashboard"))
        return render_template("login.html", error="Невірний логін або пароль")
    return render_template("login.html", error=None)

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("index"))

@app.route("/dashboard")
def dashboard():
    if not require_login():
        return redirect(url_for("login"))
    global news, users, tasks
    news = load_json(NEWS_FILE, news)
    users = load_json(USERS_FILE, users)
    tasks = load_json(TASKS_FILE, tasks)
    return render_template("dashboard.html", news=news, users=users, tasks=tasks, user=current_user())

@app.route("/add_news", methods=["POST"])
def add_news():
    if not require_login():
        return redirect(url_for("login"))
    title = request.form.get("title", "").strip()
    content = request.form.get("content", "").strip()
    if title and content:
        news_list = load_json(NEWS_FILE, news)
        news_item = {"title": title, "content": content}
        news_list.insert(0, news_item)
        save_json(NEWS_FILE, news_list)
    return redirect(url_for("dashboard"))

@app.route("/add_task", methods=["POST"])
def add_task():
    if not require_login():
        return redirect(url_for("login"))
    task_text = request.form.get("task", "").strip()
    if task_text:
        tasks_list = load_json(TASKS_FILE, tasks)
        tasks_list.insert(0, task_text)
        save_json(TASKS_FILE, tasks_list)
    return redirect(url_for("dashboard"))

@app.route("/add_user", methods=["POST"])
def add_user():
    if not require_login():
        return redirect(url_for("login"))
    user = current_user()
    # тільки адміністратор може додавати користувачів
    if user.get("role") not in ("superadmin", "admin"):
        abort(403)
    new_username = request.form.get("username", "").strip()
    new_login = request.form.get("login", "").strip()
    new_password = request.form.get("password", "").strip()
    new_role = request.form.get("role", "user")
    if not (new_username and new_login and new_password):
        return redirect(url_for("dashboard"))
    users_list = load_json(USERS_FILE, users)
    users_list.append({
        "username": new_username,
        "login": new_login,
        "password": new_password,
        "role": new_role
    })
    save_json(USERS_FILE, users_list)
    return redirect(url_for("dashboard"))

# Проста сторінка для перевірки прав
@app.errorhandler(403)
def forbidden(e):
    return "Доступ заборонено", 403

if __name__ == "__main__":
    # запускаємо локально; у продакшн — використовуй WSGI сервер
    app.run(host="127.0.0.1", port=5000, debug=True)
