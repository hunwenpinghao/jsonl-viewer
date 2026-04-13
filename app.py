#!/usr/bin/env python3
import json
import webview
from pathlib import Path
import sys
import subprocess

class JSONLViewer:
    def __init__(self):
        self.records = []
        self.current_index = 0
        self.filepath = None
        self.window = None
        
    def set_window(self, window):
        self.window = window
        
    def open_file_dialog(self):
        if not self.window:
            return {"error": "窗口未初始化"}
        result = self.window.create_file_dialog(webview.OPEN_DIALOG,
            file_types=('JSONL Files (*.jsonl)', 'JSON Files (*.json)', 'All Files (*.*)'))
        if result and len(result) > 0:
            return self.load_file(result[0])
        return {"cancelled": True}
    
    def load_file(self, filepath):
        self.records = []
        self.current_index = 0
        self.filepath = filepath
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                for i, line in enumerate(f, 1):
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        record = json.loads(line)
                        self.records.append(record)
                    except json.JSONDecodeError as e:
                        return {"error": f"第 {i} 行解析错误: {e}", "count": 0}
            return {"success": True, "filename": Path(filepath).name, "count": len(self.records)}
        except Exception as e:
            return {"error": str(e), "count": 0}
    
    def load_from_text(self, text):
        if not text or not text.strip():
            return {"error": "内容为空", "count": 0}
        self.records = []
        self.current_index = 0
        self.filepath = None
        lines = text.strip().split('\n')
        for i, line in enumerate(lines, 1):
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
                self.records.append(record)
            except json.JSONDecodeError as e:
                return {"error": f"第 {i} 行解析错误: {e}", "count": 0}
        return {"success": True, "filename": "输入内容", "count": len(self.records)}
    
    def paste_from_clipboard(self):
        try:
            result = subprocess.run(['pbpaste'], capture_output=True, text=True)
            if result.returncode != 0:
                return {"error": "无法读取剪贴板", "count": 0}
            return self.load_from_text(result.stdout)
        except Exception as e:
            return {"error": f"粘贴失败: {e}", "count": 0}
    
    def clear(self):
        self.records = []
        self.current_index = 0
        self.filepath = None
        return {"success": True}
    
    def get_record(self, index=None):
        if not self.records:
            return {"error": "无记录", "index": 0, "total": 0, "content": "", "fields": [], "empty": True}
        if index is not None:
            index = max(0, min(index, len(self.records) - 1))
            self.current_index = index
        record = self.records[self.current_index]
        formatted = self.format_record(record)
        return {"index": self.current_index + 1, "total": len(self.records), "content": formatted, "fields": list(record.keys()), "empty": False}
    
    def format_record(self, record):
        lines = ["=" * 60]
        for key, value in record.items():
            lines.append(f"\n【{key}】")
            lines.append("-" * 40)
            if isinstance(value, str):
                if len(value) > 100:
                    try:
                        parsed = json.loads(value)
                        lines.append(json.dumps(parsed, ensure_ascii=False, indent=2))
                    except:
                        lines.append(value)
                else:
                    lines.append(value)
            elif isinstance(value, (dict, list)):
                lines.append(json.dumps(value, ensure_ascii=False, indent=2))
            else:
                lines.append(str(value))
        lines.append("\n" + "=" * 60)
        return "\n".join(lines)
    
    def prev_record(self):
        if self.current_index > 0:
            self.current_index -= 1
        return self.get_record()
    
    def next_record(self):
        if self.current_index < len(self.records) - 1:
            self.current_index += 1
        return self.get_record()
    
    def goto_record(self, index):
        return self.get_record(index - 1)

