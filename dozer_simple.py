#!/usr/bin/env python3
"""
Dozer Python版 - 状态栏图标隐藏工具
"""

import sys
import objc
from Foundation import NSObject, NSTimer, NSUserDefaults
from AppKit import (NSApplication, NSStatusBar, NSStatusItem, NSMenu, NSMenuItem, 
                    NSImage, NSColor, NSSize, NSRect, NSPoint, NSBezierPath, NSVariableStatusItemLength,
                    NSSquareStatusItemLength, NSEventTrackingRunLoopMode, NSView, NSLeftMouseDown, NSEvent)
# 移除 PyQt6 依赖，完全使用原生 macOS API

class ClickableStatusView(NSView):
    """可点击的状态栏视图"""
    
    def initWithFrame_callback_(self, frame, callback):
        self = objc.super(ClickableStatusView, self).initWithFrame_(frame)
        if self is None:
            return None
        self.callback = callback
        print("🔧 创建可点击视图")
        return self
    
    def mouseDown_(self, event):
        """处理鼠标点击"""
        print("🖱️ 视图检测到鼠标点击！")
        if self.callback:
            self.callback()
    
    def drawRect_(self, rect):
        """绘制视图"""
        # 绘制白色圆点
        NSColor.whiteColor().setFill()
        dot_rect = NSRect(NSPoint(5, 5), NSSize(6, 6))
        circle = NSBezierPath.bezierPathWithOvalInRect_(dot_rect)
        circle.fill()


