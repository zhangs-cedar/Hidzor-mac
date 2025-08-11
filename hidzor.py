#!/usr/bin/env python3
"""状态栏图标隐藏工具"""

import sys
import objc
import imageio
import yaml
import os
from Foundation import NSObject, NSTimer, NSData, NSURL
from AppKit import (NSApplication, NSStatusBar, NSMenu, NSMenuItem, NSImage, 
                    NSColor, NSSize, NSRect, NSPoint, NSBezierPath, NSView)

def get_resource_path(relative_path):
    """获取资源文件的绝对路径"""
    try:
        # PyInstaller创建临时文件夹，将路径存储在_MEIPASS中
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

def load_config():
    """加载配置文件"""
    # 首先尝试从用户目录加载配置
    home_dir = os.path.expanduser("~")
    user_config_path = os.path.join(home_dir, ".hidzor", "config.yaml")
    
    if os.path.exists(user_config_path):
        config_path = user_config_path
    else:
        # 回退到资源目录的默认配置
        config_path = get_resource_path("config.yaml")
    
    # 检查文件是否存在且不是目录
    if os.path.exists(config_path) and os.path.isfile(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                # 动态扫描icons文件夹下的所有gif文件
                config['available_icons'] = scan_gif_files()
                return config
        except Exception as e:
            print(f"配置文件读取错误: {e}")
    
    # 默认配置
    return {
        "current_icon": "icons/icons.gif",
        "available_icons": scan_gif_files()
    }

def scan_gif_files():
    """扫描icons文件夹下的所有gif文件"""
    gif_files = []
    icons_dir = get_resource_path("icons")
    
    if os.path.exists(icons_dir) and os.path.isdir(icons_dir):
        for filename in os.listdir(icons_dir):
            if filename.lower().endswith('.gif'):
                # 验证文件是否真实存在
                full_path = os.path.join(icons_dir, filename)
                if os.path.isfile(full_path):
                    gif_files.append(os.path.join("icons", filename))
    
    # 如果没有找到gif文件，返回默认图标
    if not gif_files:
        gif_files = ["icons/icons.gif"]
    
    print(f"扫描到 {len(gif_files)} 个图标文件: {gif_files}")
    return sorted(gif_files)


def save_config(config):
    """保存配置文件"""
    try:
        # 配置文件保存到用户目录
        home_dir = os.path.expanduser("~")
        config_dir = os.path.join(home_dir, ".hidzor")
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
        
        config_path = os.path.join(config_dir, "config.yaml")
        with open(config_path, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
        return True
    except Exception as e:
        print(f"配置保存错误: {e}")
        return False

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
            config = load_config()
            gif_path = config.get("current_icon", "icons/icons.gif")
            
            # 使用资源路径获取完整的图标路径
            full_gif_path = get_resource_path(gif_path)
            
            if not os.path.exists(full_gif_path):
                print(f"图标文件不存在，尝试默认图标: {gif_path}")
                full_gif_path = get_resource_path("icons/icons.gif")  # 回退到默认图标
                
                # 如果默认图标也不存在，尝试第一个可用图标
                if not os.path.exists(full_gif_path):
                    available_icons = scan_gif_files()
                    if available_icons:
                        full_gif_path = get_resource_path(available_icons[0])
                        print(f"使用第一个可用图标: {available_icons[0]}")
            
            gif_reader = imageio.get_reader(full_gif_path)
            self.gif_frames = []
            
            for frame_num, frame in enumerate(gif_reader):
                frame_image = self.numpy_to_nsimage(frame)
                if frame_image:
                    self.gif_frames.append(frame_image)
            
            gif_reader.close()
            print(f"已加载图标: {gif_path}, 共 {len(self.gif_frames)} 帧")
            
        except Exception as e:
            print(f"GIF加载错误: {e}")
            # 尝试加载默认图标
            try:
                available_icons = scan_gif_files()
                if available_icons:
                    default_path = get_resource_path(available_icons[0])
                    gif_reader = imageio.get_reader(default_path)
                    self.gif_frames = []
                    for frame in gif_reader:
                        frame_image = self.numpy_to_nsimage(frame)
                        if frame_image:
                            self.gif_frames.append(frame_image)
                    gif_reader.close()
                    print(f"已加载备用图标: {available_icons[0]}")
                else:
                    print("没有可用的图标文件")
            except Exception as e2:
                print(f"备用图标加载也失败: {e2}")
    
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
                                if r > 150 and g > 150 and b > 150:
                                    alpha = 0.0
                                else:
                                    alpha = a / 255.0
                            else:  # RGB
                                r, g, b = numpy_array[src_y, src_x]
                                if r > 150 and g > 150 and b > 150:
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
        
        # 设置菜单
        self.controller_view.menu = self.menu
        self.controller.setMenu_(self.menu)
        
        self.controller.setView_(self.controller_view)
        self.setupSeparatorIcon()
    
    def setupMenu(self):
        menu = NSMenu.alloc().init()
        
        # 图标选择子菜单
        icon_menu = NSMenu.alloc().init()
        config = load_config()
        current_icon = config.get("current_icon", "icons/icons.gif")
        available_icons = scan_gif_files()  # 动态扫描
        
        # 验证当前图标是否在可用列表中
        if current_icon not in available_icons:
            current_icon = available_icons[0] if available_icons else "icons/icons.gif"
        
        for icon_path in available_icons:
            # 验证图标文件是否真实存在
            full_icon_path = get_resource_path(icon_path)
            if not os.path.exists(full_icon_path):
                print(f"跳过不存在的图标: {icon_path}")
                continue
                
            icon_name = os.path.basename(icon_path)
            icon_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(icon_name, "switchIcon:", "")
            icon_item.setTarget_(self)
            icon_item.setRepresentedObject_(icon_path)
            
            # 设置当前选中的图标
            if icon_path == current_icon:
                icon_item.setState_(1)  # NSOnState
            else:
                icon_item.setState_(0)  # NSOffState
                
            icon_menu.addItem_(icon_item)
        
        # 图标选择菜单项
        icon_menu_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("选择图标", "", "")
        icon_menu_item.setSubmenu_(icon_menu)
        menu.addItem_(icon_menu_item)
        
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
    def switchIcon_(self, sender):
        """切换图标"""
        try:
            new_icon_path = sender.representedObject()
            if new_icon_path:
                # 使用资源路径检查文件是否存在
                full_icon_path = get_resource_path(new_icon_path)
                if os.path.exists(full_icon_path):
                    # 更新配置
                    config = load_config()
                    config["current_icon"] = new_icon_path
                    if save_config(config):
                        # 重新加载图标
                        self.controller_view.loadGifFrames()
                        print(f"已切换到图标: {new_icon_path}")
                        
                        # 更新菜单状态
                        self.updateMenuStates()
                    else:
                        print("配置保存失败")
                else:
                    print(f"图标文件不存在: {full_icon_path}")
            else:
                print("无效的图标路径")
        except Exception as e:
            print(f"切换图标失败: {e}")
    
    def updateMenuStates(self):
        """更新菜单选中状态"""
        try:
            config = load_config()
            current_icon = config.get("current_icon", "icons/icons.gif")
            
            # 更新图标选择子菜单的状态
            icon_menu = self.menu.itemAtIndex_(0).submenu()
            for i in range(icon_menu.numberOfItems()):
                item = icon_menu.itemAtIndex_(i)
                icon_path = item.representedObject()
                if icon_path == current_icon:
                    item.setState_(1)  # NSOnState
                else:
                    item.setState_(0)  # NSOffState
        except Exception as e:
            print(f"更新菜单状态失败: {e}")
    
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
