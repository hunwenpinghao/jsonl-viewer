# JSONL 查看器

一个简洁优雅的 macOS 桌面应用，用于查看和浏览 JSONL（JSON Lines）文件。

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Platform](https://img.shields.io/badge/Platform-macOS-lightgrey.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 功能特性

- 📂 **打开文件** - 支持选择本地 JSONL 文件
- 📋 **粘贴导入** - 支持 ⌘V 从剪贴板直接粘贴 JSONL 内容
- ✏️ **直接输入** - 支持在输入框中直接输入 JSONL 内容
- 🗑️ **清空数据** - 一键清空所有记录
- 🔍 **记录导航** - 上一条/下一条切换，支持键盘方向键
- 🔢 **快速跳转** - 输入序号直接跳转到指定记录
- 📋 **字段列表** - 左侧显示当前记录的所有字段名
- 🎨 **深色主题** - 优雅的深色界面，护眼舒适

## 安装运行

### 环境要求

- macOS 10.14+
- Python 3.8+

### 安装依赖

```bash
# 克隆仓库
git clone https://github.com/yourusername/jsonl-viewer.git
cd jsonl-viewer

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install pywebview
```

### 运行应用

```bash
python app.py
```

或者双击桌面上的 `JSONL查看器.app`（如果已创建）

## 使用说明

### 打开文件
点击「📂 打开」按钮选择 JSONL 文件，或直接拖拽文件到应用窗口。

### 粘贴内容
复制 JSONL 内容后，按 `⌘V` 或点击「📋 粘贴」按钮即可加载。

### 直接输入
1. 在主界面点击输入区域
2. 直接输入或粘贴 JSONL 内容
3. 点击「✓ 加载输入内容」按钮解析

### 浏览记录
- 点击「← 上一条」/「下一条 →」按钮
- 或使用键盘 `↑` `↓` `←` `→` 方向键
- 在跳转框输入序号按回车快速定位

### 清空数据
点击「🗑 清空」按钮清空所有记录（会弹出确认对话框）

## JSONL 格式说明

JSONL（JSON Lines）是一种每行一个独立 JSON 对象的文本格式：

```jsonl
{"name": "张三", "age": 25}
{"name": "李四", "age": 30}
{"name": "王五", "age": 28}
```

每行必须是一个合法的 JSON 对象，行与行之间用换行符分隔。

## 项目结构

```
jsonl-viewer/
├── app.py              # 主程序
├── README.md           # 项目说明
├── requirements.txt    # 依赖列表
├── icon.png            # 应用图标
├── AppIcon.icns        # macOS 图标集
└── venv/               # 虚拟环境（本地使用）
```

## 打包应用（可选）

使用 py2app 打包成独立的 Mac 应用：

```bash
# 安装 py2app
pip install py2app

# 打包
python setup.py py2app

# 打包后的应用在 dist/ 目录中
```

## 技术栈

- **Python 3** - 后端逻辑
- **pywebview** - 桌面应用框架
- **HTML/CSS/JS** - 前端界面
- **Tkinter** - 文件对话框（备选）

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

## 作者

Created with ❤️ by [Your Name]
