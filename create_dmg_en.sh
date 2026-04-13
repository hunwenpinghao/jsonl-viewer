#!/bin/bash
# 创建英文版 DMG 安装包

APP_NAME="JSONL查看器"
APP_PATH="dist/${APP_NAME}.app"
DMG_NAME="JSONL-Viewer-v1.0.dmg"
VOLUME_NAME="JSONL Viewer Install"

if [ ! -d "$APP_PATH" ]; then
    echo "错误: 找不到 $APP_PATH"
    echo "请先运行 ./build_app.sh 打包应用"
    exit 1
fi

cd "$(dirname "$0")"

# 清理旧的 DMG
rm -f "$DMG_NAME"

# 创建临时目录
TMP_DIR=$(mktemp -d)

# 复制应用，改名为英文
cp -R "$APP_PATH" "$TMP_DIR/JSONL Viewer.app"

# 创建 Applications 文件夹快捷方式
ln -s /Applications "$TMP_DIR/Applications"

# 创建 DMG
hdiutil create -srcfolder "$TMP_DIR" -volname "$VOLUME_NAME" -fs HFS+ -format UDZO -size 100m "$DMG_NAME"

# 清理临时目录
rm -rf "$TMP_DIR"

echo "✅ DMG 创建成功: $DMG_NAME"
ls -lh "$DMG_NAME"
