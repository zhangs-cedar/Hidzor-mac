#!/usr/bin/env python3
"""状态栏图标隐藏工具"""

import sys
import objc
from Foundation import NSObject
from AppKit import (NSApplication, NSStatusBar, NSMenu, NSMenuItem, NSImage, 
                    NSColor, NSSize, NSRect, NSPoint, NSBezierPath, NSView)

class ClickableStatusView(NSView):
    def initWithFrame_callback_(self, frame, callback):
        self = objc.super(ClickableStatusView, self).initWithFrame_(frame)
        if self:
            self.callback = callback
            self.is_hiding = False
        return self
    
    def mouseDown_(self, event):
        if self.callback:
            self.callback()
    
    def setHidingState_(self, hiding):
        self.is_hiding = hiding
        self.setNeedsDisplay_(True)
    
    def drawRect_(self, rect):
        if self.is_hiding:
            # 隐藏状态：显示眼睛图标
            self.drawEyeIcon()
        else:
            # 显示状态：显示隐藏图标
            self.drawHideIcon()
    
    def drawEyeIcon(self):
        # 绘制眼睛图标（显示状态）
        NSColor.whiteColor().setFill()
        # 眼睛轮廓
        eye_rect = NSRect(NSPoint(3, 4), NSSize(16, 10))
        eye_path = NSBezierPath.bezierPathWithOvalInRect_(eye_rect)
        eye_path.setLineWidth_(1.5)
        eye_path.stroke()
        # 瞳孔
        pupil_rect = NSRect(NSPoint(7, 6), NSSize(6, 6))
        NSBezierPath.bezierPathWithOvalInRect_(pupil_rect).fill()
    
    def drawHideIcon(self):
        # 绘制隐藏图标（隐藏状态）
        NSColor.whiteColor().setFill()
        # 斜线
        line1 = NSBezierPath.bezierPath()
        line1.moveToPoint_(NSPoint(4, 4))
        line1.lineToPoint_(NSPoint(18, 16))
        line1.setLineWidth_(2)
        line1.stroke()
        
        line2 = NSBezierPath.bezierPath()
        line2.moveToPoint_(NSPoint(18, 4))
        line2.lineToPoint_(NSPoint(4, 16))
        line2.setLineWidth_(2)
        line2.stroke()


class DozerStatusIcon(NSObject):
    def init(self):
        self = objc.super(DozerStatusIcon, self).init()
        if self:
            # 创建分隔符（用于隐藏左侧图标）
            self.separator = NSStatusBar.systemStatusBar().statusItemWithLength_(8)
            # 创建控制器（保持可见用于操作）  
            self.controller = NSStatusBar.systemStatusBar().statusItemWithLength_(25)
            self.is_hiding_others = False
            self.setup_icons()
            self.setup_menu()
        return self
    
    def setup_icons(self):
        # 设置控制器图标（动态图标）
        self.controller_view = ClickableStatusView.alloc().initWithFrame_callback_(
            NSRect(NSPoint(0, 0), NSSize(22, 22)), self.toggle_hiding
        )
        self.controller.setView_(self.controller_view)
        
        # 设置分隔符图标（显示为小圆点）
        self.setup_separator_icon()
    
    def setup_menu(self):
        menu = NSMenu.alloc().init()
        
        show_all = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("显示所有", "show_all:", "")
        show_all.setTarget_(self)
        menu.addItem_(show_all)
        
        menu.addItem_(NSMenuItem.separatorItem())
        
        quit_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("退出", "quit:", "q")
        quit_item.setTarget_(self)
        menu.addItem_(quit_item)
        
        self.controller.setMenu_(menu)
    
    def setup_separator_icon(self):
        # 创建分隔符图标（小圆点）
        image = NSImage.alloc().initWithSize_(NSSize(8, 8))
        image.lockFocus()
        NSColor.grayColor().setFill()
        rect = NSRect(NSPoint(1, 1), NSSize(6, 6))
        NSBezierPath.bezierPathWithOvalInRect_(rect).fill()
        image.unlockFocus()
        image.setTemplate_(True)
        self.separator.setImage_(image)
    
    def toggle_hiding(self):
        if self.is_hiding_others:
            self.show_others()
        else:
            self.hide_others()
    
    def hide_others(self):
        if not self.is_hiding_others:
            self.is_hiding_others = True
            # 扩展分隔符来隐藏左侧图标，并隐藏分隔符图标
            self.separator.setLength_(500.0)
            self.separator.setImage_(None)
            # 更新控制器图标状态
            self.controller_view.setHidingState_(True)
    
    def show_others(self):
        if self.is_hiding_others:
            self.is_hiding_others = False
            # 恢复分隔符正常大小，并显示分隔符图标
            self.separator.setLength_(8)
            self.setup_separator_icon()
            # 更新控制器图标状态
            self.controller_view.setHidingState_(False)
    
    @objc.IBAction
    def show_all_(self, sender):
        self.show_others()
    
    @objc.IBAction
    def quit_(self, sender):
        if self.is_hiding_others:
            self.show_others()
        NSApplication.sharedApplication().terminate_(None)


def main():
    app = NSApplication.sharedApplication()
    app.setActivationPolicy_(2)
    DozerStatusIcon.alloc().init()
    app.run()

if __name__ == "__main__":
    main()
