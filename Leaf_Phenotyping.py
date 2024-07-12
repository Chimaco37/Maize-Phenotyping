import tkinter as tk
from tkinter import StringVar, END, Listbox, Scrollbar, Menu
import os
from gui_functions import selectPath, update_original_pics, show_pics, model_inference_thread, update_results_from_excel
from language_support import get_language_text, lang
import webbrowser
from PIL import Image, ImageTk


def update_language(language):
    global lang
    lang = language
    # 删除并重新添加菜单项以更新标签
    menubar.delete(0, tk.END)

    # 重新添加路径设置菜单
    menubar.add_cascade(label=get_language_text(lang, "path_settings"), menu=path_menu)
    # 重新添加语言选择菜单
    menubar.add_cascade(label=get_language_text(lang, "change_language"), menu=language_menu)
    # 重新添加帮助(About)菜单
    menubar.add_cascade(label=get_language_text(lang, "about"), menu=help_menu)

    # 更新路径设置菜单项标签
    path_menu.entryconfig(0, label=get_language_text(lang, "select_image_path"))
    path_menu.entryconfig(1, label=get_language_text(lang, "change_output_directory"))

    # 更新帮助菜单项标签
    help_menu.entryconfig(0, label=get_language_text(lang, "help"))

    # 更新按钮文本
    btn_model_inference.config(text=get_language_text(lang,"model_inference"))

    # 更新数据标签
    data_labels_keys = ["leaf_width"]
    for key in data_labels_keys:
        label_text = get_language_text(lang, key)
        data_labels[key]["label"].config(text=label_text)


def refresh_img_list():
    global original_img_paths
    original_img_paths = update_original_pics(pic_path_var)
    listbox_pics.delete(0, END)
    for path in original_img_paths:
        listbox_pics.insert(END, path)

def handle_listbox_select(event):
    global label
    # threading.Event().wait(0.1)
    selection = event.widget.curselection()
    if selection:
        index = selection[0]
        original_projection_path = original_img_paths[index]
        label = original_projection_path.split('\\')[-1].split('.')[0]

        # 模型预测前后图片的格式是一样的，之后要保持一致为jpg格式
        predicted_projection_path = os.path.join(result_path_var.get(), 'marker', label + '.jpg')
        original_ear_path = os.path.join(result_path_var.get(), 'transformed', label + '.jpg')
        predicted_ear_path = os.path.join(result_path_var.get(), 'leaf', label + '.jpg')

        show_pics(original_projection_path, canvas_projection_original)
        show_pics(original_ear_path, canvas_ear_original)
        show_pics(predicted_projection_path, canvas_projection_analyzed)
        show_pics(predicted_ear_path, canvas_ear_analyzed)

        update_results_from_excel(label, result_path_var, data_labels)


root = tk.Tk()
root.title("Leaf Phenotyping")
root.iconbitmap("logo/leaf_logo.ico")

# 设置顶部行：控制按钮、结果展示、文本输出
top_frame = tk.Frame(root)
top_frame.pack(side=tk.TOP, fill=tk.X, expand=True)

# 文件路径变量
pic_path_var = StringVar(value="./images/")

pic_path_var.trace("w", lambda name, index, mode: refresh_img_list())  # 当 pic_path_var 更新时，调用 refresh_video_list
result_path_var = StringVar(value="./runs/segment/")
model_path_var = StringVar(value="./models/")

# 菜单栏设置
menubar = Menu(root)
root.config(menu=menubar)

# 创建路径设置菜单
path_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label=get_language_text(lang, "path_settings"), menu=path_menu)

# 添加菜单项
path_menu.add_command(label=get_language_text(lang, "select_image_path"), command=lambda: selectPath(pic_path_var, get_language_text(lang, "select_image_path_prompt")))
path_menu.add_command(label=get_language_text(lang, "select_result_path"), command=lambda: selectPath(result_path_var, get_language_text(lang, "select_result_path_prompt")))

# 创建语言选择菜单
language_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label=get_language_text(lang, "change_language"), menu=language_menu)
language_menu.add_command(label="English", command=lambda: update_language("English"))
language_menu.add_command(label="中文", command=lambda: update_language("中文"))

