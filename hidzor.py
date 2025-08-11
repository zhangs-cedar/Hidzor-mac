#!/usr/bin/env python3
"""状态栏图标隐藏工具"""

import sys
import objc
import time
from Foundation import NSObject, NSTimer
from AppKit import (NSApplication, NSStatusBar, NSMenu, NSMenuItem, NSImage, 
                    NSColor, NSSize, NSRect, NSPoint, NSBezierPath, NSView)

class ClickableStatusView(NSView):
    def initWithFrame_callback_(self, frame, callback):
        self = objc.super(ClickableStatusView, self).initWithFrame_(frame)
        if self:
            self.callback = callback
            self.is_hiding = False
            self.animation_frame = 0
            self.animation_timer = None
            self.start_animation()
        return self
    
    def mouseDown_(self, event):
        if self.callback:
            self.callback()
    
    def rightMouseDown_(self, event):
        # 处理右键点击，显示菜单
        if hasattr(self, 'menu') and self.menu:
            self.menu.popUpMenuPositioningItem_atLocation_inView_(
                None, event.locationInWindow(), self
            )
    
    def setHidingState_(self, hiding):
        self.is_hiding = hiding
        self.setNeedsDisplay_(True)
    
    def start_animation(self):
        print("启动招财猫动画...")
        # 启动招财猫动画定时器
        self.animation_timer = NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(
            0.2, self, "updateAnimation:", None, True
        )
        print("动画已启动")
    
    def updateAnimation_(self, sender):
        try:
            # 更新动画帧
            self.animation_frame = (self.animation_frame + 1) % 8
            # 招财猫动画（招财手势摆动）
            self.setNeedsDisplay_(True)
        except Exception as e:
            print(f"Animation error: {e}")
    
    def drawRect_(self, rect):
        if self.is_hiding:
            # 隐藏状态：显示招财猫动画
            self.drawLuckyCatAnimation()
        else:
            # 显示状态：显示招财猫动画
            self.drawLuckyCatAnimation()
    
    def drawLuckyCatAnimation(self):
        try:
            # 绘制招财猫动画
            # 背景
            NSColor.clearColor().setFill()
            background_rect = NSBezierPath.bezierPathWithRect_(NSRect(NSPoint(0, 0), NSSize(22, 22)))
            background_rect.fill()
            
            # 绘制招财猫
            self.drawLuckyCat()
            
            # 绘制招财手势（带摆动动画）
            self.drawLuckyPaw()
        except Exception as e:
            print(f"Draw error: {e}")
    
    def drawLuckyCat(self):
        try:
            # 绘制精致的招财猫
            NSColor.whiteColor().setFill()
            
            # 身体（圆形）
            body_rect = NSRect(NSPoint(6, 6), NSSize(10, 10))
            NSBezierPath.bezierPathWithOvalInRect_(body_rect).fill()
            
            # 头部（圆形）
            head_rect = NSRect(NSPoint(5, 12), NSSize(8, 8))
            NSBezierPath.bezierPathWithOvalInRect_(head_rect).fill()
            
            # 猫耳朵（三角形）
            ear1 = NSBezierPath.bezierPath()
            ear1.moveToPoint_(NSPoint(5, 20))
            ear1.lineToPoint_(NSPoint(3, 22))
            ear1.lineToPoint_(NSPoint(7, 20))
            ear1.closePath()
            ear1.fill()
            
            ear2 = NSBezierPath.bezierPath()
            ear2.moveToPoint_(NSPoint(9, 20))
            ear2.lineToPoint_(NSPoint(11, 22))
            ear2.lineToPoint_(NSPoint(7, 20))
            ear2.closePath()
            ear2.fill()
            
            # 眼睛（椭圆形，更可爱）
            NSColor.blackColor().setFill()
            eye1_rect = NSRect(NSPoint(6, 15), NSSize(1.5, 2))
            NSBezierPath.bezierPathWithOvalInRect_(eye1_rect).fill()
            
            eye2_rect = NSRect(NSPoint(8.5, 15), NSSize(1.5, 2))
            NSBezierPath.bezierPathWithOvalInRect_(eye2_rect).fill()
            
            # 鼻子（粉色小圆点）
            NSColor.systemPinkColor().setFill()
            nose_rect = NSRect(NSPoint(7.25, 14), NSSize(1, 1))
            NSBezierPath.bezierPathWithOvalInRect_(nose_rect).fill()
            
            # 铃铛（金色）
            NSColor.systemYellowColor().setFill()
            bell_rect = NSRect(NSPoint(7.5, 8), NSSize(3, 3))
            NSBezierPath.bezierPathWithOvalInRect_(bell_rect).fill()
            
            # 铃铛中心点
            NSColor.blackColor().setFill()
            bell_center = NSRect(NSPoint(8.25, 8.5), NSSize(0.5, 0.5))
            NSBezierPath.bezierPathWithOvalInRect_(bell_center).fill()
            
            # 胡须（黑色细线）
            NSColor.blackColor().setStroke()
            whisker1 = NSBezierPath.bezierPath()
            whisker1.moveToPoint_(NSPoint(4, 14))
            whisker1.lineToPoint_(NSPoint(2, 14))
            whisker1.setLineWidth_(0.5)
            whisker1.stroke()
            
            whisker2 = NSBezierPath.bezierPath()
            whisker2.moveToPoint_(NSPoint(4, 13))
            whisker2.lineToPoint_(NSPoint(2, 13))
            whisker2.setLineWidth_(0.5)
            whisker2.stroke()
            
            whisker3 = NSBezierPath.bezierPath()
            whisker3.moveToPoint_(NSPoint(10, 14))
            whisker3.lineToPoint_(NSPoint(12, 14))
            whisker3.setLineWidth_(0.5)
            whisker3.stroke()
            
            whisker4 = NSBezierPath.bezierPath()
            whisker4.moveToPoint_(NSPoint(10, 13))
            whisker4.lineToPoint_(NSPoint(12, 13))
            whisker4.setLineWidth_(0.5)
            whisker4.stroke()
            
        except Exception as e:
            print(f"Lucky cat draw error: {e}")
    
    def drawLuckyPaw(self):
        try:
            # 绘制招财手势（带摆动动画）
            NSColor.whiteColor().setFill()
            
            # 招财手势位置（根据动画帧摆动）
            paw_angle = (self.animation_frame * 20) % 40 - 20  # -20到20度摆动
            paw_x = 18 + 1.5 * (paw_angle / 20)  # 手势位置随角度变化
            
            # 绘制招财手势（圆形爪子）
            paw_rect = NSRect(NSPoint(paw_x - 1, 4), NSSize(2, 2))
            NSBezierPath.bezierPathWithOvalInRect_(paw_rect).fill()
            
            # 绘制招财手势的爪子细节
            NSColor.blackColor().setFill()
            paw_detail1 = NSRect(NSPoint(paw_x - 0.5, 4.5), NSSize(0.3, 0.3))
            NSBezierPath.bezierPathWithOvalInRect_(paw_detail1).fill()
            
            paw_detail2 = NSRect(NSPoint(paw_x + 0.2, 4.5), NSSize(0.3, 0.3))
            NSBezierPath.bezierPathWithOvalInRect_(paw_detail2).fill()
            
            # 绘制招财手势的连接线
            NSColor.whiteColor().setStroke()
            connection = NSBezierPath.bezierPath()
            connection.moveToPoint_(NSPoint(16, 8))
            connection.lineToPoint_(NSPoint(paw_x, 5))
            connection.setLineWidth_(1.5)
            connection.stroke()
            
        except Exception as e:
            print(f"Lucky paw draw error: {e}")


