# Hidzor-mac

状态栏图标隐藏工具，支持自定义图标。

## 功能

- 点击状态栏图标隐藏/显示其他状态栏图标
- 支持自定义 GIF 图标
- 右键菜单切换不同图标

## 使用方法

### 修改图标

1. 将 GIF 图标文件放入 `icons/` 目录
2. 编辑 `config.yaml` 文件：
   ```yaml
   current_icon: "icons/你的图标.gif"  # 当前使用的图标
   available_icons:
     - "icons/icons.gif"
     - "icons/你的图标.gif"
   ```
3. 重启应用或右键选择"重新加载图标"

### 右键菜单

- **选择图标**: 切换不同的图标
- **重新加载图标**: 重新加载配置文件中的图标
- **退出**: 退出应用

## 配置说明

- `current_icon`: 当前使用的图标路径
- `available_icons`: 可选择的图标列表

## 运行

```bash
python3 hidzor.py
```
