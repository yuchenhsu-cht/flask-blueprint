# app/models.py
import json
import os

DATA_FILE = 'tasks.json'

def load_tasks():
    """從 JSON 檔案載入所有任務。"""
    if not os.path.exists(DATA_FILE) or os.path.getsize(DATA_FILE) == 0:
        initial_data = [
            {'id': 1, 'task': '設計 Blueprint 架構', 'done': True},
            {'id': 2, 'task': '實作資料持久化', 'done': False},
            {'id': 3, 'task': '完成輕奢 UI 重構', 'done': False},
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
    tasks.sort(key=lambda t: t['id'])
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, indent=4, ensure_ascii=False)

def get_next_id(tasks):
    """取得下一個可用的 ID。"""
    return max([t['id'] for t in tasks] or [0]) + 1
