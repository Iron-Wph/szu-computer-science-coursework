import torch
from torch import nn
from torchvision.models import alexnet, googlenet, vgg19
from torchvision.transforms import transforms

import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox as msg
from tkinter import filedialog as filedialog
from tkinter import ttk


class Window:
    def __init__(self, w=800, h=700):
        # 主窗口
        self.window = tk.Tk(className='肺炎感染影像智能识别')
        self.window.geometry(f'{w}x{h}')
        self.window.resizable(0, 0)

        # 标题
        self.title = tk.Label(self.window, text='肺炎感染影像智能识别', font=("", 18))
        self.title.pack(pady=5)

        self.init_frame()

        # 加载模型
        self.alex = alexnet()
        self.alex.classifier = nn.Sequential(
            nn.Dropout(p=0.5),
            nn.Linear(256 * 6 * 6, 4096),
            nn.ReLU(inplace=True),
            nn.Dropout(p=0.5),
            nn.Linear(4096, 4096),
            nn.ReLU(inplace=True),
            nn.Linear(4096, 2),
        )
        self.alex.eval()
        state = torch.load(
            r"D:\作业\大四\计算机视觉\大作业\code\cv-big-homework\alex\alex\alex_70_0.0003.pth",
            map_location="cpu"
        )
        self.alex.load_state_dict(state)
        
        self.google = googlenet(aux_logits=False, transform_input=True)
        self.google.fc = nn.Linear(1024, 2)
        self.google.eval()
        state = torch.load(
            r"D:\作业\大四\计算机视觉\大作业\code\cv-big-homework\google\google_70_0.0003.pth", map_location="cpu"
        )
        self.google.load_state_dict(state)

        self.vgg = vgg19()
        self.vgg.classifier = nn.Sequential(
            nn.Linear(512 * 7 * 7, 4096),
            nn.ReLU(True),
            nn.Dropout(p=0.5),
            nn.Linear(4096, 4096),
            nn.ReLU(True),
            nn.Dropout(p=0.5),
            nn.Linear(4096, 2),
        )
        self.vgg.eval()
        state = torch.load(
            r"D:\作业\大四\计算机视觉\大作业\code\cv-big-homework\vgg\vgg_100_0.0001.pth",   
            map_location="cpu"
        )
        self.vgg.load_state_dict(state)

        self.window.mainloop()

    def init_frame(self):
        # 控制面板
        self.init_control_frame()
        # 显示区域
        self.init_show_frame()

        self.image = None


    def init_control_frame(self):
        """添加控制面板"""
        self.control_frame = tk.LabelFrame(self.window, text='控制面板', width=200, height=600, font=("", 15))
        self.control_frame.place(x=50, y=50)

        self.bt_choice_im = tk.Button(self.control_frame, text='选择图像', width=22, height=4, command=self.choice_image)
        self.bt_choice_im.place(x=15, y=85)

        self.bt_cnn = tk.Button(self.control_frame, text='CNN识别', width=22, height=4, command=self.cnn)
        self.bt_cnn.place(x=15, y=235)

        self.bt_exit = tk.Button(self.control_frame, text='退出系统', width=22, height=4, command=self.exit_sys)
        self.bt_exit.place(x=15, y=385)

    def init_show_frame(self):
        """添加显示区域窗口"""
        self.show_frame = tk.LabelFrame(self.window, text='显示面板', width=500, height=600, font=("", 15))
        self.show_frame.place(x=250, y=50)

        self.image_tk = ImageTk.PhotoImage(Image.new("RGB", (int(384 * 1.2), int(224 * 1.2)), (179, 199, 255)))
        self.image_label = tk.Label(self.show_frame, image=self.image_tk, relief="solid", borderwidth=1)
        self.image_label.place(x=15, y=10)

        self.table_style = ttk.Style()
        self.table_style.configure("Treeview", rowheight=50)

        self.table = ttk.Treeview(self.show_frame, show='headings', height=4)
        self.table["columns"] = ("模型名称", "识别结果")
        self.table.column("模型名称", width=230, anchor='center')
        self.table.column("识别结果", width=230, anchor='center')
        self.table.heading("模型名称", text="模型名称", anchor='center')
        self.table.heading("识别结果", text="识别结果", anchor='center')
        self.table.place(x=15, y=300)

        self.table.insert('', 0, values=("AlexNet", ""))
        self.table.insert('', 1, values=("GoogleNet", ""))
        self.table.insert('', 2, values=("VGGNet", ""))
        self.table.insert('', 3, values=("融合模型", ""))

    def choice_image(self):
        # 初始化工作
        self.init_frame()
        # 选择文件
        file_path = filedialog.askopenfilename(initialdir='./')

        if file_path:
            if file_path.split('.')[-1] not in {"jpg", "png"}:
                msg.showerror(message='文件格式不支持')
            else:
                # 加载图像
                image = Image.open(file_path).convert('RGB')
                self.image = image.copy()

                self.image_tk = ImageTk.PhotoImage(image.resize((self.image_tk.width(), self.image_tk.height())))
                self.image_label['image'] = self.image_tk


    def preprocess(self, image: Image.Image):
        trans = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
        ])
        image = trans(image)
        return torch.unsqueeze(image, 0)

    def pred2idx(self, pred):
        _, predicted = torch.max(pred.data, 1)
        predicted = predicted.detach().cpu().numpy().tolist()
        return predicted[0]

    def cnn(self):
        image = self.preprocess(self.image)
        alex_pred = self.alex(image)
        alex_pred = self.pred2idx(alex_pred)

        google_pred = self.google(image)
        google_pred = self.pred2idx(google_pred)

        vgg_pred = self.google(image)
        vgg_pred = self.pred2idx(vgg_pred)

        fuse_pred = 1 if sum([alex_pred, google_pred, vgg_pred]) >= 2 else 0
        if fuse_pred == 0:
            fuse_pred = vgg_pred

        id2cls = {0: "肺炎阳性", 1: "肺炎阴性"}

        alex_pred = id2cls[alex_pred]
        google_pred = id2cls[google_pred]
        vgg_pred = id2cls[vgg_pred]
        fuse_pred = id2cls[fuse_pred]

        self.table.insert('', 0, values=("AlexNet", f"判断{alex_pred}"))
        self.table.insert('', 1, values=("GoogleNet", f"判断{google_pred}"))
        self.table.insert('', 2, values=("VGGNet", f"判断{vgg_pred}"))
        self.table.insert('', 3, values=("融合模型", f"判断{fuse_pred}"))

    def exit_sys(self):
        if msg.askyesno('提示', '是否退出系统'):
            exit()


w = Window()
