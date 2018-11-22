from tkinter.ttk import Button,Entry,Scrollbar,Radiobutton
from tkinter import Tk,StringVar,Label,END,Listbox,BROWSE,SINGLE,IntVar
import time
import os,re
from 播放器_test import music_get
from tkinter.filedialog import askdirectory
from tkinter import messagebox
import random
import mp3play
import pygame

class App(object):
    def __init__(self):
        self.win=Tk()
        self.win.geometry('405x380')
        self.win.title("网易云mp3播放下载器")
        self.creat_res()
        self.res_config()
        self.win.mainloop()

    def creat_res(self):
        self.music_temp=StringVar(value="(.)(.)")
        self.mp3_lis=[] #备用
        self.temp=StringVar()#url输入框
        self.temp2=IntVar() #单选框 播放或者下载
        self.temp3=StringVar()#path 输入框
        self.T_message=Listbox(self.win,background="#EEE9E9")
        self.B_search=Button(self.win,text="搜索")
        self.B_path=Button(self.win,text="选择目录")
        self.E_song=Entry(self.win,textvariable=self.temp)
        self.E_path=Entry(self.win,textvariable=self.temp3)
        self.Play_button=Button(self.win,text="播放")
        self.Pause_button=Button(self.win,textvariable=self.music_temp)
        self.Temp_button=Button(self.win,text="单曲下载")
        self.Stop_button=Button(self.win,text="停止")
        self.Info=Button(self.win,text="说明")
        self.More_down=Button(self.win,text="歌单批量下载")
        self.B_search_loacl=Button(self.win,text="扫描本地歌曲")
        self.S_bal=Scrollbar(self.win)
        self.R_1=Radiobutton(self.win,variable=self.temp2,text="下载",value=True)
        self.R_2=Radiobutton(self.win,variable=self.temp2,text="播放",value=False)
        self.L_mp3_message=Label(self.win,background="#EEE9E9",fg="#9370DB")
        self.B_search.place(x=340,y=5,width=50,height=30)
        self.E_song.place(x=10,y=10,width=300,height=35)
        self.T_message.place(x=10,y=165,width=280,height=200)
        self.Play_button.place(x=340,y=160,width=50,height=40)
        self.Pause_button.place(x=340,y=209,width=50,height=40)
        self.Temp_button.place(x=130,y=125,width=100,height=30)
        self.S_bal.place(x=286,y=165,width=20,height=200)
        self.E_path.place(x=10,y=70,width=200,height=40)
        self.B_path.place(x=230,y=75,width=60,height=38)
        self.L_mp3_message.place(x=241,y=125,width=152,height=30)
        self.Info.place(x=340,y=315,width=50,height=40)
        self.More_down.place(x=10,y=125,width=100,height=30)
        self.B_search_loacl.place(x=300,y=75,width=100,height=38)
        self.R_1.place(x=265,y=50,width=60,height=25)
        self.R_2.place(x=340,y=50,width=60,height=25)
        self.Stop_button.place(x=340,y=260,width=50,height=40)

    def res_config(self):
        self.B_search.config(command=self.get_lis)
        self.S_bal.config(command=self.T_message.yview)
        self.T_message["yscrollcommand"]=self.S_bal.set
        self.T_message.config(selectmode=BROWSE)
        self.B_path.config(command=self.choose_path)
        self.More_down.config(command=self.download_music)
        self.Info.config(command=self.show_mesage)
        self.Temp_button.config(command=self.single_music_down)
        self.Play_button.config(command=self.play_music)
        self.Pause_button.config(command=self.pause_button_click)
        self.Stop_button.config(command=self.stop_button_click)
        self.temp2.set(1) #默认配置为下载模式

    def choose_path(self):
        self.path_=askdirectory()
        self.temp3.set(self.path_)

    def show_mesage(self):
        msg="输入框可识别歌单list,或者歌曲名称 '\n'" \
            "输入歌单,请搜索后选择单独下载或者全部批量下载 '\n'" \
            "播放单曲需要先选择路径,选择歌曲"
        messagebox.showinfo(message=msg,title="使用说明")

    def get_web_lis(self):
        if self.temp.get()!="":#输入框非空
            flag = music_get.do_something(self.temp.get())
            music_dic=music_get.get_music_id(self.temp.get())
            if flag==True:#输入的是链接
                mp3_url=music_get.get_mps_url(self.temp.get())
                for i, j in mp3_url.items():#i是id号
                    self.T_message.insert(END,"歌曲："+i+"\n")
            else:#如果输入的是单曲
                self.T_message.insert(END, "正在查找歌曲：" + self.temp.get() + "\n")
                for id,name in music_dic.items():
                    self.T_message.insert(END, "找到歌曲:{}-{}".format(id,name)+ "\n")
        else:
            self.T_message.insert(END, "清输入歌曲名或者歌单链接："  + "\n")
            messagebox.showerror(title="警告",message="请输入歌名或者歌曲清单链接")

    def get_loacl_lis(self):
        for file in os.listdir(self.temp3.get()):
            self.T_message.insert(END, file + "\n")

    def get_lis(self):#搜索按钮，先判断下输入的是url 还是单曲
        print("开关",self.temp2.get())
        if self.temp2.get():#wen搜索
            print("web搜索")
            self.get_web_lis()
        else: #本地搜所
            print("本地搜索")
            self.get_loacl_lis()

    def download_music(self):#歌单批量下载
        try:
            mp3_url = music_get.get_mps_url(self.temp.get())#mp3 清单表 字典
            print(mp3_url)
            music_get.down_mp3(self.temp3.get(),self.temp.get())
            flag = music_get.do_something(self.temp.get())
            print(self.temp.get(),self.temp3.get())
            if os.path.exists(self.temp3.get()) and flag==True and len(mp3_url)>0:#路径存在,输入连接,dic飞空
                self.L_mp3_message.config(text="批量下载中,请不要再操作软件")
                for i in mp3_url.keys():
                    t=random.randint(100,300)*0.01
                    self.T_message.insert(END, "正在努力下载歌曲：" + i + "\n")
                    time.sleep(t)
            else:
                self.T_message.insert(END, "请输入歌单连接和存储路径" + "\n")
        except Exception as s:
            print(s.args)
            self.T_message.insert(END, "请先输入歌单连接和存储路径" + "\n")
            messagebox.showerror(title="警告",message="请输入歌名或者歌曲清单链接")


    def get_id(self):#获取id号
        if self.T_message.curselection():#不为空
            s=self.T_message.curselection()
            res=self.T_message.get(s[0])
            pa_id='找到歌曲:[\d]+-.+'
            if re.match(pa_id,res):#选择listbox
                id=res[res.find(":")+1:res.find("-")]
                return id
            else:
                self.T_message.insert(END, "请选择带id号的歌曲" + "\n")
        else:
            self.T_message.insert(END, "请先搜索歌名" + "\n")

    def single_music_down(self):#单曲下载
        print("----------下载单曲----------")
        id=self.get_id()
        flag=music_get.do_something(self.temp.get())#判断是url 还是歌曲名字 如果是url true 否则f
        if os.path.exists(self.temp3.get()) and flag==False:
            try:
                music_get.down_music2(self.temp3.get(),id,self.temp.get())
                self.T_message.insert(END, "正在下载歌曲:" +self.temp.get()+ str(id) + "\n")
                self.L_mp3_message.config(text="歌曲{}_{}下载完成".format(self.temp.get(),id))
            except Exception:
                self.T_message.insert(END, "请选择带的ID号的歌曲:" + "\n")
                messagebox.showwarning(title="友情提示", message="请选择带的ID号的歌曲")
        else:
            self.T_message.insert(END, "erro,请选择存储路径:" + "\n")
            messagebox.showwarning(title="温馨提示",message="请先搜索歌曲再选择存储路径")


    def play_music(self):
        print("播放音乐")
        path=self.temp3.get()#路径
        if os.path.exists(path) and self.temp2.get()==False:#如果路径存在,开关在播放模式
            if self.T_message.curselection():#lisbox飞空
                print("--------开始播放--------")
                music_file=self.T_message.get(self.T_message.curselection())
                current_music_path=self.temp3.get()+"/"+music_file
                pa_music=".+[\.]mp3"
                if re.match(pa_music,music_file):#匹配mp3文件
                    print("文件识别OK")
                    print(current_music_path)
                    self.L_mp3_message.config(text="文件识别OK")
                    self.play_music_mp3(current_music_path.strip()) #此处有坑,需要清除字符串换行符
                    self.music_temp.set("暂停")
                else:
                    print("非mp3文件")
                    self.L_mp3_message.config(text="非mp3文件")
            else:
                self.T_message.insert(END, "erro,请选择歌名:" + "\n")
        else:
            messagebox.showwarning(title="温馨提示",message="请选择歌曲路径,选择播放模式")

    def play_music_mp3(self,name):#播放音乐
        pygame.init()
        pygame.mixer.music.load(name)
        pygame.mixer.music.play()
        time.sleep(12)
        # pygame.mixer.music.stop()

    def pause_button_click(self):
        if self.music_temp.get()=="暂停":
            pygame.mixer.music.pause()
            self.music_temp.set("继续")
        elif self.music_temp.get()=="继续":
            pygame.mixer.music.unpause()
            self.music_temp.set("暂停")

    def pause_music(self):
        print("暂停播放")
        pygame.mixer.music.pause()

    def stop_button_click(self):
        pygame.mixer.music.stop()


a=App()