HTML = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>JSONL 查看器</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #1e1e1e; color: #d4d4d4; height: 100vh; display: flex; flex-direction: column; }
        .toolbar { background: #2d2d2d; padding: 12px 16px; display: flex; align-items: center; gap: 12px; border-bottom: 1px solid #404040; -webkit-app-region: drag; }
        button { background: #0e639c; color: white; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer; font-size: 13px; -webkit-app-region: no-drag; }
        button:hover { background: #1177bb; }
        button.secondary { background: #3c3c3c; border: 1px solid #505050; }
        button.secondary:hover { background: #4a4a4a; }
        button.danger { background: #5c3c3c; border: 1px solid #704040; color: #ff9999; }
        button.danger:hover { background: #704040; }
        button.success { background: #2d5c3c; border: 1px solid #407040; color: #99ff99; }
        button.success:hover { background: #3d7c4c; }
        .nav-info { color: #808080; font-size: 13px; min-width: 120px; text-align: center; -webkit-app-region: no-drag; }
        .jump-box { display: flex; align-items: center; gap: 6px; -webkit-app-region: no-drag; }
        .jump-box input { width: 60px; padding: 6px 10px; border: 1px solid #404040; border-radius: 4px; background: #3c3c3c; color: #d4d4d4; font-size: 13px; }
        .main { flex: 1; display: flex; overflow: hidden; }
        .sidebar { width: 200px; background: #252526; border-right: 1px solid #404040; overflow-y: auto; padding: 12px; }
        .sidebar h3 { font-size: 11px; color: #808080; text-transform: uppercase; margin-bottom: 8px; }
        .field-item { padding: 6px 10px; background: #3c3c3c; border-radius: 4px; margin-bottom: 4px; font-size: 12px; font-family: Menlo, monospace; }
        .content { flex: 1; display: flex; flex-direction: column; overflow: hidden; }
        .input-area { flex: 1; display: flex; flex-direction: column; padding: 16px; }
        .input-area textarea {
            flex: 1;
            width: 100%;
            background: #1e1e1e;
            border: 1px solid #404040;
            border-radius: 4px;
            padding: 12px;
            color: #d4d4d4;
            font-family: Menlo, Monaco, monospace;
            font-size: 13px;
            line-height: 1.6;
            resize: none;
            outline: none;
        }
        .input-area textarea:focus { border-color: #0e639c; }
        .input-area textarea::placeholder { color: #666; }
        .input-actions { display: flex; gap: 8px; margin-top: 12px; }
        .display-area { flex: 1; overflow-y: auto; padding: 16px; display: none; }
        .display-area pre { font-family: Menlo, Monaco, monospace; font-size: 13px; line-height: 1.6; white-space: pre-wrap; word-wrap: break-word; }
        .status-bar { background: #007acc; color: white; padding: 4px 16px; font-size: 12px; }
    </style>
</head>
<body>
    <div class="toolbar">
        <button id="openBtn">📂 打开</button>
        <button id="pasteBtn" class="secondary">📋 粘贴</button>
        <button id="clearBtn" class="danger">🗑 清空</button>
        <div style="flex:1"></div>
        <button id="prevBtn">← 上一条</button>
        <span class="nav-info" id="navInfo">共 0 条</span>
        <button id="nextBtn">下一条 →</button>
        <div class="jump-box">
            <span>跳转:</span>
            <input type="number" id="jumpIndex" min="1">
            <button id="gotoBtn">跳</button>
        </div>
    </div>
    <div class="main">
        <div class="sidebar">
            <h3>字段列表</h3>
            <div id="fieldList"></div>
        </div>
        <div class="content">
            <div class="input-area" id="inputArea">
                <textarea id="jsonlInput" placeholder="请打开 JSONL 文件或粘贴内容 (⌘V)&#10;也可以直接在此输入 JSONL 内容..."></textarea>
                <div class="input-actions">
                    <button id="loadBtn" class="success">✓ 加载输入内容</button>
                    <button id="clearInputBtn" class="secondary">清除</button>
                </div>
            </div>
            <div class="display-area" id="displayArea">
                <pre id="content"></pre>
            </div>
        </div>
    </div>
    <div class="status-bar" id="statusBar">就绪</div>
    <script>
        let isViewMode = false;
        
        document.getElementById("openBtn").addEventListener("click", openFile);
        document.getElementById("pasteBtn").addEventListener("click", pasteFromClipboard);
        document.getElementById("clearBtn").addEventListener("click", clearAll);
        document.getElementById("loadBtn").addEventListener("click", loadInput);
        document.getElementById("clearInputBtn").addEventListener("click", () => {
            document.getElementById("jsonlInput").value = "";
        });
        document.getElementById("prevBtn").addEventListener("click", prevRecord);
        document.getElementById("nextBtn").addEventListener("click", nextRecord);
        document.getElementById("gotoBtn").addEventListener("click", gotoRecord);
        document.getElementById("jumpIndex").addEventListener("keypress", function(e) {
            if (e.key === "Enter") gotoRecord();
        });
        
        async function openFile() {
            document.getElementById("statusBar").textContent = "选择文件中...";
            const result = await pywebview.api.open_file_dialog();
            handleLoadResult(result);
        }
        
        async function pasteFromClipboard() {
            document.getElementById("statusBar").textContent = "读取剪贴板...";
            const result = await pywebview.api.paste_from_clipboard();
            handleLoadResult(result);
        }
        
        async function loadInput() {
            const text = document.getElementById("jsonlInput").value;
            if (!text.trim()) {
                document.getElementById("statusBar").textContent = "请输入内容";
                return;
            }
            document.getElementById("statusBar").textContent = "加载中...";
            const result = await pywebview.api.load_from_text(text);
            handleLoadResult(result);
        }
        
        async function clearAll() {
            if (!confirm("确定要清空所有记录吗？")) return;
            await pywebview.api.clear();
            document.getElementById("statusBar").textContent = "已清空";
            showInputMode();
        }
        
        function handleLoadResult(result) {
            if (result && result.cancelled) {
                document.getElementById("statusBar").textContent = "已取消";
                return;
            }
            if (result && result.error) {
                document.getElementById("statusBar").textContent = "错误: " + result.error;
                return;
            }
            if (result && result.success) {
                document.getElementById("statusBar").textContent = "已加载: " + result.filename + " (" + result.count + " 条记录)";
                showViewMode();
                updateDisplay();
            }
        }
        
        function showInputMode() {
            isViewMode = false;
            document.getElementById("inputArea").style.display = "flex";
            document.getElementById("displayArea").style.display = "none";
            document.getElementById("navInfo").textContent = "共 0 条";
            document.getElementById("fieldList").innerHTML = "";
        }
        
        function showViewMode() {
            isViewMode = true;
            document.getElementById("inputArea").style.display = "none";
            document.getElementById("displayArea").style.display = "block";
        }
        
        async function prevRecord() {
            if (!isViewMode) return;
            const data = await pywebview.api.prev_record();
            renderRecord(data);
        }
        
        async function nextRecord() {
            if (!isViewMode) return;
            const data = await pywebview.api.next_record();
            renderRecord(data);
        }
        
        async function gotoRecord() {
            if (!isViewMode) return;
            const index = parseInt(document.getElementById("jumpIndex").value);
            if (isNaN(index)) return;
            const data = await pywebview.api.goto_record(index);
            renderRecord(data);
        }
        
        async function updateDisplay() {
            const data = await pywebview.api.get_record();
            renderRecord(data);
        }
        
        function renderRecord(data) {
            if (!data) return;
            document.getElementById("navInfo").textContent = "第 " + (data.index || 0) + " / " + (data.total || 0) + " 条";
            document.getElementById("content").textContent = data.content || "";
            const fieldList = document.getElementById("fieldList");
            fieldList.innerHTML = "";
            (data.fields || []).forEach(field => {
                const div = document.createElement("div");
                div.className = "field-item";
                div.textContent = field;
                fieldList.appendChild(div);
            });
            if (data.index) {
                document.getElementById("jumpIndex").value = data.index;
            }
        }
        
        document.addEventListener("keydown", async (e) => {
            if ((e.metaKey || e.ctrlKey) && e.key === "v") {
                e.preventDefault();
                await pasteFromClipboard();
                return;
            }
            if (e.target.tagName === "INPUT" || e.target.tagName === "TEXTAREA") return;
            if (e.key === "ArrowLeft" || e.key === "ArrowUp") {
                e.preventDefault();
                await prevRecord();
            } else if (e.key === "ArrowRight" || e.key === "ArrowDown") {
                e.preventDefault();
                await nextRecord();
            }
        });
    </script>
</body>
</html>'''

def main():
    viewer = JSONLViewer()
    if len(sys.argv) > 1:
        viewer.load_file(sys.argv[1])
    window = webview.create_window("JSONL 查看器", html=HTML, js_api=viewer, width=1200, height=800, resizable=True)
    viewer.set_window(window)
    webview.start(debug=False)

if __name__ == "__main__":
    main()
