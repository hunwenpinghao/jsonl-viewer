#!/bin/bash
# 创建 DMG 安装包

APP_NAME="JSONL查看器"
APP_PATH="dist/${APP_NAME}.app"
DMG_NAME="JSONL查看器-v1.0.dmg"
VOLUME_NAME="JSONL查看器安装"

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
mkdir -p "$TMP_DIR/.background"

# 复制应用
cp -R "$APP_PATH" "$TMP_DIR/"

# 创建 Applications 文件夹快捷方式
ln -s /Applications "$TMP_DIR/Applications"

# 创建背景图片（可选，使用纯色背景）
cat > "$TMP_DIR/.background/DS_Store" << 'EOF'
EOF

# 创建 .DS_Store 来设置窗口样式
# 使用 applescript 设置 DMG 窗口布局
cat > "$TMP_DIR/setup_dmg.scpt" << 'EOF'
tell application "Finder"
    tell disk "JSONL查看器安装"
        open
        set current view of container window to icon view
        set toolbar visible of container window to false
        set statusbar visible of container window to false
        set the bounds of container window to {400, 100, 885, 430}
        set theViewOptions to the icon view options of container window
        set arrangement of theViewOptions to not arranged
        set icon size of theViewOptions to 72
        set position of item "JSONL查看器.app" of container window to {100, 100}
        set position of item "Applications" of container window to {375, 100}
        close
    end tell
end tell
EOF

# 创建 DMG
hdiutil create -srcfolder "$TMP_DIR" -volname "$VOLUME_NAME" -fs HFS+ -format UDZO -size 100m "$DMG_NAME"

# 清理临时目录
rm -rf "$TMP_DIR"

echo "✅ DMG 创建成功: $DMG_NAME"
ls -lh "$DMG_NAME"
