from flask import Flask, render_template, request, redirect, url_for, session
import json
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # 세션을 위한 보안 키

NOTICE_FILE = "homework.json"

def load_notices():
    if os.path.exists(NOTICE_FILE):
        with open(NOTICE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_notices(notices):
    with open(NOTICE_FILE, "w", encoding="utf-8") as f:
        json.dump(notices, f, indent=4, ensure_ascii=False)

@app.route('/')
def home():
    notices = load_notices()
    is_admin = session.get('admin', False)
    return render_template('index.html', notices=notices, is_admin=is_admin)

@app.route('/login', methods=['POST'])
def login():
    password = request.form['password']
    if password == "1234":  # 관리자 비밀번호 설정 (원하는 비밀번호로 변경 가능)
        session['admin'] = True
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('home'))

@app.route('/add', methods=['POST'])
def add_notice():
    if not session.get('admin'):
        return redirect(url_for('home'))
    
    title = request.form['title']
    content = request.form['content']
    deadline = request.form['deadline']
    
    if title and content and deadline:
        notices = load_notices()
        notices.append({
            "id": len(notices) + 1,
            "title": title,
            "content": content,
            "deadline": deadline
        })
        save_notices(notices)

    return redirect(url_for('home'))

@app.route('/delete/<int:notice_id>', methods=['POST'])
def delete_notice(notice_id):
    if not session.get('admin'):
        return redirect(url_for('home'))
    
    notices = load_notices()
    notices = [n for n in notices if n["id"] != notice_id]
    save_notices(notices)
    
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
