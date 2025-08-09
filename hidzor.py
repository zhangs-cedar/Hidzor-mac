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
        return self
    
    def mouseDown_(self, event):
        if self.callback:
            self.callback()
    
    def drawRect_(self, rect):
        NSColor.whiteColor().setFill()
        dot_rect = NSRect(NSPoint(5, 5), NSSize(6, 6))
        NSBezierPath.bezierPathWithOvalInRect_(dot_rect).fill()


class DozerStatusIcon(NSObject):
    def init(self):
        self = objc.super(DozerStatusIcon, self).init()
        if self:
            self.normal_length = 25
            self.status_item = NSStatusBar.systemStatusBar().statusItemWithLength_(self.normal_length)
            self.is_hiding_others = False
            self.setup_icon()
            self.setup_menu()
        return self
    
    def setup_icon(self):
        view = ClickableStatusView.alloc().initWithFrame_callback_(
            NSRect(NSPoint(0, 0), NSSize(22, 22)), self.toggle_hiding
        )
        self.status_item.setView_(view)
    
    def setup_menu(self):
        menu = NSMenu.alloc().init()
        
        show_all = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("显示所有", "show_all:", "")
        show_all.setTarget_(self)
        menu.addItem_(show_all)
        
        menu.addItem_(NSMenuItem.separatorItem())
        
        quit_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("退出", "quit:", "q")
        quit_item.setTarget_(self)
        menu.addItem_(quit_item)
        
        self.status_item.setMenu_(menu)
    
    def toggle_hiding(self):
        if self.is_hiding_others:
            self.show_others()
        else:
            self.hide_others()
    
    def hide_others(self):
        if not self.is_hiding_others:
            self.is_hiding_others = True
            # 使用较小的隐藏长度，确保自己图标仍可见
            self.status_item.setLength_(500.0)
    
    def show_others(self):
        if self.is_hiding_others:
            self.is_hiding_others = False
            self.status_item.setLength_(self.normal_length)
    
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
