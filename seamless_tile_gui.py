print("程序已启动")

import os
import threading
from tkinter import Tk, Label, messagebox, filedialog, StringVar, BooleanVar, Checkbutton, Button, Entry, Listbox, END, SINGLE, IntVar, OptionMenu
from tkinter import ttk
from PIL import Image
from tkinterdnd2 import DND_FILES, TkinterDnD
import sys

import tkinter  # 保证Menu可用

def create_2x2_tile(input_image_path, output_image_path, out_format):
    try:
        with Image.open(input_image_path) as img:
            width, height = img.size
            new_image = Image.new(img.mode, (width * 2, height * 2))
            new_image.paste(img, (0, 0))
            new_image.paste(img, (width, 0))
            new_image.paste(img, (0, height))
            new_image.paste(img, (width, height))
            save_kwargs = {}
            if out_format == 'png':
                save_kwargs['compress_level'] = 0
            new_image.save(output_image_path, format=out_format.upper(), **save_kwargs)
        return True, output_image_path
    except Exception as e:
        return False, str(e)

def create_tile_grid(input_image_path, output_image_path, out_format, rows, cols):
    try:
        with Image.open(input_image_path) as img:
            width, height = img.size
            new_width = width * cols
            new_height = height * rows
            new_image = Image.new(img.mode, (new_width, new_height))
            for i in range(cols):
                for j in range(rows):
                    new_image.paste(img, (i * width, j * height))
            save_kwargs = {}
            if out_format == 'png':
                save_kwargs['compress_level'] = 0
            new_image.save(output_image_path, format=out_format.upper(), **save_kwargs)
        return True, output_image_path
    except Exception as e:
        return False, str(e)

def parse_drop_files(files):
    # 支持多文件拖拽，返回文件路径列表
    if files.startswith('{') and files.endswith('}'):
        # 多文件格式：{file1} {file2} ...
        return [f for f in files.strip('{}').split('} {')]
    else:
        return files.split()

