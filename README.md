# 陈狗四方连续图片2x2拼接工具

## 功能简介
本工具用于将一张图片拼接成2x2的四方连续图案，支持批量处理，支持拖拽添加任务，支持选择输出格式（png、jpg、jpeg），并可自定义输出文件夹和文件名。
![Uploading image.png…]()

## 软件特性
- 支持批量拖拽图片到窗口，自动加入任务队列
- 支持选择输出文件夹
- 支持选择输出图片格式（png、jpg、jpeg）
- 支持自定义输出文件名（可选用源文件名）
- 任务队列右键可一键清空
- 进度条与状态栏实时显示处理进度
- 一键“执行任务”按钮，手动开始批量处理

## 使用方法
1. 双击运行 `seamless_tile_gui.exe`（首次打开窗口已自动适配所有控件显示）
2. 拖拽一张或多张图片到窗口，图片将加入任务队列
3. 可右键任务队列，选择“清空队列”
4. 选择输出文件夹、输出格式、是否使用源文件名
5. 点击“执行任务”按钮，开始批量拼接处理
6. 处理完成后，图片将输出到指定文件夹

## 支持的图片格式
- 输入：png、jpg、jpeg、bmp、tiff、gif
- 输出：png、jpg、jpeg（可选）

## 依赖环境
- Python 3.10 及以上
- 依赖包：Pillow、TkinterDnD2、tkinter（标准库）

可通过如下命令安装依赖：
```
pip install -r requirements.txt
```

## 打包方法
1. 确保已安装 PyInstaller：
   ```
   pip install pyinstaller
   ```
2. 使用如下命令打包（需在虚拟环境中执行）：
   ```
   .\venv\Scripts\pyinstaller.exe --onefile --noconsole --icon=window.ico --add-data "window.ico;." seamless_tile_gui.py
   ```
3. 打包完成后，`dist` 目录下生成 `seamless_tile_gui.exe`

## 常见问题
- **拖拽无反应**：请确保已安装 TkinterDnD2，且在 Windows 系统下运行。
- **图标不显示或报错**：请确保 window.ico 文件存在，且打包时已用 `--add-data` 参数。
- **任务队列无法清空**：请用鼠标右键点击任务队列区域，选择“清空队列”。
- **窗口控件显示不全**：已优化初始窗口高度，如仍有问题请手动拉大窗口。

## 联系方式
如有问题或建议，请联系开发者。 
