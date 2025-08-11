import imageio
from Foundation import NSObject, NSTimer, NSData, NSURL
from AppKit import (NSApplication, NSStatusBar, NSMenu, NSMenuItem, NSImage, 
                    NSColor, NSSize, NSRect, NSPoint, NSBezierPath, NSView)

def numpy_to_nsimage( numpy_array):
    try:
        # 确保图像是RGB格式
        if len(numpy_array.shape) == 3:
            height, width, channels = numpy_array.shape
            
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
                        if channels == 4:  # RGBA
                            r, g, b, a = numpy_array[src_y, src_x]
                            # 检测白色背景 (RGB值都接近255)
                            if r > 240 and g > 240 and b > 240:
                                alpha = 0.0  # 透明
                            else:
                                alpha = a / 255.0
                        else:  # RGB
                            r, g, b = numpy_array[src_y, src_x]
                            # 检测白色背景
                            if r > 240 and g > 240 and b > 240:
                                alpha = 0.0  # 透明
                            else:
                                alpha = 1.0
                        
                        if alpha > 0:  # 只绘制非透明像素
                            color = NSColor.colorWithCalibratedRed_green_blue_alpha_(
                                r/255.0, g/255.0, b/255.0, alpha
                            )
                            color.setFill()
                            rect = NSRect(NSPoint(x, 21-y), NSSize(1, 1))
                            NSBezierPath.bezierPathWithRect_(rect).fill()
            image.unlockFocus()
            return image
    except Exception as e:
        print(f"Convert error: {e}")
        return None



# 使用imageio加载GIF文件
gif_path = "icons.gif"
gif_reader = imageio.get_reader(gif_path)
gif_frames = []

for frame_num, frame in enumerate(gif_reader):
    # 将numpy数组转换为NSImage
    frame_image = numpy_to_nsimage(frame)
    if frame_image:
        gif_frames.append(frame_image)

gif_reader.close()