def on_drop(event):
    files = parse_drop_files(event.data)
    # 只保留图片文件
    image_files = [f for f in files if os.path.isfile(f) and os.path.splitext(f)[1].lower() in [".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".gif"]]
    if not image_files:
        messagebox.showerror("错误", "请拖入图片文件！")
        return
    out_dir = output_dir_var.get()
    if not out_dir or not os.path.isdir(out_dir):
        messagebox.showerror("错误", "请选择有效的输出文件夹！")
        return
    # 加入任务队列
    for f in image_files:
        task_listbox.insert(END, f)
        task_queue.append(f)
    # 拖拽后不自动执行

def select_output_dir():
    dir_selected = filedialog.askdirectory(title="选择输出文件夹")
    if dir_selected:
        output_dir_var.set(dir_selected)

def process_next_task():
    if not task_queue:
        progress_var.set(0)
        status_var.set("全部处理完成！")
        return
    processing_flag[0] = True
    file_path = task_queue.pop(0)
    idx = task_listbox.get(0, END).index(file_path)
    task_listbox.itemconfig(idx, {'bg':'#e6f7ff'})
    out_dir = output_dir_var.get()
    use_src_name = use_src_name_var.get()
    out_format = output_format_var.get()
    rows = row_var.get()
    cols = col_var.get()
    ext = out_format
    if use_src_name:
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        out_name = f"{base_name}.{ext}"
    else:
        out_name = f"陈狗四方连续{rows}x{cols}.{ext}"
    output_path = os.path.join(out_dir, out_name)
    status_var.set(f"正在处理：{os.path.basename(file_path)}")
    def do_process():
        success, msg = create_tile_grid(file_path, output_path, out_format, rows, cols)
        if success:
            task_listbox.itemconfig(idx, {'bg':'#d4ffd4'})
        else:
            task_listbox.itemconfig(idx, {'bg':'#ffd4d4'})
            messagebox.showerror("错误", f"处理失败：\n{msg}")
        # 更新进度
        total = task_listbox.size()
        finished = total - len(task_queue)
        progress_var.set(int(finished / total * 100))
        if task_queue:
            root.after(100, process_next_task)
        else:
            processing_flag[0] = False
            status_var.set("全部处理完成！")
    threading.Thread(target=do_process).start()

def main():
    global output_dir_var, use_src_name_var, task_listbox, task_queue, progress_var, status_var, processing_flag, root, output_format_var, row_var, col_var
    root = TkinterDnD.Tk()
    # 初始化全局变量
    row_var = IntVar(value=2)
    col_var = IntVar(value=2)
    root.title("陈狗四方连续图片拼接工具（批量拖拽，任务栏进度）")
    root.geometry("600x520")  # 增大高度，确保所有控件可见
    
    import os
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
        # 修正打包时的图标路径
        ico_path = os.path.join(base_path, 'window.ico')
    else:
        base_path = os.path.dirname(__file__)
        ico_path = os.path.join(base_path, 'window.ico')
    root.iconbitmap(ico_path)
    label = Label(root, text="请将四方连续图片文件拖到此窗口\n支持批量拖拽，自动生成陈狗四方连续拼接图", font=("微软雅黑", 13), width=60, height=3, relief="ridge", borderwidth=2)
    label.pack(padx=20, pady=10, expand=False, fill="x")
    label.drop_target_register(DND_FILES)
    label.dnd_bind('<<Drop>>', on_drop)

    # 输出文件夹选择
    output_dir_var = StringVar(value=os.getcwd())
    out_dir_frame = Label(root)
    out_dir_frame.pack(pady=5, fill="x", padx=20)
    Entry(out_dir_frame, textvariable=output_dir_var, width=40, state="normal").pack(side="left", padx=(0,5))
    Button(out_dir_frame, text="选择输出文件夹", command=select_output_dir).pack(side="left")

    # 输出格式选择
    output_format_var = StringVar(value="png")
    format_frame = Label(root)
    format_frame.pack(pady=5, fill="x", padx=20)
    Label(format_frame, text="输出格式：").pack(side="left")
    OptionMenu(format_frame, output_format_var, "png", "jpg", "jpeg").pack(side="left")
    Label(format_frame, text="行数：").pack(side="left", padx=(10, 2))
    Entry(format_frame, textvariable=row_var, width=5).pack(side="left", padx=(0, 10))
    Label(format_frame, text="列数：").pack(side="left", padx=(10, 2))
    Entry(format_frame, textvariable=col_var, width=5).pack(side="left")

    # 是否使用源文件名
    use_src_name_var = BooleanVar(value=True)
    Checkbutton(root, text="输出文件名使用源图片名", variable=use_src_name_var).pack(pady=5)

    # 任务栏
    Label(root, text="任务队列：", font=("微软雅黑", 10)).pack(anchor="w", padx=20)
    task_listbox = Listbox(root, selectmode=SINGLE, width=80, height=8)
    task_listbox.pack(padx=20, pady=5, fill="x")

    # 右键菜单：清空队列
    def clear_task_queue():
        task_listbox.delete(0, END)
        task_queue.clear()
    menu = None
    def show_context_menu(event):
        nonlocal menu
        if menu is None:
            menu = tkinter.Menu(root, tearoff=0)
            menu.add_command(label="清空队列", command=clear_task_queue)
        menu.tk_popup(event.x_root, event.y_root)
    task_listbox.bind("<Button-3>", show_context_menu)

    # 定义执行任务函数
    def execute_tasks():
        global row_var, col_var
        if not processing_flag[0] and task_queue:
            rows = row_var.get()
            cols = col_var.get()
            if rows < 1 or cols < 1:
                messagebox.showerror("错误", "行数和列数必须至少为1")
                return
            process_next_task()
        elif not task_queue:
            messagebox.showinfo("提示", "任务队列为空！")
        else:
            messagebox.showinfo("提示", "任务正在处理中，请稍候。")

    # 执行按钮
    Button(root, text="执行任务", command=execute_tasks, bg="#4CAF50", fg="white", font=("微软雅黑", 11)).pack(pady=5)

    # 进度条
    progress_var = IntVar(value=0)
    progressbar = ttk.Progressbar(root, variable=progress_var, maximum=100)
    progressbar.pack(fill="x", padx=20, pady=5)

    # 状态栏
    status_var = StringVar(value="等待任务...")
    Label(root, textvariable=status_var, font=("微软雅黑", 10)).pack(anchor="w", padx=20, pady=(0,10))

    # 任务队列和处理标志
    task_queue = []
    processing_flag = [False]

    root.mainloop()

if __name__ == "__main__":
    main()