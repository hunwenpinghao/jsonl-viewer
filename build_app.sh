#!/bin/bash
# 打包 JSONL Viewer 为 Mac App

cd "$(dirname "$0")"
source venv/bin/activate

# 清理旧构建
rm -rf build dist

# 打包
python setup.py py2app

# 检查是否成功
if [ -d "dist/JSONL查看器.app" ]; then
    echo "✅ 打包成功！"
    echo "应用位置: dist/JSONL查看器.app"
    ls -lh "dist/JSONL查看器.app/Contents/MacOS/"
else
    echo "❌ 打包失败"
fi
