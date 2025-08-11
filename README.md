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
   ```
3. 重启应用，系统会自动扫描 `icons/` 目录下的所有 GIF 文件

### 右键菜单

- **选择图标**: 切换不同的图标（自动扫描 `icons/` 目录）
- **退出**: 退出应用

## 配置说明

- `current_icon`: 当前使用的图标路径
- `available_icons`: 系统会自动扫描 `icons/` 目录下的所有 GIF 文件

## 运行

### 开发环境运行

```bash
python3 hidzor.py
```

### 打包成Mac应用

#### 方法一：构建DMG安装包（推荐）

```bash
# 一键构建DMG安装包
./build_dmg.sh
```

#### 方法二：基础构建

```bash
# 基础构建
./build.sh
```

#### 方法三：手动构建

```bash
# 安装依赖
pip3 install -r requirements.txt

# 使用PyInstaller构建
pyinstaller Hidzor.spec
```

#### 构建结果

构建完成后，在 `dist/` 目录下会生成：
- `Hidzor` - 可执行文件
- `Hidzor.app` - Mac应用包
- `Hidzor.dmg` - DMG安装包（如果使用build_dmg.sh）

#### 安装和使用

1. **DMG安装包**（推荐）：
   - 双击 `dist/Hidzor.dmg` 打开安装包
   - 将 `Hidzor.app` 拖拽到 Applications 文件夹
   - 从启动台或Applications文件夹启动应用

2. **直接运行**：
   - 双击 `dist/Hidzor.app` 或 `dist/Hidzor` 运行
   - 首次运行可能需要授予辅助功能权限

## 系统要求

- macOS 10.13 或更高版本
- Python 3.7+（仅开发环境需要）

## 注意事项

1. 首次运行可能需要授予辅助功能权限
2. 应用会在状态栏显示，不会在Dock中显示
3. 配置文件会自动保存在应用目录下
4. 支持Intel和Apple Silicon芯片