# 创建帮助(About)菜单
help_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label=get_language_text(lang, "about"), menu=help_menu)
help_menu.add_command(label=get_language_text(lang, "help"), command=lambda: webbrowser.open("https://github.com/Chimaco37/Maize-Phenotyping"))

# 控制按钮
control_frame = tk.Frame(top_frame)
control_frame.pack(side=tk.LEFT, padx=0, pady=10, expand=True)

btn_model_inference = tk.Button(control_frame, text=get_language_text(lang, "model_inference"), font=('等线', 15), width=15, height=3, command=lambda: model_inference_thread(pic_path_var, result_path_var, text_output))
btn_model_inference.pack(padx=0, pady=5)

# 结果展示模块
result_frame = tk.Frame(top_frame)
result_frame.pack(side=tk.LEFT, padx= 2, pady=10, expand=True)

data_labels = {
    "leaf_width": {"var": tk.StringVar(), "label": None},
}

# 当创建标签时，保存引用
for key, item in data_labels.items():
    item["var"].set("N/A")
    frame = tk.Frame(result_frame)
    frame.pack(fill=tk.X, expand=True)
    label = tk.Label(frame, text=f"{key}:", width=8, font=('等线', 12))
    label.pack(side=tk.LEFT)
    value_label = tk.Label(frame, textvariable=item["var"], width=8, font=('等线', 12))
    value_label.pack(side=tk.RIGHT)
    item["label"] = label  # 保存标签控件的引用

# 文本输出
text_output = tk.Text(top_frame, height=10, width=70)
text_output.pack(side=tk.LEFT, padx=0, pady=10)

# logo展示
logo_show = tk.Frame(top_frame)
logo_show.pack_propagate(False)  # 禁用自动调整大小
logo_show.pack(side=tk.LEFT, padx=5, pady=10, expand=True, fill=tk.BOTH)

# 等待控制框架的高度设置完成
root.update_idletasks()

# 设置logo_show的高度与控制框架的高度一致
logo_show.config(height=control_frame.winfo_reqheight())

# 获取logo_show的大小
logo_show_height = logo_show.winfo_height()
logo_show_width = logo_show_height + 5

# 加载并调整PNG图片大小
image_path = "./logo/leaf_logo.png"  # 替换为你的图片路径
image = Image.open(image_path)
image = image.resize((logo_show_width, logo_show_height), Image.LANCZOS)  # 调整图片大小
photo = ImageTk.PhotoImage(image)

# 创建一个标签来展示图片
label = tk.Label(logo_show, image=photo)
label.image = photo  # 保持引用，避免被垃圾回收
label.pack(expand=True)


# 设置底部行：视频展示画布和目录
bottom_frame = tk.Frame(root)
bottom_frame.pack(side=tk.TOP, fill=tk.BOTH)

# 视频播放画布
pic_display_frame = tk.Frame(bottom_frame)
pic_display_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

# 创建四个画布
canvas_projection_original = tk.Canvas(pic_display_frame, width=427, height=320)
canvas_projection_original.grid(row=0, column=0, padx=10, pady=10)

canvas_projection_analyzed = tk.Canvas(pic_display_frame, width=427, height=320)
canvas_projection_analyzed.grid(row=1, column=0, padx=10, pady=10)

canvas_ear_original = tk.Canvas(pic_display_frame, width=640 , height=320)
canvas_ear_original.grid(row=0, column=1, padx=15, pady=10)

canvas_ear_analyzed = tk.Canvas(pic_display_frame, width=640 , height=320)
canvas_ear_analyzed.grid(row=1, column=1, padx=15, pady=10)

# 目录模块
listbox_frame = tk.Frame(bottom_frame, bd=2, relief=tk.GROOVE)
listbox_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True)
scrollbar = Scrollbar(listbox_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
listbox_pics = Listbox(listbox_frame, yscrollcommand=scrollbar.set)
listbox_pics.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.config(command=listbox_pics.yview)
listbox_pics.bind('<Double-1>', handle_listbox_select)

refresh_img_list()
update_language(lang)

root.mainloop()
