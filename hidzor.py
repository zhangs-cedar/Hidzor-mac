#!/usr/bin/env python3
"""状态栏图标隐藏工具"""

import sys
import objc
import imageio
from Foundation import NSObject, NSTimer, NSData, NSURL
from AppKit import (NSApplication, NSStatusBar, NSMenu, NSMenuItem, NSImage, 
                    NSColor, NSSize, NSRect, NSPoint, NSBezierPath, NSView)

class ClickableStatusView(NSView):
    def initWithFrame_callback_(self, frame, callback):
        self = objc.super(ClickableStatusView, self).initWithFrame_(frame)
        if self:
            self.callback = callback
            self.is_hiding = False
            self.frame = 0
            self.gif_frames = []
            self.current_frame = 0
            self.loadGifFrames()
            self.timer = NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(
                0.1, self, "updateFrame:", None, True
            )
        return self
    
    def loadGifFrames(self):
        try:
            # 使用imageio加载GIF文件
            gif_path = "icons.gif"
            gif_reader = imageio.get_reader(gif_path)
            self.gif_frames = []
            
            for frame_num, frame in enumerate(gif_reader):
                # 将numpy数组转换为NSImage
                frame_image = self.numpy_to_nsimage(frame)
                if frame_image:
                    self.gif_frames.append(frame_image)
            
            gif_reader.close()
            print(f"Loaded {len(self.gif_frames)} GIF frames")
            
        except Exception as e:
            print(f"GIF load error: {e}")
    
    def numpy_to_nsimage(self, numpy_array):
        try:
            # 确保图像是RGB格式
            if len(numpy_array.shape) == 3:
                height, width, channels = numpy_array.shape
                if channels == 4:  # RGBA
                    # 转换为RGB
                    rgb_array = numpy_array[:, :, :3]
                else:
                    rgb_array = numpy_array
                
                # 创建NSImage
                image = NSImage.alloc().initWithSize_(NSSize(22, 22))
                image.lockFocus()
                
                # 缩放并绘制图像
                scale_x = width / 22.0
                scale_y = height / 22.0
                
                for y in range(22):
                    for x in range(22):
                        # 计算原图对应位置
                        src_x = int(x * scale_x)
                        src_y = int(y * scale_y)
                        
                        if src_x < width and src_y < height:
                            r, g, b = rgb_array[src_y, src_x]
                            color = NSColor.colorWithCalibratedRed_green_blue_alpha_(
                                r/255.0, g/255.0, b/255.0, 1.0
                            )
                            color.setFill()
                            rect = NSRect(NSPoint(x, 21-y), NSSize(1, 1))
                            NSBezierPath.bezierPathWithRect_(rect).fill()
                
                image.unlockFocus()
                return image
        except Exception as e:
            print(f"Convert error: {e}")
            return None
    
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
            if self.gif_frames:
                self.current_frame = (self.current_frame + 1) % len(self.gif_frames)
            else:
                self.frame = (self.frame + 1) % 8
            self.setNeedsDisplay_(True)
        except Exception as e:
            print(f"Animation error: {e}")
    
    def drawRect_(self, rect):
        if self.gif_frames:
            self.drawGifIcon()
        else:
            self.drawCat()
    
    def drawGifIcon(self):
        try:
            if self.current_frame < len(self.gif_frames):
                frame_image = self.gif_frames[self.current_frame]
                frame_image.drawInRect_(NSRect(NSPoint(0, 0), NSSize(22, 22)))
        except Exception as e:
            print(f"GIF draw error: {e}")
            # 如果GIF绘制失败，回退到猫头
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
            self.separator.setAction_("showOthers:")
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