class DozerStatusIcon(NSObject):
    """Dozer状态栏图标 - 使用原生 macOS API"""
    
    def init(self):
        self = objc.super(DozerStatusIcon, self).init()
        if self is None:
            return None
        
        self.normal_length = 25  # 正常长度
        self.hide_length = 10000.0  # 隐藏长度
        
        # 创建单个状态栏图标
        self.status_item = NSStatusBar.systemStatusBar().statusItemWithLength_(self.normal_length)
        self.is_hiding_others = False
        
        self.setup_icon()
        self.setup_menu()
        
        return self
    
    def setup_icon(self):
        """设置图标"""
        print("🔧 开始设置状态栏图标...")
        
        # 方法1: 尝试使用自定义视图
        try:
            print("🔧 尝试方法1: 自定义视图")
            view = ClickableStatusView.alloc().initWithFrame_callback_(
                NSRect(NSPoint(0, 0), NSSize(22, 22)), 
                self.on_click
            )
            self.status_item.setView_(view)
            print("✅ 方法1成功: 使用自定义视图")
            return
        except Exception as e:
            print(f"❌ 方法1失败: {e}")
        
        # 方法2: 传统的图标+动作方式
        try:
            print("🔧 尝试方法2: 传统图标+动作")
            # 创建图标
            image = NSImage.alloc().initWithSize_(NSSize(16, 16))
            image.lockFocus()
            NSColor.whiteColor().setFill()
            rect = NSRect(NSPoint(5, 5), NSSize(6, 6))
            circle = NSBezierPath.bezierPathWithOvalInRect_(rect)
            circle.fill()
            image.unlockFocus()
            image.setTemplate_(True)
            
            self.status_item.setImage_(image)
            self.status_item.setToolTip_("Dozer - 点击隐藏/显示左侧图标")
            
            # 尝试不同的动作设置方式
            self.status_item.setTarget_(self)
            self.status_item.setAction_("on_click:")
            print("✅ 方法2成功: 传统方式")
            
        except Exception as e:
            print(f"❌ 方法2失败: {e}")
        
        # 确保长度正确设置
        self.status_item.setLength_(self.normal_length)
        print(f"🔍 最终事件目标: {self.status_item.target()}")
        print(f"🔍 最终事件动作: {self.status_item.action()}")
    
    def setup_menu(self):
        """设置右键菜单"""
        menu = NSMenu.alloc().init()
        
        # 显示所有图标
        show_all_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            "显示所有图标", "show_all:", "")
        show_all_item.setTarget_(self)
        menu.addItem_(show_all_item)
        
        menu.addItem_(NSMenuItem.separatorItem())
        
        # 退出
        quit_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            "退出", "quit:", "q")
        quit_item.setTarget_(self)
        menu.addItem_(quit_item)
        
        self.status_item.setMenu_(menu)
    
    def on_click(self):
        """点击回调 - 无参数版本"""
        print("🎯 =======点击事件触发(无参数)======= 🎯")
        print("🖱️ 视图点击回调被调用")
        self.toggle_hiding_core()
    
    def on_click_(self, sender):
        """点击回调 - 带参数版本"""
        print("🎯 =======点击事件触发(带参数)======= 🎯")
        print(f"🖱️ 发送者: {sender}")
        print("🖱️ 状态栏项点击回调被调用")
        self.toggle_hiding_core()
    
    def toggle_hiding_core(self):
        """核心切换逻辑"""
        print(f"📊 当前状态: {'隐藏中' if self.is_hiding_others else '显示中'}")
        print(f"📏 当前长度: {self.status_item.length()}")
        
        if self.is_hiding_others:
            print("➡️ 执行显示操作")
            self.show_others()
        else:
            print("➡️ 执行隐藏操作")
            self.hide_others()
        
        print(f"📏 操作后长度: {self.status_item.length()}")
        print("🎯 =======点击事件结束======= 🎯")
    
    # 确保方法可以被 Objective-C 运行时发现
    on_click_ = objc.selector(on_click_, signature=b'v@:@')
    
    # 添加测试方法
    @objc.IBAction
    def test_click_(self, sender):
        """测试点击方法"""
        print("🧪 测试点击方法被调用!")
        self.on_click_(sender)
    
    # 添加兼容性方法
    @objc.IBAction  
    def statusItemClicked_(self, sender):
        """状态栏项点击方法（兼容性）"""
        print("🧪 兼容性点击方法被调用!")
        self.on_click_(sender)
    
    def hide_others(self):
        """隐藏其他图标 - 使用长度扩展机制"""
        if not self.is_hiding_others:
            self.is_hiding_others = True
            print(f"🔧 隐藏模式：开始隐藏操作")
            
            try:
                # 设置非常大的长度来推挤其他图标到屏幕外
                print(f"🔧 设置隐藏长度: {self.hide_length}")
                self.status_item.setLength_(self.hide_length)
                
                # 更新提示
                if hasattr(self.status_item, 'setToolTip_'):
                    self.status_item.setToolTip_("Dozer - 点击显示隐藏的图标")
                
                print(f"✅ 隐藏操作成功")
                    
            except Exception as e:
                print(f"❌ 隐藏失败: {e}")
                # 重置状态
                self.is_hiding_others = False
            
            print(f"🙈 隐藏操作完成，状态: {self.is_hiding_others}")
    
    def show_others(self):
        """显示其他图标"""
        if self.is_hiding_others:
            self.is_hiding_others = False
            print(f"🔧 显示模式：开始显示操作")
            
            try:
                # 恢复正常长度
                self.status_item.setLength_(self.normal_length)
                
                print(f"🔧 恢复正常长度: {self.normal_length}")
                
                # 更新提示
                if hasattr(self.status_item, 'setToolTip_'):
                    self.status_item.setToolTip_("Dozer - 点击隐藏/显示左侧图标")
                
                print(f"✅ 显示操作成功")
                
            except Exception as e:
                print(f"❌ 显示失败: {e}")
            
            print(f"👁️ 显示操作完成，状态: {self.is_hiding_others}")
    
    @objc.IBAction
    def show_all_(self, sender):
        """显示所有图标"""
        self.show_others()
    
    @objc.IBAction
    def quit_(self, sender):
        """退出应用"""
        print("🔚 正在退出应用...")
        # 恢复正常状态
        if self.is_hiding_others:
            self.show_others()
        NSApplication.sharedApplication().terminate_(None)


class DozerApp:
    """Dozer应用主类 - 使用原生 macOS API"""
    
    def __init__(self):
        # 初始化 Cocoa 应用
        self.app = NSApplication.sharedApplication()
        self.app.setActivationPolicy_(2)  # NSApplicationActivationPolicyAccessory
        
        # 创建 Dozer 状态栏图标
        self.dozer_icon = DozerStatusIcon.alloc().init()
    
    def run(self):
        """运行应用"""
        print("🔵 Dozer Python版已启动（原生 macOS API）")
        print("📍 在状态栏中找到 Dozer 图标（白色圆点）")
        print("👆 点击图标 = 隐藏/显示左侧的状态栏图标")
        print("💡 使用方法：")
        print("   1. 按住 ⌘ 键拖动其他应用图标到 Dozer 图标左侧")
        print("   2. 点击 Dozer 图标即可隐藏左侧所有图标")
        print("   3. 再次点击可以重新显示隐藏的图标")
        print("✨ 现在使用真正的 macOS NSStatusItem API，应该能正确隐藏图标了！")
        
        # 运行应用主循环
        self.app.run()


def main():
    """主函数"""
    app = DozerApp()
    sys.exit(app.run())


if __name__ == "__main__":
    main()
