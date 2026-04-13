"""
JSONL Viewer - Mac App 打包配置
"""
from setuptools import setup

APP = ['app.py']
DATA_FILES = ['icon.png', 'AppIcon.icns']
OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'AppIcon.icns',
    'plist': {
        'CFBundleName': 'JSONL查看器',
        'CFBundleDisplayName': 'JSONL查看器',
        'CFBundleIdentifier': 'com.wphu.jsonl-viewer',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'NSHumanReadableCopyright': 'Created by wphu',
        'NSHighResolutionCapable': True,
    },
    'packages': ['webview'],
    'includes': ['json', 'subprocess', 'pathlib'],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
