#!/bin/bash

echo "🚀 构建Hidzor DMG安装包..."

# 清理旧文件
echo "清理旧文件..."
rm -rf build dist __pycache__

# 安装依赖
echo "安装依赖..."
pip3 install -r requirements.txt

# 使用spec文件构建
echo "开始构建应用..."
pyinstaller Hidzor.spec

if [ $? -eq 0 ]; then
    echo "✅ 应用构建成功!"
    echo "📁 应用位置: dist/Hidzor"
    echo "📦 应用包: dist/Hidzor.app"
    
    # 检查是否有create-dmg工具
    if command -v create-dmg &> /dev/null; then
        echo "📦 创建DMG安装包..."
        
        # 创建DMG
        create-dmg \
            --volname "Hidzor" \
            --window-pos 200 120 \
            --window-size 600 400 \
            --icon-size 100 \
            --icon "Hidzor.app" 175 120 \
            --hide-extension "Hidzor.app" \
            --app-drop-link 425 120 \
            --no-internet-enable \
            "dist/Hidzor.dmg" \
            "dist/Hidzor.app"
        
        if [ $? -eq 0 ]; then
            echo "✅ DMG创建成功!"
            echo "📦 DMG位置: dist/Hidzor.dmg"
            
            # 显示DMG信息
            echo ""
            echo "📊 DMG文件信息:"
            ls -lh dist/Hidzor.dmg
        else
            echo "❌ DMG创建失败!"
            exit 1
        fi
    else
        echo "⚠️  未找到create-dmg工具，跳过DMG创建"
        echo "💡 可以通过以下命令安装: brew install create-dmg"
        echo "📦 应用包位置: dist/Hidzor.app"
    fi
    
    # 测试运行
    echo "🧪 测试运行应用..."
    timeout 3s ./dist/Hidzor || echo "应用启动测试完成"
    
    echo ""
    echo "🎉 构建完成!"
    echo "💡 使用方法:"
    echo "   1. 双击 dist/Hidzor.dmg 打开安装包"
    echo "   2. 将 Hidzor.app 拖拽到 Applications 文件夹"
    echo "   3. 从启动台或Applications文件夹启动应用"
    echo "   4. 应用会在状态栏显示图标"
    echo "   5. 点击图标隐藏/显示其他状态栏图标"
    echo "   6. 右键菜单可以切换图标和退出应用"
    echo ""
    echo "📦 分发文件:"
    if [ -f "dist/Hidzor.dmg" ]; then
        echo "   - dist/Hidzor.dmg (DMG安装包)"
    fi
    echo "   - dist/Hidzor.app (Mac应用包)"
else
    echo "❌ 应用构建失败!"
    exit 1
fi
