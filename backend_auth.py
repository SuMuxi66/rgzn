from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import json
import os
import hashlib
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# 数据文件路径
DATA_DIR = 'data/后端'
USERS_FILE = os.path.join(DATA_DIR, 'users.json')

# 确保数据目录存在
os.makedirs(DATA_DIR, exist_ok=True)

# 初始化用户数据文件
def init_users_file():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w', encoding='utf-8') as f:
            json.dump({"users": []}, f, ensure_ascii=False, indent=2)

# 密码加密
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# 加载用户数据
def load_users():
    init_users_file()
    with open(USERS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

# 保存用户数据
def save_users(users_data):
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users_data, f, ensure_ascii=False, indent=2)

# 查找用户
def find_user(username=None, email=None):
    users_data = load_users()
    for user in users_data['users']:
        if (username and user['username'] == username) or (email and user['email'] == email):
            return user
    return None

# 注册用户
def register_user(username, email, password):
    users_data = load_users()
    
    # 检查用户名或邮箱是否已存在
    if find_user(username=username) or find_user(email=email):
        return False
    
    # 创建新用户
    new_user = {
        'username': username,
        'email': email,
        'password': hash_password(password),
        'created_at': '2025-01-01'  # 简化处理
    }
    
    users_data['users'].append(new_user)
    save_users(users_data)
    return True

# 验证用户登录
def verify_user(username, password):
    user = find_user(username=username)
    if user and user['password'] == hash_password(password):
        return user
    return None

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember') == 'on'
        
        user = verify_user(username, password)
        if user:
            session['user'] = user['username']
            session['email'] = user['email']
            if remember:
                session.permanent = True
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='用户名或密码错误')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            return render_template('register.html', error='两次输入的密码不一致')
        
        if len(password) < 6:
            return render_template('register.html', error='密码长度至少6位')
        
        success = register_user(username, email, password)
        if success:
            return redirect(url_for('login'))
        else:
            return render_template('register.html', error='用户名或邮箱已存在')
    
    return render_template('register.html')

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        # 在实际应用中，这里应该发送重置邮件
        # 为了简化，我们只是显示提示信息
        return render_template('forgot_password.html', message='密码重置链接已发送到您的邮箱')
    
    return render_template('forgot_password.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    init_users_file()
    app.run(debug=True, host='0.0.0.0', port=5000)
