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
            self.gif_frames = []
            self.current_frame = 0
            self.loadGifFrames()
            self.timer = NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(
                0.1, self, "updateFrame:", None, True
            )
        return self
    
    def loadGifFrames(self):
        try:
            gif_path = "icons.gif"
            gif_reader = imageio.get_reader(gif_path)
            self.gif_frames = []
            
            for frame_num, frame in enumerate(gif_reader):
                frame_image = self.numpy_to_nsimage(frame)
                if frame_image:
                    self.gif_frames.append(frame_image)
            
            gif_reader.close()
            print(f"Loaded {len(self.gif_frames)} GIF frames")
            
        except Exception as e:
            print(f"GIF load error: {e}")
    
    def numpy_to_nsimage(self, numpy_array):
        try:
            if len(numpy_array.shape) == 3:
                height, width, channels = numpy_array.shape
                
                image = NSImage.alloc().initWithSize_(NSSize(22, 22))
                image.lockFocus()
                
                scale_x = width / 22.0
                scale_y = height / 22.0
                
                for y in range(22):
                    for x in range(22):
                        src_x = int(x * scale_x)
                        src_y = int(y * scale_y)
                        
                        if src_x < width and src_y < height:
                            if channels == 4:  # RGBA
                                r, g, b, a = numpy_array[src_y, src_x]
                                if r > 100 and g > 100 and b > 100:
                                    alpha = 0.0
                                else:
                                    alpha = a / 255.0
                            else:  # RGB
                                r, g, b = numpy_array[src_y, src_x]
                                if r > 100 and g > 100 and b > 100:
                                    alpha = 0.0
                                else:
                                    alpha = 1.0
                            
                            if alpha > 0:
                                color = NSColor.colorWithCalibratedRed_green_blue_alpha_(
                                    1, 1, 1, alpha
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
            self.setNeedsDisplay_(True)
        except Exception as e:
            print(f"Animation error: {e}")
    
    def drawRect_(self, rect):
        self.drawGifIcon()
    
    def drawGifIcon(self):
        try:
            if self.gif_frames and self.current_frame < len(self.gif_frames):
                frame_image = self.gif_frames[self.current_frame]
                frame_image.drawInRect_(NSRect(NSPoint(0, 0), NSSize(22, 22)))
        except Exception as e:
            print(f"GIF draw error: {e}")


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
