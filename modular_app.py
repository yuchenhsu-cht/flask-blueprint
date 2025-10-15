# -*- coding: utf-8 -*-
# Flask 模組化專案範例 (使用 Blueprint 劃分 auth, api, ui)
# 已升級為使用 JSON 檔案進行資料持久化 (Persistence)

from flask import Flask, Blueprint, render_template, request, jsonify, redirect, url_for
import json
import os

# --- 資料持久化配置與輔助函式 (Model 層職責) ---
DATA_FILE = 'tasks.json' # 儲存資料的檔案名稱

def load_tasks():
    """從 JSON 檔案載入所有任務，如果檔案不存在則創建初始資料。"""
    if not os.path.exists(DATA_FILE) or os.path.getsize(DATA_FILE) == 0:
        initial_data = [
            {'id': 1, 'task': '設計 Blueprint 架構', 'done': True},
            {'id': 2, 'task': '實作資料持久化', 'done': False},
            {'id': 3, 'task': '完成 UI 重構', 'done': False},
        ]
        save_tasks(initial_data)
        return initial_data
    
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_tasks(tasks):
    """將當前所有任務寫入 JSON 檔案。"""
    # 確保資料是有序的
    tasks.sort(key=lambda t: t['id'])
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, indent=4, ensure_ascii=False)

def get_next_id(tasks):
    """取得下一個可用的 ID。"""
    return max([t['id'] for t in tasks] or [0]) + 1


# --- 1. 定義 Blueprint 模組 (Controller/Router) ---

# (1) UI 模組：處理主介面和頁面渲染
ui = Blueprint('ui', __name__, url_prefix='/')

@ui.route('/', methods=['GET'])
def index():
    """UI Controller: 渲染主頁面，顯示待辦事項列表 (R)。"""
    tasks = load_tasks()
    return render_template('ui_list.html', tasks=tasks)

@ui.route('/task/add', methods=['GET'])
def ui_add_task_form():
    """UI Controller: 渲染新增任務表單 (C)。"""
    return render_template('ui_form.html', task=None)

@ui.route('/task/edit/<int:task_id>', methods=['GET'])
def ui_edit_task_form(task_id):
    """UI Controller: 渲染編輯任務表單 (U)。"""
    tasks = load_tasks()
    task = next((t for t in tasks if t['id'] == task_id), None)
    if not task:
        return redirect(url_for('ui.index'))
    return render_template('ui_form.html', task=task)

# (2) API 模組：處理所有 CRUD 邏輯 (POST/PUT/DELETE)
api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/tasks', methods=['POST'])
def handle_tasks_post():
    tasks = load_tasks()
    
    # 處理 UI 表單提交（新增任務）
    task_name = request.form.get('task')
    if task_name:
        new_id = get_next_id(tasks)
        new_task = {'id': new_id, 'task': task_name, 'done': False}
        tasks.append(new_task)
        save_tasks(tasks)
        return redirect(url_for('ui.index')) 
    
    # 處理 API JSON 提交
    if request.is_json:
        data = request.json
        if 'task' not in data: return jsonify({'error': 'Missing task data'}), 400
        new_id = get_next_id(tasks)
        new_task = {'id': new_id, 'task': data['task'], 'done': data.get('done', False)}
        tasks.append(new_task)
        save_tasks(tasks)
        return jsonify(new_task), 201

    return jsonify({'error': 'Invalid request format'}), 400

@api.route('/tasks/<int:task_id>', methods=['GET'])
def handle_tasks_get(task_id):
    """單一任務 API 查詢 (R)"""
    tasks = load_tasks()
    task = next((t for t in tasks if t['id'] == task_id), None)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    return jsonify(task)

@api.route('/tasks/<int:task_id>', methods=['POST'])
def handle_single_task_ui(task_id):
    """專門用於處理 UI 表單的 Update, Delete, Toggle 邏輯。"""
    tasks = load_tasks()
    task = next((t for t in tasks if t['id'] == task_id), None)
    if not task: return redirect(url_for('ui.index'))

    action = request.form.get('action')
    
    if action == 'toggle':
        # U: 切換狀態 (快速更新)
        task['done'] = not task['done']
    
    elif action == 'edit':
        # U: 編輯/更新任務
        task_name = request.form.get('task')
        if task_name:
            task['task'] = task_name
            task['done'] = request.form.get('done') == 'on'
        
    elif action == 'delete':
        # D: 刪除任務
        tasks.remove(task)
    
    save_tasks(tasks)
    return redirect(url_for('ui.index'))


# (3) AUTH 模組：處理使用者驗證邏輯
auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """Auth Controller: 模擬登入流程。"""
    if request.method == 'POST':
        return redirect(url_for('ui.index')) 
    return "<h1>登入頁面 (Auth Module)</h1><form method='POST' class='p-4'><input type='text' name='username' class='border p-2'><button type='submit' class='bg-blue-500 text-white p-2 rounded ml-2'>登入</button></form>"

@auth.route('/logout')
def logout():
    """Auth Controller: 模擬登出。"""
    return redirect(url_for('ui.index'))

# --- 2. 應用程式工廠 (Application Factory) ---
def create_app(test_config=None):
    """
    應用程式工廠：建立並配置 Flask 實例。
    """
    app = Flask(__name__, instance_relative_config=True, template_folder='templates')

    app.config.from_mapping(
        SECRET_KEY='dev_key', 
        TEMPLATES_AUTO_RELOAD=True
    )

    # 註冊 Blueprints (模組化關鍵步驟)
    app.register_blueprint(ui)
    app.register_blueprint(api)
    app.register_blueprint(auth)

    return app

# --- 3. 運行腳本 ---

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5001)
