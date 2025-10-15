# app/api/views.py
from flask import Blueprint, request, jsonify, redirect, url_for
from ..models import load_tasks, save_tasks, get_next_id

# 創建 Blueprint
api_bp = Blueprint('api', __name__)

# --- CRUD 核心邏輯 (由 UI 或 JSON API 調用) ---

@api_bp.route('/tasks', methods=['POST'])
def handle_tasks_post():
    """處理 UI 表單提交（新增任務 C）或 JSON API 新增。"""
    tasks = load_tasks()
    
    # 1. 處理 UI 表單提交（新增任務）
    task_name = request.form.get('task')
    if task_name:
        new_id = get_next_id(tasks)
        new_task = {'id': new_id, 'task': task_name, 'done': False}
        tasks.append(new_task)
        save_tasks(tasks)
        # UI 操作成功後重定向回列表頁面
        return redirect(url_for('ui.index')) 
    
    # 2. 處理 API JSON 提交
    if request.is_json:
        data = request.json
        if 'task' not in data: return jsonify({'error': 'Missing task data'}), 400
        
        new_id = get_next_id(tasks)
        new_task = {'id': new_id, 'task': data['task'], 'done': data.get('done', False)}
        tasks.append(new_task)
        save_tasks(tasks)
        return jsonify(new_task), 201

    return jsonify({'error': 'Invalid request format'}), 400

@api_bp.route('/tasks/<int:task_id>', methods=['POST'])
def handle_single_task_ui(task_id):
    """專門用於處理 UI 表單的 Update (編輯/切換) 和 Delete 邏輯。"""
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
