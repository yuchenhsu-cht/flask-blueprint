# run.py
import os
from app import create_app

# 確保在非開發環境下不啟用 Debug 模式
ENV = os.environ.get('FLASK_ENV') or 'development'
DEBUG = ENV == 'development'

app = create_app(ENV)

if __name__ == '__main__':
    # 使用 5001 埠號，避免 5000 埠號衝突
    app.run(host='127.0.0.1', port=5001, debug=DEBUG)
