#coding=utf-8  
'''
Created on 2015年12月21日

@author: Administrator
'''



from os.path import os
import sys
from tkinter import ttk, IntVar, Text, StringVar
import tkinter
from tkinter.constants import TOP, BOTH, VERTICAL, RIGHT, LEFT
from tkinter.filedialog import askdirectory
import traceback

from process import ProcessMgr
from util import Log, RootInfoMgr
from util.Constant import VERSION_TYPE_NORMAL, VERSION_TYPE_MILESTONE, \
    VERSION_TYPE_PLATFORM, PLATFORM_IOS, PLATFORM_ANDROID


class MainUI:
    
    __PLATFORM = ['IOS', 'ANDROID']
    __rootList = []
    
    def __init__(self):
        self.__rootList = []
        
    def initUI(self):
        self.frame = tkinter.Tk()
        self.frame.geometry('600x600')  # 是x 不是*
        self.frame.resizable(width=True, height=True)  # 宽不可变, 高可变,默认为True
        self.frame.minsize(700, 600)
        self.frame.title('工具集')
        
        '''工作目录'''
        panel1 = ttk.Labelframe(self.frame, text='工作目录')
        
        # 打包路径label
        packRootLabel = ttk.Label(panel1, text='打包路径:')
        packRootLabel.grid(row=0, column=0, padx=3, pady=3)
        
        # root下拉菜单
        self.packRootPathVar = StringVar()
        self.packRootPathVar.trace('w', self.__packRootPathChangeCallBack)
        self.packRootPath = ttk.Combobox(panel1, textvariable=self.packRootPathVar)
        self.packRootPath.grid(row=0, column=1, padx=3, pady=3, stick='we')
        
        # root路径选择按钮
        packRootSelBtn = ttk.Button(panel1, text='选择', command=self.selectRootDir)
        packRootSelBtn.grid(row=0, column=2, padx=3, pady=3)
        panel1.columnconfigure(1, weight=1)
        panel1.pack(fill='x', side=TOP, padx=5, pady=5, ipadx=10, ipady=5)
        
        '''打包设置'''
        panel2 = ttk.LabelFrame(self.frame, text='打包设置')
        childRow1 = ttk.Frame(panel2)
        
        # 资源目录label
        srcPathLabel = ttk.Label(childRow1, text='资源目录:')
        srcPathLabel.grid(row=0, column=0, padx=3, pady=3)
        
        # 资源目录路径
        self.srcPathVar = StringVar()
        self.srcPathVar.trace('w', callback=self.__platformChangeCallBack)
        srcPath = ttk.Entry(childRow1, textvariable=self.srcPathVar)
        srcPath.grid(row=0, column=1, padx=3, pady=3, stick='we')
        
        # 资源目录路径选择按钮
        srcPathBtn = ttk.Button(childRow1, text='选择', command=self.selectSrcDir)
        srcPathBtn.grid(row=0, column=2, padx=3, pady=3)
        childRow1.columnconfigure(1, weight=1)
        childRow1.pack(fill='x', side=TOP)
        childRow2 = ttk.Frame(panel2)
        
        # 平台类型
        self.platformComboVar = StringVar()
        platformCombo = ttk.Combobox(childRow2, values=self.__PLATFORM, state='readonly', width=10, textvariable=self.platformComboVar)
        platformCombo.current(0)
        platformCombo.grid(row=0, column=1, padx=3, pady=3)
        
        # 是否全新打包
        self.isNew = IntVar()
        isNewCheck = ttk.Checkbutton(childRow2, text='全新打包', variable=self.isNew)
        isNewCheck.grid(row=0, column=3, padx=3, pady=3)
        
        # 是否整包
        self.isFull = IntVar()
        isFullCheck = ttk.Checkbutton(childRow2, text='整包', variable=self.isFull)
        isFullCheck.grid(row=0, column=4, padx=3, pady=3)
        
        childRow2.columnconfigure(5, weight=1)
        childRow2.pack(fill='x', side=TOP)
        
        panel2.pack(fill='x', side=TOP, padx=5, pady=5, ipadx=10, ipady=5)
        
        # 开始按钮
        startBtn = ttk.Button(self.frame, text='开始打包', command=self.startPack)
        startBtn.pack()
        
        '''输出步骤'''
        panel3 = ttk.LabelFrame(self.frame, text='总览')
        headTextBar = ttk.Scrollbar(panel3, orient=VERTICAL)
        headTextBar.pack(side=RIGHT, fill='y')
        self.headConsole = Text(panel3, state='disabled', yscrollcommand=headTextBar.set, width=40, foreground='white', background='black')
        self.headConsole.pack(expand=1, fill=BOTH)
        panel3.pack(fill='y', side=LEFT, padx=5, pady=5, ipadx=10, ipady=5)
        
        '''输出详细信息'''
        panel4 = ttk.LabelFrame(self.frame, text='详细信息')
        bottomTextBar = ttk.Scrollbar(panel4, orient=VERTICAL)
        bottomTextBar.pack(side=RIGHT, fill='y')
        self.bottomConsole = Text(panel4, state='disabled', yscrollcommand=bottomTextBar.set, foreground='white', background='black')
        self.bottomConsole.pack(expand=1, fill=BOTH)
        panel4.pack(expand=1, fill=BOTH, side=LEFT, padx=5, pady=5, ipadx=10, ipady=5)
        
        self.frame.after(50, func=self.updateLog)
        
    def initUIValues(self):
        RootInfoMgr.load()
        self.__rootList = RootInfoMgr.rootPathList
        self.updateRootList()
        
    def show(self):
        self.frame.mainloop()
        
    def updateLog(self):
        self.headConsole.configure(state='normal')
        while not Log.infoQueue.empty() :
            text = Log.infoQueue.get(True, 1)
            self.headConsole.insert('end', text)
        self.headConsole.configure(state='disabled')
        
        self.bottomConsole.configure(state='normal')
        while not Log.detailQueue.empty() :
            text = Log.detailQueue.get(True, 1)
            self.bottomConsole.insert('end', text)
        self.bottomConsole.configure(state='disabled')
        
        self.frame.after(50, func=self.updateLog)
    
    def selectRootDir(self):
        rootdir = askdirectory()
        if len(rootdir) > 0 and os.path.exists(rootdir) :
            self.packRootPathVar.set(rootdir)
            
    def selectSrcDir(self):
        srcdir = askdirectory()
        if len(srcdir) > 0 and os.path.exists(srcdir) :
            self.srcPathVar.set(srcdir)
    
    def updateRootList(self):
        self.packRootPath['values'] = self.__rootList
        if len(self.__rootList) > 0:
            self.packRootPath.current(0)
            
    def startPack(self):
        self.headConsole.configure(state='normal')
        self.headConsole.delete(0.0, 'end')
        self.headConsole.configure(state='disabled')
        self.bottomConsole.configure(state='normal')
        self.bottomConsole.delete(0.0, 'end')
        self.bottomConsole.configure(state='disabled')
        if not os.path.exists(self.packRootPathVar.get()) :
            Log.printInfoln('打包目录错了，骚年，你确定有这文件夹？？ ' + self.packRootPathVar.get())
            return
        if not os.path.exists(self.srcPathVar.get()) :
            Log.printInfoln('资源文件目录错了!' + self.srcPathVar.get())
            return
        RootInfoMgr.updateRoot(self.packRootPathVar.get())
        RootInfoMgr.writeRootInfo(self.packRootPathVar.get(), os.path.normpath(self.srcPathVar.get()), self.platformComboVar.get())
        self.updateRootList()
        ProcessMgr.start(self.srcPathVar.get(), self.getPlatformType(), self.isNew.get() > 0, self.isFull.get() > 0)
        
    def getPlatformType(self):
        if self.__PLATFORM[0] == self.platformComboVar :
            return PLATFORM_IOS
        else :
            return PLATFORM_ANDROID
        
    def __packRootPathChangeCallBack(self, *args):
        if os.path.exists(self.packRootPathVar.get()) :
            rootInfo = RootInfoMgr.loadRootInfo(self.packRootPathVar.get())
            if rootInfo != None :
                self.srcPathVar.set(os.path.normpath(rootInfo.srcPath))
                self.platformComboVar.set(rootInfo.platform)
        
    def __platformChangeCallBack(self, *args):
        if os.path.exists(self.srcPathVar.get()) :
            try:
                self.headConsole.configure(state='normal')
                self.headConsole.delete(0.0, 'end')
                self.headConsole.configure(state='disabled')
                self.bottomConsole.configure(state='normal')
                self.bottomConsole.delete(0.0, 'end')
                self.bottomConsole.configure(state='disabled')
                ProcessMgr.createContext(self.packRootPathVar.get())
            except :
                t, v, tb = sys.exc_info()
                print(t, v)
                traceback.print_tb(tb)
