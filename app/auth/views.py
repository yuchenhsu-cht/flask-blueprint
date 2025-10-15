# app/auth/views.py
from flask import Blueprint, request, redirect, url_for

# 創建 Blueprint
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Auth Controller: 模擬登入流程。"""
    if request.method == 'POST':
        # 實際情況會驗證用戶名和密碼
        return redirect(url_for('ui.index')) 
    return "<h1>登入頁面 (Auth Module)</h1><form method='POST' class='p-4'><input type='text' name='username' class='border p-2'><button type='submit' class='bg-blue-500 text-white p-2 rounded ml-2'>登入</button></form>"

@auth_bp.route('/logout')
def logout():
    """Auth Controller: 模擬登出。"""
    return redirect(url_for('ui.index'))
