#!/usr/bin/env python3
"""构建Mac应用的脚本"""

import os
import shutil
import subprocess
import sys

def clean_build():
    """清理构建文件"""
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"已清理: {dir_name}")

def install_deps():
    """安装依赖"""
    print("安装依赖...")
    subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])

def build_app():
    """构建应用"""
    print("开始构建Mac应用...")
    
    # PyInstaller命令
    cmd = [
        'pyinstaller',
        '--onefile',  # 打包成单个文件
        '--windowed',  # 无控制台窗口
        '--name=Hidzor',  # 应用名称
        '--icon=icons/icons.gif',  # 应用图标
        '--add-data=icons:icons',  # 包含icons目录
        '--add-data=config.yaml:config.yaml',  # 包含配置文件
        '--hidden-import=imageio.plugins.ffmpeg',  # 隐式导入
        '--hidden-import=imageio.plugins.pillow',
        '--hidden-import=imageio.plugins.gif',
        'hidzor.py'
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ 构建成功!")
        print("应用位置: dist/Hidzor")
    else:
        print("❌ 构建失败:")
        print(result.stderr)
        return False
    
    return True

def create_dmg():
    """创建DMG安装包"""
    print("创建DMG安装包...")
    
    # 检查是否有create-dmg工具
    try:
        subprocess.run(['which', 'create-dmg'], capture_output=True, check=True)
    except subprocess.CalledProcessError:
        print("⚠️  未找到create-dmg工具，跳过DMG创建")
        print("可以通过以下命令安装: brew install create-dmg")
        return
    
    # 创建DMG
    cmd = [
        'create-dmg',
        '--volname=Hidzor',
        '--window-pos=200,120',
        '--window-size=600,400',
        '--icon-size=100',
        '--icon=Hidzor.app=175,120',
        '--hide-extension=Hidzor.app',
        '--app-drop-link=425,120',
        'dist/Hidzor.dmg',
        'dist/Hidzor.app'
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ DMG创建成功!")
        print("DMG位置: dist/Hidzor.dmg")
    else:
        print("❌ DMG创建失败:")
        print(result.stderr)

def main():
    """主函数"""
    print("🚀 开始构建Hidzor Mac应用...")
    
    # 清理
    clean_build()
    
    # 安装依赖
    install_deps()
    
    # 构建应用
    if build_app():
        # 创建DMG
        create_dmg()
        
        print("\n🎉 构建完成!")
        print("📁 应用文件: dist/Hidzor")
        print("📦 DMG文件: dist/Hidzor.dmg (如果创建成功)")
        print("\n💡 使用说明:")
        print("1. 双击Hidzor应用运行")
        print("2. 应用会在状态栏显示图标")
        print("3. 点击图标隐藏/显示其他状态栏图标")
        print("4. 右键菜单可以切换图标和退出应用")
    else:
        print("❌ 构建失败，请检查错误信息")

if __name__ == "__main__":
    main()