class DozerStatusIcon(NSObject):
    def init(self):
        print("初始化状态栏图标...")
        self = objc.super(DozerStatusIcon, self).init()
        if self:
            # 创建分隔符（用于隐藏左侧图标）
            print("创建分隔符...")
            self.separator = NSStatusBar.systemStatusBar().statusItemWithLength_(8)
            # 创建控制器（保持可见用于操作）  
            print("创建控制器...")
            self.controller = NSStatusBar.systemStatusBar().statusItemWithLength_(25)
            self.is_hiding_others = False
            self.setup_menu()  # 先创建菜单
            self.setup_icons()  # 再设置图标
            print("状态栏图标初始化完成")
        return self
    
    def setup_icons(self):
        print("设置图标...")
        # 设置控制器图标（动态图标）
        self.controller_view = ClickableStatusView.alloc().initWithFrame_callback_(
            NSRect(NSPoint(0, 0), NSSize(22, 22)), self.toggle_hiding
        )
        
        # 将菜单传递给视图，用于右键点击
        if hasattr(self, 'menu'):
            self.controller_view.menu = self.menu
            self.controller.setMenu_(self.menu)
        
        self.controller.setView_(self.controller_view)
        
        # 设置分隔符图标（显示为小圆点）
        self.setup_separator_icon()
        print("图标设置完成")
    
    def setup_menu(self):
        print("创建菜单...")
        menu = NSMenu.alloc().init()
        
        show_all = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("显示所有", "show_all:", "")
        show_all.setTarget_(self)
        menu.addItem_(show_all)
        
        menu.addItem_(NSMenuItem.separatorItem())
        
        quit_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("退出", "quit:", "q")
        quit_item.setTarget_(self)
        menu.addItem_(quit_item)
        
        self.menu = menu  # 保存菜单引用
        print("菜单创建完成")
        return menu
    
    def setup_separator_icon(self):
        print("设置分隔符图标...")
        # 创建分隔符图标（小圆点）
        image = NSImage.alloc().initWithSize_(NSSize(8, 8))
        image.lockFocus()
        NSColor.grayColor().setFill()
        rect = NSRect(NSPoint(1, 1), NSSize(6, 6))
        NSBezierPath.bezierPathWithOvalInRect_(rect).fill()
        image.unlockFocus()
        image.setTemplate_(True)
        self.separator.setImage_(image)
        print("分隔符图标设置完成")
    
    def toggle_hiding(self):
        print("切换隐藏状态...")
        if self.is_hiding_others:
            self.show_others()
        else:
            self.hide_others()
    
    def hide_others(self):
        if not self.is_hiding_others:
            print("隐藏其他图标...")
            self.is_hiding_others = True
            # 扩展分隔符来隐藏左侧图标，并隐藏分隔符图标
            self.separator.setLength_(500.0)
            self.separator.setImage_(None)
            # 为隐藏区域添加点击事件
            self.separator.setTarget_(self)
            self.separator.setAction_("show_all:")
            # 更新控制器图标状态
            self.controller_view.setHidingState_(True)
            print("其他图标已隐藏")
    
    def show_others(self):
        if self.is_hiding_others:
            print("显示所有图标...")
            self.is_hiding_others = False
            # 恢复分隔符正常大小，并显示分隔符图标
            self.separator.setLength_(8)
            self.setup_separator_icon()
            # 移除隐藏区域的点击事件
            self.separator.setTarget_(None)
            self.separator.setAction_(None)
            # 更新控制器图标状态
            self.controller_view.setHidingState_(False)
            print("所有图标已显示")
    
    @objc.IBAction
    def show_all_(self, sender):
        print("菜单：显示所有")
        self.show_others()
    
    @objc.IBAction
    def quit_(self, sender):
        print("菜单：退出程序")
        if self.is_hiding_others:
            self.show_others()
        # 停止动画定时器
        if hasattr(self.controller_view, 'animation_timer') and self.controller_view.animation_timer:
            self.controller_view.animation_timer.invalidate()
        NSApplication.sharedApplication().terminate_(None)


def main():
    print("启动 Hidzor 状态栏工具...")
    app = NSApplication.sharedApplication()
    app.setActivationPolicy_(2)
    DozerStatusIcon.alloc().init()
    print("程序启动完成，正在运行...")
    app.run()

if __name__ == "__main__":
    main()
