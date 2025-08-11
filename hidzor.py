#!/usr/bin/env python3
"""状态栏图标隐藏工具"""

import sys
import objc
from Foundation import NSObject, NSTimer
from AppKit import (NSApplication, NSStatusBar, NSMenu, NSMenuItem, NSImage, 
                    NSColor, NSSize, NSRect, NSPoint, NSBezierPath, NSView)

class ClickableStatusView(NSView):
    def initWithFrame_callback_(self, frame, callback):
        self = objc.super(ClickableStatusView, self).initWithFrame_(frame)
        if self:
            self.callback = callback
            self.is_hiding = False
            self.frame = 0
            self.timer = NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(
                0.2, self, "updateFrame:", None, True
            )
        return self
    
    def mouseDown_(self, event):
        if self.callback:
            self.callback()
    
    def rightMouseDown_(self, event):
        if hasattr(self, 'menu') and self.menu:
            self.menu.popUpMenuPositioningItem_atLocation_inView_(
                None, event.locationInWindow(), self
            )
    
    def setHidingState_(self, hiding):
        self.is_hiding = hiding
        self.setNeedsDisplay_(True)
    
    def updateFrame_(self, sender):
        try:
            self.frame = (self.frame + 1) % 8
            self.setNeedsDisplay_(True)
        except Exception as e:
            print(f"Animation error: {e}")
    
    def drawRect_(self, rect):
        self.drawCat()
    
    def drawCat(self):
        try:
            # 背景
            NSColor.clearColor().setFill()
            NSBezierPath.bezierPathWithRect_(NSRect(NSPoint(0, 0), NSSize(22, 22))).fill()
            
            # 猫身体
            NSColor.whiteColor().setFill()
            NSBezierPath.bezierPathWithOvalInRect_(NSRect(NSPoint(6, 6), NSSize(10, 10))).fill()
            
            # 猫头
            NSBezierPath.bezierPathWithOvalInRect_(NSRect(NSPoint(5, 12), NSSize(8, 8))).fill()
            
            # 耳朵
            for i, points in enumerate([[(5, 20), (3, 22), (7, 20)], [(9, 20), (11, 22), (7, 20)]]):
                ear = NSBezierPath.bezierPath()
                ear.moveToPoint_(NSPoint(*points[0]))
                ear.lineToPoint_(NSPoint(*points[1]))
                ear.lineToPoint_(NSPoint(*points[2]))
                ear.closePath()
                ear.fill()
            
            # 眼睛
            NSColor.blackColor().setFill()
            for x in [6, 8.5]:
                NSBezierPath.bezierPathWithOvalInRect_(NSRect(NSPoint(x, 15), NSSize(1.5, 2))).fill()
            
            # 鼻子
            NSColor.systemPinkColor().setFill()
            NSBezierPath.bezierPathWithOvalInRect_(NSRect(NSPoint(7.25, 14), NSSize(1, 1))).fill()
            
            # 铃铛
            NSColor.systemYellowColor().setFill()
            NSBezierPath.bezierPathWithOvalInRect_(NSRect(NSPoint(7.5, 8), NSSize(3, 3))).fill()
            NSColor.blackColor().setFill()
            NSBezierPath.bezierPathWithOvalInRect_(NSRect(NSPoint(8.25, 8.5), NSSize(0.5, 0.5))).fill()
            
            # 胡须
            NSColor.blackColor().setStroke()
            for whisker in [(4, 14, 2), (4, 13, 2), (10, 14, 12), (10, 13, 12)]:
                path = NSBezierPath.bezierPath()
                path.moveToPoint_(NSPoint(whisker[0], whisker[1]))
                path.lineToPoint_(NSPoint(whisker[2], whisker[1]))
                path.setLineWidth_(0.5)
                path.stroke()
            
            # 招财手势
            paw_angle = (self.frame * 20) % 40 - 20
            paw_x = 18 + 1.5 * (paw_angle / 20)
            
            NSColor.whiteColor().setFill()
            NSBezierPath.bezierPathWithOvalInRect_(NSRect(NSPoint(paw_x - 1, 4), NSSize(2, 2))).fill()
            
            NSColor.blackColor().setFill()
            for dx in [-0.5, 0.2]:
                NSBezierPath.bezierPathWithOvalInRect_(NSRect(NSPoint(paw_x + dx, 4.5), NSSize(0.3, 0.3))).fill()
            
            NSColor.whiteColor().setStroke()
            connection = NSBezierPath.bezierPath()
            connection.moveToPoint_(NSPoint(16, 8))
            connection.lineToPoint_(NSPoint(paw_x, 5))
            connection.setLineWidth_(1.5)
            connection.stroke()
            
        except Exception as e:
            print(f"Draw error: {e}")


class DozerStatusIcon(NSObject):
    def init(self):
        self = objc.super(DozerStatusIcon, self).init()
        if self:
            self.separator = NSStatusBar.systemStatusBar().statusItemWithLength_(8)
            self.controller = NSStatusBar.systemStatusBar().statusItemWithLength_(25)
            self.is_hiding_others = False
            self.setupMenu()
            self.setupIcons()
        return self
    
    def setupIcons(self):
        self.controller_view = ClickableStatusView.alloc().initWithFrame_callback_(
            NSRect(NSPoint(0, 0), NSSize(22, 22)), self.toggleHiding
        )
        
        if hasattr(self, 'menu'):
            self.controller_view.menu = self.menu
            self.controller.setMenu_(self.menu)
        
        self.controller.setView_(self.controller_view)
        self.setupSeparatorIcon()
    
    def setupMenu(self):
        menu = NSMenu.alloc().init()
        
        show_all = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("显示所有", "showAll:", "")
        show_all.setTarget_(self)
        menu.addItem_(show_all)
        
        menu.addItem_(NSMenuItem.separatorItem())
        
        quit_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("退出", "quit:", "q")
        quit_item.setTarget_(self)
        menu.addItem_(quit_item)
        
        self.menu = menu
        return menu
    
    def setupSeparatorIcon(self):
        image = NSImage.alloc().initWithSize_(NSSize(8, 8))
        image.lockFocus()
        NSColor.grayColor().setFill()
        NSBezierPath.bezierPathWithOvalInRect_(NSRect(NSPoint(1, 1), NSSize(6, 6))).fill()
        image.unlockFocus()
        image.setTemplate_(True)
        self.separator.setImage_(image)
    
    def toggleHiding(self):
        if self.is_hiding_others:
            self.showOthers()
        else:
            self.hideOthers()
    
    def hideOthers(self):
        if not self.is_hiding_others:
            self.is_hiding_others = True
            self.separator.setLength_(10000.0)
            self.separator.setImage_(None)
            self.separator.setTarget_(self)
            self.separator.setAction_("showAll:")
            self.controller_view.setHidingState_(True)
    
    def showOthers(self):
        if self.is_hiding_others:
            self.is_hiding_others = False
            self.separator.setLength_(8)
            self.setupSeparatorIcon()
            self.separator.setTarget_(None)
            self.separator.setAction_(None)
            self.controller_view.setHidingState_(False)
    
    @objc.IBAction
    def showAll_(self, sender):
        self.showOthers()
    
    @objc.IBAction
    def quit_(self, sender):
        if self.is_hiding_others:
            self.showOthers()
        if hasattr(self.controller_view, 'timer') and self.controller_view.timer:
            self.controller_view.timer.invalidate()
        NSApplication.sharedApplication().terminate_(None)


def main():
    app = NSApplication.sharedApplication()
    app.setActivationPolicy_(2)
    DozerStatusIcon.alloc().init()
    app.run()

if __name__ == "__main__":
    main()
