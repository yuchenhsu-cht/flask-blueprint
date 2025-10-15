# app/ui/views.py
from flask import Blueprint, render_template, redirect, url_for
from ..models import load_tasks # 從 app/models.py 匯入 Model 層

# 創建 Blueprint
ui_bp = Blueprint('ui', __name__)

@ui_bp.route('/', methods=['GET'])
def index():
    """UI Controller: 渲染主頁面，顯示待辦事項列表 (R)。"""
    tasks = load_tasks()
    return render_template('ui_list.html', tasks=tasks)

@ui_bp.route('/task/add', methods=['GET'])
def ui_add_task_form():
    """UI Controller: 渲染新增任務表單 (C)。"""
    return render_template('ui_form.html', task=None)

@ui_bp.route('/task/edit/<int:task_id>', methods=['GET'])
def ui_edit_task_form(task_id):
    """UI Controller: 渲染編輯任務表單 (U)。"""
    tasks = load_tasks()
    task = next((t for t in tasks if t['id'] == task_id), None)
    if not task:
        return redirect(url_for('ui.index'))
    return render_template('ui_form.html', task=task)
