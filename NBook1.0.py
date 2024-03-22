import tkinter as tk
from tkinter import ttk
from PIL import Image,ImageTk
import json
from tkinter import font as tkFont
import ctypes
#import threading
import multiprocessing
ctypes.windll.shcore.SetProcessDpiAwareness(1)
ScaleFactor=ctypes.windll.shcore.GetScaleFactorForDevice(0)

class Gifbutton(ttk.Button):
    def __init__(self,master,index):
        super().__init__(master)
        self.name="Vocbook"
        self.index=index
        self.frameindex=0
        self.gifstate=0
        self.openorclose=-1#notbookgif/
        self.images=[ImageTk.PhotoImage(Image.open(f'assets/bookgif/openbook ({i}).png').resize((130,130), Image.BICUBIC)) for i in range(19)]
        self.speed=35
        self.config(image=self.images[self.frameindex])
        self.bind("<Enter>", self.triggerplay) 
        self.bind("<Leave>", self.triggerplay)

    def triggerplay(self,event):
        self.openorclose*=-1
        def play():
            end=0
            if self.openorclose==1:
                if self.frameindex==18:
                    self.frameindex=10
                else:
                    self.frameindex+=1
            else:
                if self.frameindex<=10:
                    if self.frameindex>=1:
                        self.frameindex-=1
                    else:
                        end=1
                else:
                    if self.frameindex==18:
                        self.frameindex=10
                    else:
                        self.frameindex+=1
            self.config(image=self.images[self.frameindex])
            if end!=1:
                self.master.after(self.speed,play)       
        play()
    
    def enternotbook(self,event):
        print("enternotbook!")

class Giflabel(ttk.Label):
    def __init__(self,master,type,command):
        super().__init__(master)
        self.frameindex=0
        self.type=type
        self.openorclose=1
        self.speed=20
        self.pathlist=['assets/hints/config.png','assets/hints/left.png','assets/hints/right.png','assets/hints/delete.png']   
        self.images=[ImageTk.PhotoImage(Image.open(self.pathlist[type]).resize((50+i*2,50+i*2), Image.BICUBIC)) for i in range(5)]
        self.bind("<Button-1>",command)
        self.config(image=self.images[self.frameindex])
        self.bind("<Enter>", self.movein) 
        self.bind("<Leave>", self.moveout)
        self.config(padding=10)
    def movein(self,event):
        self.openorclose=1
        self.triggerplay()
    def moveout(self,event):
        self.openorclose=-1
        self.triggerplay()
    def triggerplay(self):
        def play():
            end=0
            if self.openorclose==1:
                if self.frameindex<4:
                    self.frameindex+=1
            else:
                if self.frameindex==0:
                    end=1
                else:
                    self.frameindex-=1
            self.config(image=self.images[self.frameindex],padding=10-self.frameindex)
            
            if end!=1:
                self.master.after(self.speed,play)       
        play()

class Giftext(ttk.Label):
    def __init__(self,master,text,command):
        super().__init__(master)
        self.config(text=text)
        self.font1 = tkFont.Font(family="楷体", size=12)
        self.font2 = tkFont.Font(family="楷体", size=14,weight='bold')
        self.bind("<Button-1>",command)
        self.config(font=self.font1)
        self.bind("<Enter>", self.movein) 
        self.bind("<Leave>", self.moveout)
        self.touched=0
        self.config(padding=2)
    def movein(self,event):
        self.config(font=self.font2)
        self.touched=1
        self.config(padding=1)
    def moveout(self,event):
        self.config(font=self.font1)
        self.touched=0
        self.config(padding=2)

class Word:
    def __init__(self,index,name='',len=0):
        self.name=name
        self.proficiency=0
        self.index=index
        self.collocation=[]
        self.meaning=[]
        self.egsentence=[]
        self.length=len
        self.hadchanged=0
    def compile(self,targetlist,update):
        targetlist
        type=targetlist[0]
        if type==1:#compile collocation
            if targetlist[1]>len(self.collocation)-1:
                self.collocation.append(update)
                self.meaning.append([])
                self.egsentence.append([])
            else:
                self.collocation[targetlist[1]]=update
        elif type==2:#compile meaning
            if targetlist[2]>len(self.meaning[targetlist[1]])-1:
                self.meaning[targetlist[1]].append(update)
                self.egsentence[targetlist[1]].append([])
            else:
                self.meaning[targetlist[1]][targetlist[2]]=update
        else:#compile egsentence
            if targetlist[3]>len(self.egsentence[targetlist[1]][targetlist[2]])-1:
                self.egsentence[targetlist[1]][targetlist[2]].append(update)
            else:
                self.egsentence[targetlist[1]][targetlist[2]][targetlist[3]]=update

        self.hadchanged=1
        print(self.collocation,self.meaning,self.egsentence)

    def remove(self,targetlist):
        type=targetlist[0]
        if type==1:
            if self.collocation!=[]:
                del self.collocation[targetlist[1]]
                del self.meaning[targetlist[1]]
                del self.egsentence[targetlist[1]]
        elif type==2:
            if self.meaning!=[[]]:
                del self.meaning[targetlist[1]][targetlist[2]]
                del self.egsentence[targetlist[1]][targetlist[2]]
        elif type==3:
            if self.egsentence!=[[[]]]:
                del self.egsentence[targetlist[1]][targetlist[2]][targetlist[3]]

class Vocbook:
    def __init__(self,name,index,pagedatalist,currentpage,lastwordindex):
        self.name=name
        self.index=index
        self.currentpage=currentpage
        self.pagedatalist=pagedatalist
        self.stagedpageinex=[]
        self.stagedword=[]
        self.lastwordindex=lastwordindex
        self.pageline=22

    def PAdjust(self,ind=0):
        pageline=self.pageline
        sum=0
        pageindex=0
        newlist=[[]]
        for pages in self.pagedatalist[ind:]:
            for words in pages:
                tepstart=0
                if sum+words[3]>=self.pageline:
                    if sum+words[3]==self.pageline:
                        newlist[pageindex].append([words[0],0,words[3],words[3]])
                        newlist.append([])
                        pageindex+=1
                        sum=0
                    else:
                        newlist[pageindex].append([words[0],0,pageline-sum,words[3]])
                        newlist.append([])
                        pageindex+=1
                        tepstart=pageline-sum
                        while words[3]-tepstart>=pageline:
                            newlist[pageindex].append([words[0],tepstart,tepstart+pageline,words[3]])
                            tepstart+=self.pageline
                            newlist.append([])
                            pageindex+=1
                        sum=words[3]-tepstart
                        if sum!=0:
                            newlist[pageindex].append([words[0],tepstart,words[3],words[3]])
                else:
                    sum+=words[3]
                    newlist[pageindex].append([words[0],0,words[3]-1,words[3]])
        self.pagedatalist=self.pagedatalist[:ind]+newlist

class Manager:
    def __init__(self,master):
        self.master=master
        self.menudata=None
        self.booknumber=None
        self.booknamelist=[]
        self.btnlist=[]#determine which vocbook to enter
        self.window=ttk.Frame(self.master)
        self.window.pack(fill="both", expand=True)
        self.CNB=None#class vocbook
        self.CNBindex=0#index of the vocbook you choose use this to read vocbook data accordingly
        self.CNBdata=None#whole list of class word
        self.CNBword=[]#only class word data of current page
        self.CNBline=0#how many lines for one page alter according to state
        self.CNBpage=0#current page of the vocbook
        self.SetupMenu()
        self.csize=12
        self.cfont = tkFont.Font(family="楷体", size=self.csize)
        self.efont = tkFont.Font(family="Ink Free", size=self.csize+1)
        self.e2font=tkFont.Font(family="Ink Free", size=13)
        self.cstyle = ttk.Style()
        self.cstyle.configure("TButton", font=self.cfont)
        self.newpagelist=[[]]#today's newword pages
        self.newpageindex=0#index to display today's new word
        self.newword=None#class word
        self.conpageline=18#config page's line number
        self.cxy=[0,0]#coordinate for config block
        self.state=0#0=reader 1=configer
        self.pagelinestr=[]#page line strings
        self.nwlabel=[[],[],[]]#newword's configure block entry and labels
        self.owlabel=None
        self.oldword=None
        self.deletelist=[]
        self.width=42
        self.width2=17
        self.endofline=3
        #s = ttk.Style()
        #s.configure('Treeview', rowheight=45)

    def SetupMenu(self):######################### MENU ##########################
        self.readmenu()
        self.window.col1 = ttk.Frame(self.window, padding=50)
        self.window.col1.grid(row=0, column=0)
        #self.window.lp=ttk.Frame(self.window)
        for i in range(self.booknumber):
            a=Gifbutton(self.window.col1,i)
            a.bind('<Button-1>',self.enternotbook)
            a.grid(row=i, column=1, padx=(45,40), pady=10, sticky="nsew")
            self.btnlist.append(a)
        note= ttk.Label(
            master=self.window.col1,
            text="Welcome to NBook\nIf you risk nothing\nyou risk even more",
            justify="center",
            font=tkFont.Font(family="Ink Free", size=13)
        )
        note.grid(row=4, column=1, pady=10, columnspan=2)
        # Separator
        sep = ttk.Separator(self.window.col1)
        sep.grid(row=3, column=1,padx=(45,40), pady=20, sticky="ew")

    def readmenu(self):
        with open('menu.json',mode='r',encoding='utf-8') as f:
            text=f.read()
        self.menudata=json.loads(text)
        self.booknumber=self.menudata[0]['booknumber']
        self.booknamelist=self.menudata[0]['bookname']

    def readnotebook(self):
        data=self.menudata[self.CNBindex+1]
        self.CNB=Vocbook(data['name'],self.CNBindex,data['pagedatalist'],data['currentpage'],data['lastwordindex'])
        with open(f'voc{self.CNBindex}.json',mode='r',encoding='utf-8') as f:
            text=f.read()
        self.CNBdata=json.loads(text)

    def enternotbook(self,event):######################### NOTEBOOK ##########################
        self.CNBindex=self.btnlist.index(event.widget)
        self.readnotebook()
        self.CNBpage=self.CNB.currentpage
        self.CNBline=self.CNB.pageline
        #mp=multiprocessing.Process(target=self.setuppage(), args=())
        #mp.start()
        #mp.join()
        self.window.col1.grid_remove()
        self.setuppage()
        self.window.menubox=ttk.Frame(self.window)
        self.window.menubox.grid(row=0,column=0)
        triggerconfig=Giflabel(self.window.menubox,0,self.triggerconfig)
        triggerconfig.grid(row=0,column=0,padx=20)
        leftbutton=Giflabel(self.window.menubox,1,self.left)
        leftbutton.grid(row=0,column=1,padx=20)
        rightbutton=Giflabel(self.window.menubox,2,self.right)
        rightbutton.grid(row=0,column=2,padx=20)
        
    def setuppage(self,event=None,word=None,wordpostion=None):#start setuppage 
        if self.state==0:
            self.window.lp = ttk.LabelFrame(self.window, text=f"Page:{self.CNBpage}", padding=(5,25))
            self.window.lp.grid(row=1, column=0,padx=(10, 10), pady=(10, 10))
            canvas = tk.Canvas(self.window.lp, width=900, height=1100, bg='#2b2b2b')
            canvas.grid(row=1,column=0)
            self.decodeintostr(self.CNB.pagedatalist,self.CNBpage,self.CNBline)
            self.configcanvas(self.pagelinestr,self.window.lp)
            #self.initcanvatexts(self.CNBline,canvas)
            #self.configlabels(self.pagelinestr)
            #self.displaylabels(self.CNBline)
        if self.state==1:
            self.window.menubox.grid_remove()
            self.window.lp.grid_remove()
            self.window.lp = ttk.LabelFrame(self.window, text="New Words", padding=(5,25))
            self.window.lp.grid(row=1, column=0,padx=(10, 10), pady=(10, 10))
            self.configblock()
            #self.initcanvatexts(self.conpageline,self.window.lp)
            self.decodeintostr(self.newpagelist,0,self.conpageline)
            self.configcanvas(self.pagelinestr,self.window.lp)
            #self.configlabels(self.pagelinestr)
            #self.displaylabels(self.conpageline)
        if self.state==2:
            self.window.menubox.grid_remove()
            self.configblock(word,wordpostion)
            
    def decodeintostr(self,pagedatalist,currentpage,pagelength):#list of strings
        current=pagedatalist[currentpage]
        pagelinestr=[]
        for word4list in current:
            print(len(self.CNBdata),word4list[0])
            word=self.CNBdata[word4list[0]]
            wordlinedata=[[0,0,1]]
            for collocation in range(len(word['collocation'])):
                for meaning in range(len(word['meaning'][collocation])):
                    wordlinedata[-1][0]=(word['meaning'][collocation][meaning])
                    for egsen in word['egsentence'][collocation][meaning]:
                        wordlinedata[-1][1]=egsen
                        wordlinedata.append([0,0,0])
            pagelinestr+=wordlinedata[word4list[1]:word4list[2]+1]
        while len(pagelinestr)<pagelength:
            pagelinestr.append([0,0,0])
        while len(pagelinestr)>pagelength:
            pagelinestr=pagelinestr[:-1]
        self.pagelinestr=pagelinestr
        print(self.pagelinestr)

    def configcanvas(self,pagelinestr,master):
        height=40+self.csize*4*len(pagelinestr)
        self.canvas = tk.Canvas(master, width=1100, height=height, bg='#353535')
        self.canvas.grid(row=1,column=0)
        for i in range(len(pagelinestr)):
            if pagelinestr[i]!=[0,0,0]:
                if pagelinestr[i][2]==1:
                    text_id = self.canvas.create_text(20,40+self.csize*4*i ,text='◉'+self.pagelinestr[i][0], anchor="w",fill="white",width=270,font=self.cfont)
                    text_id = self.canvas.create_text(280,40+self.csize*4*i ,text=self.pagelinestr[i][1], anchor="w",fill="white",width=900,font=self.efont)
                elif pagelinestr[i][0]!=0:
                    text_id = self.canvas.create_text(20,40+self.csize*4*i ,text='◯'+self.pagelinestr[i][0], anchor="w",fill="white",width=270,font=self.cfont)
                    text_id = self.canvas.create_text(280,40+self.csize*4*i ,text=self.pagelinestr[i][1], anchor="w",fill="white",width=900,font=self.efont)
                else:
                    text_id = self.canvas.create_text(280,40+self.csize*4*i ,text=self.pagelinestr[i][1], anchor="w",fill="white",width=900,font=self.efont)
            line_id = self.canvas.create_line(10,40+self.csize*4*i+2*self.csize,260, 40+self.csize*4*i+2*self.csize , fill="#585858")
            line_id = self.canvas.create_line(270,40+self.csize*4*i+2*self.csize,1170, 40+self.csize*4*i+2*self.csize , fill="#585858")

    def triggerconfig(self,event=None):#start configpage
        self.state=1
        self.setuppage(event)

    def triggerfix(self,event):#state3 fix exist word
        self.state=2
        for x in self.pagelabellist:
            if event.widget==x[0]:
                word=self.CNBword[self.pagelabellist.index[x]]
                wordposition=[self.CNBpage,self.pagelabellist.index[x]]
        self.setuppage(word=word,wordpostion=wordposition)

    def configblock(self,word:Word=None,wordposition=None):######################### CONFIGPAGE ##########################
        self.window.con = ttk.LabelFrame(self.window, text="AddWord", padding=0)
        self.window.con.grid(row=0, column=0 )
        alterpagebutton=ttk.Frame(self.window.con)
        alterpagebutton.grid(row=0,column=2)
        leftbutton=Giflabel(alterpagebutton,1,self.left)
        leftbutton.grid(row=0,column=1,padx=20)
        rightbutton=Giflabel(alterpagebutton,2,self.right)
        rightbutton.grid(row=0,column=2,padx=20)

        if self.state==1:
            self.newword=Word(self.CNB.lastwordindex)

            lab1=ttk.Label(self.window.con,text='N:')
            lab1.grid(row=0, column=0, padx=(3, 3), pady=(5, 5), sticky="nsew")
            en1=ttk.Entry(self.window.con,width=10)
            en1.grid(row=0,column=1,padx=(0, 4), pady=(5, 5), sticky="nsew")
            en1.bind("<KeyPress>", self.movefocus)
            en1.bind("<Button-1>",self.adjustcxy)
            self.nwlabel[0]=[en1,0,0,0]
            
            lab2=Giftext(self.window.con,text='x',command=self.remove)
            lab2.grid(row=1, column=0,padx=(3, 3), pady=(5, 5), sticky="nsew")
            self.deletelist.append(lab2)
            en2=ttk.Entry(self.window.con,width=15)
            en2.grid(row=1,column=1,padx=(0, 4), pady=(5, 5), sticky="nsew")
            en2.bind("<KeyPress>", self.movefocus)
            en2.bind("<Button-1>",self.adjustcxy)
            b=ttk.Label(self.window.con,width=self.width,text="|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||")
            b.grid(row=1,column=2,padx=(0, 4), pady=(5, 5), sticky="nsew")
            self.nwlabel[1]=[en2,b,[1,0,0,0],0]
            lab3=Giftext(self.window.con,text='x',command=self.remove)
            lab3.grid(row=2, column=0, padx=(3, 3), pady=(5, 5), sticky="nsew")
            self.deletelist.append(lab3)
            en3=ttk.Entry(self.window.con,width=10,font=self.cfont)
            en3.grid(row=2,column=1,padx=(0, 4), pady=(5, 5), sticky="nsew")
            en3.bind("<KeyPress>", self.movefocus)
            en3.bind("<Button-1>",self.adjustcxy)

            en4=ttk.Entry(self.window.con,width=self.width,font=self.efont)
            en4.grid(row=2,column=2,padx=(3, 4), pady=(5, 5), sticky="nsew")
            en4.bind("<KeyPress>", self.movefocus)
            en4.bind("<Button-1>",self.adjustcxy)
            self.nwlabel[2]=[en3,en4,[2,0,0,0],[3,0,0,0]]
            self.nwlabel[0][0].focus_set()

        elif self.state==2:
            pass
            #for i in range(len(word.meaning))

    def adjustcxy(self,event):
        for i in range(len(self.nwlabel)):
            for j in range(len(self.nwlabel[i])):
                if event.widget==self.nwlabel[i][j]:
                    self.cxy[0]=i
                    self.cxy[1]=j
        self.nwlabel[self.cxy[0]][self.cxy[1]].focus_set()
        print(self.cxy)

    def movefocus(self,event):
        def turnnewword():
            if self.oldword.name!="":
                length=0
                newwordstrline=[]
                for lines in self.owlabel:
                    if lines[3]!=0 :
                        if self.owlabel.index(lines)==2:
                            newwordstrline.append([lines[0].get(),lines[1].get(),1])
                        else:
                            if lines[0]==0:
                                newwordstrline.append(["",lines[1].get(),0])
                            else:
                                newwordstrline.append([lines[0].get(),lines[1].get(),0])
                        length+=1
                self.CNB.pagedatalist[-1].append([self.oldword.index,0,length-1,length])
                self.CNBdata.append({"name":self.oldword.name,"index":self.oldword.index,"collocation":self.oldword.collocation,"meaning":self.oldword.meaning,"egsentence":self.oldword.egsentence,"proficiency":0})
                self.newpagelist[-1]+=newwordstrline
                print(self.newpagelist)
            if m=='esc':
                self.escape()
            else:
                self.manageconfigpage()
                self.nwlabel[self.cxy[0]][self.cxy[1]].focus_set()

        m=None
        dlr=event.keysym
        if dlr=='Escape':
            m='esc'
            print("esc")
        if dlr=='s' and(event.state & 0x0004):
            m='nw'
            print("next word")
        if dlr=='Shift_L' or dlr=='Up':
            m="u"
        elif dlr=='Return' or dlr=='Down':
            m="d"
        elif dlr=='Left' and (event.state & 0x0004):
            m="l"
        elif dlr=='Right' and (event.state & 0x0004):
            m='r'
        
        if m!=None:
            d=event.widget.get()
            row=event.widget.grid_info()['row']
            if self.nwlabel[self.cxy[0]][1]==0:#type:name
                self.newword.name=d
                if m=='d':
                    self.cxy[0]+=1

            elif self.nwlabel[self.cxy[0]][3]==0:#type:collocation

                print("into collocation")
                self.newword.compile(self.nwlabel[self.cxy[0]][2],d)
                if m=='u':
                    self.cxy[0]-=1
                if m=='d':
                    if self.cxy[0]==len(self.nwlabel)-1:#if end of config page create  NEW MEANING ENTRY
                        a=ttk.Entry(self.window.con,width=10,font=self.cfont)
                        a.grid(row=row+1,column=1,padx=(0, 4), pady=(5, 5), sticky="nsew")
                        a.bind("<KeyPress>", self.movefocus)
                        a.bind("<Button-1>",self.adjustcxy)
                        b=ttk.Entry(self.window.con,width=self.width,font=self.efont)
                        b.grid(row=row+1,column=2,padx=(3, 4), pady=(5, 5), sticky="nsew")
                        b.bind("<KeyPress>", self.movefocus)
                        b.bind("<Button-1>",self.adjustcxy)
                        lab=Giftext(self.window.con,text='x',command=self.remove)
                        lab.grid(row=row+1, column=0,padx=(3, 3), pady=(5, 5), sticky="nsew")
                        self.deletelist.append(lab)
                        self.nwlabel.append([a,b,[2,self.nwlabel[self.cxy[0]][2][1],0,0],[3,self.nwlabel[self.cxy[0]][2][1],0,0]])
                    self.cxy[0]+=1

            elif self.nwlabel[self.cxy[0]][0]==0:#pureegsentense line
                self.newword.compile(self.nwlabel[self.cxy[0]][3],d)
                if m=='u':
                    if self.nwlabel[self.cxy[0]-1][3]!=0:
                        self.cxy[0]-=1
                elif m=='r':
                    if self.cxy[0]==len(self.nwlabel)-1 or self.nwlabel[self.cxy[0]+1][0]==0:
                        b=ttk.Entry(self.window.con,width=self.width,font=self.efont)
                        b.bind("<KeyPress>", self.movefocus)
                        b.bind("<Button-1>",self.adjustcxy)
                        b.grid(row=row+1,column=2,padx=(3, 4), pady=(5, 5), sticky="nsew")
                        lab=Giftext(self.window.con,text='x',command=self.remove)
                        lab.grid(row=row+1, column=0,padx=(3, 3), pady=(5, 5), sticky="nsew")
                        self.deletelist.append(lab)
                        self.nwlabel.insert(self.cxy[0]+1,[0,b,0,[3,self.nwlabel[self.cxy[0]][3][1]+1,self.nwlabel[self.cxy[0]][3][2],self.nwlabel[self.cxy[0]][3][3]+1]])
                        self.cxy[0]+=1

                elif m=='d':
                    if self.cxy[0]==len(self.nwlabel)-1:
                        a=ttk.Entry(self.window.con,width=15)
                        a.grid(row=row+1,column=1,padx=(0, 4), pady=(5, 5), sticky="nsew")
                        a.bind("<KeyPress>", self.movefocus)
                        a.bind("<Button-1>",self.adjustcxy)
                        b=ttk.Label(self.window.con,width=self.width,text="|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||")
                        b.grid(row=row+1,column=2,padx=(0, 4), pady=(5, 5), sticky="nsew")
                        self.nwlabel.append([a,b,[1,self.nwlabel[self.cxy[0]][3][1],0,0],0])
                        lab=Giftext(self.window.con,text='x',command=self.remove)
                        lab.grid(row=row+1, column=0,padx=(3, 3), pady=(5, 5), sticky="nsew")
                        self.deletelist.append(lab)
                        self.cxy[0]+=1
                    else:
                        if self.nwlabel[self.cxy[0]+1][1]!=0:
                            self.cxy[0]+=1

            else:#meaning entry line
                if self.cxy[1]==0: #meaning column
                    self.newword.compile(self.nwlabel[self.cxy[0]][2],d)
                    if m=='u':
                        self.cxy[0]-=1
                    if m=='l':
                        a=self.cxy[0]
                        print(a,len(self.nwlabel))
                        while a!=len(self.nwlabel) and self.nwlabel[a][3]!=0 :
                            a+=1
                        if self.nwlabel[a-1][3][2]==self.nwlabel[self.cxy[0]][2][2]:#wheter meaning is end of the collocation
                            a1=ttk.Entry(self.window.con,width=10,font=self.cfont)
                            a1.grid(row=row+1,column=1,padx=(0, 4), pady=(5, 5), sticky="nsew")
                            a1.bind("<KeyPress>", self.movefocus)
                            a1.bind("<Button-1>",self.adjustcxy)
                            b=ttk.Entry(self.window.con,width=self.width,font=self.efont)
                            b.grid(row=row+1,column=2,padx=(3, 4), pady=(5, 5), sticky="nsew")
                            b.bind("<KeyPress>", self.movefocus)
                            b.bind("<Button-1>",self.adjustcxy)
                            lab=Giftext(self.window.con,text='x',command=self.remove)
                            lab.grid(row=row+1, column=0,padx=(3, 3), pady=(5, 5), sticky="nsew")
                            self.deletelist.append(lab)
                            self.nwlabel.insert(a,[a1,b,[2,self.nwlabel[self.cxy[0]][3][1],self.nwlabel[self.cxy[0]][3][2]+1,0],[3,self.nwlabel[self.cxy[0]][3][1],self.nwlabel[self.cxy[0]][3][2]+1,0]])
                            self.cxy[0]+=1
                    if m=='d':
                        if self.cxy[0]<len(self.nwlabel)-1:
                            self.cxy[0]+=1
                    if m=='r':
                        self.cxy[1]=1
                else:#egsentence column
                    self.newword.compile(self.nwlabel[self.cxy[0]][3],d)
                    if m=='u':
                        if self.nwlabel[self.cxy[0]-1][3]!=0:
                            self.cxy[0]-=1
                    elif m=='l':
                        self.cxy[1]=0
                    elif m=='r':
                        b=ttk.Entry(self.window.con,width=self.width,font=self.efont)
                        b.grid(row=row+1,column=2,padx=(3, 4), pady=(5, 5), sticky="nsew")
                        b.bind("<KeyPress>", self.movefocus)
                        lab=Giftext(self.window.con,text='x',command=self.remove)
                        lab.grid(row=row+1, column=0,padx=(3, 3), pady=(5, 5), sticky="nsew")
                        self.deletelist.append(lab)
                        self.nwlabel.insert(self.cxy[0]+1,[0,b,0,[3,self.nwlabel[self.cxy[0]][3][1],self.nwlabel[self.cxy[0]][3][2],1]])
                        self.cxy[0]+=1
                    elif m=='d':
                        if self.cxy[0]==len(self.nwlabel)-1:
                            a=ttk.Entry(self.window.con,width=15)
                            a.grid(row=row+1,column=1,padx=(0, 4), pady=(5, 5), sticky="nsew")
                            b=ttk.Label(self.window.con,width=self.width,text="|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||")
                            b.grid(row=row+1,column=2,padx=(0, 4), pady=(5, 5), sticky="nsew")
                            a.bind("<KeyPress>", self.movefocus)
                            lab=Giftext(self.window.con,text='x',command=self.remove)
                            lab.grid(row=row+1, column=0,padx=(3, 3), pady=(5, 5), sticky="nsew")
                            self.deletelist.append(lab)
                            self.nwlabel.append([a,b,[1,self.nwlabel[self.cxy[0]][3][1]+1,0,0],0])
                            self.cxy[0]+=1
                            self.cxy[1]=0
                        else:
                            if self.nwlabel[self.cxy[0]+1][3]!=0:
                                self.cxy[0]+=1

            if m=='esc' or m=='nw':
                if self.newword.name!="" and self.nwlabel[2]!=[]:
                    self.CNB.lastwordindex+=1
                self.oldword=self.newword
                self.newword=None
                self.owlabel=self.nwlabel
                self.nwlabel=[[],[],[]]
                self.cxy=[0,0]
                self.window.con.grid_remove()
                if m=='nw':
                    self.configblock()
                    mp=multiprocessing.Process(target=turnnewword, args=())
                    mp.start()
                    #thread = threading.Thread(target=turnnewword, args=())
                    #thread.start()
                elif m=="esc":
                    turnnewword()

            print(self.cxy)
            if m!='esc' and m!='nw':
                self.nwlabel[self.cxy[0]][self.cxy[1]].focus_set()

    def remove(self,event):
        for x in self.deletelist:
            #print(x)
            if x.touched==1:
                order=self.deletelist.index(x)+1
                x.touched=0
                break
        self.newword.remove(self.nwlabel[order][2])
        if self.nwlabel[order][3]!=0:
            self.newword.remove(self.nwlabel[order][3])
        print(self.nwlabel,order,self.cxy)
        if self.nwlabel[order][3]==0:#collocation
            c=self.nwlabel[order][2][1]
            while order<=len(self.nwlabel)-1:
                x=self.nwlabel[order]
                if x[3]==0 and x[2]!=0 and x[2][1]==c:
                    self.delete(x)
                    self.deletex(self.deletelist[order-1])
                    print("deledcollocation")
                elif x[3]!=0 and x[3][1]==c:
                    self.delete(x)
                    self.deletex(self.deletelist[order-1])
                    print("deletemeanig")
                else:
                    print("leave")
                    break 

            print(self.nwlabel)
            if order>=len(self.deletelist)-1:
                for x in self.nwlabel[order:]:
                    if x[2]!=0:
                        if x[2][1]>c:
                            x[2][1]-=1
                    if x[3]!=0:
                        if x[3][1]>c:
                            x[3][1]-=1   
            print(self.nwlabel)
        elif self.nwlabel[order][0]==0:#egsentence line
            c=self.nwlabel[order][3][1]
            m=self.nwlabel[order][3][2]
            e=self.nwlabel[order][3][3]
            del self.nwlabel[order]
            if order>=len(self.deletelist)-1:
                for x in self.nwlabel[order:]:
                    if x[0]==0 and x[3][1]==c:
                        x[3][3]-=1

        else:#meaning line
            c=self.nwlabel[order][3][1]
            m=self.nwlabel[order][3][2]
            for x in self.nwlabel[order:]:
                if x[3][2]==m:
                    del x
                else:
                    break
            if order>=len(self.deletelist)-1:
                for x in self.nwlabel[order:]:
                    if x[2]!=0:
                        if x[2][1]==c:
                            x[3][2]-=1
                            x[2][2]-=1
                    elif x[3]!=0:
                        if x[2][1]==c:
                            x[3][2]-=1
        self.cxy=[order,0]
        self.nwlabel[self.cxy[0]][self.cxy[1]].focus_set()
        if len(self.nwlabel)==1:
            self.nwlabel.append([])
            self.nwlabel.append([])
            lab2=Giftext(self.window.con,text='x',command=self.remove)
            lab2.grid(row=1, column=0,padx=(3, 3), pady=(5, 5), sticky="nsew")
            self.deletelist.append(lab2)
            lab3=Giftext(self.window.con,text='x',command=self.remove)
            lab3.grid(row=2, column=0,padx=(3, 3), pady=(5, 5), sticky="nsew")
            self.deletelist.append(lab3)
            en2=ttk.Entry(self.window.con,width=15)
            en2.grid(row=1,column=1,padx=(0, 4), pady=(5, 5), sticky="nsew")
            en2.bind("<KeyPress>", self.movefocus)
            en2.bind("<Button-1>",self.adjustcxy)
            b=ttk.Label(self.window.con,width=self.width,text="|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||")
            b.grid(row=1,column=2,padx=(0, 4), pady=(5, 5), sticky="nsew")
            self.nwlefthintlist.append(b)
            self.nwlabel[1]=[en2,b,[1,0,0,0],0]
            en3=ttk.Entry(self.window.con,width=10,font=self.cfont)
            en3.grid(row=2,column=1,padx=(0, 4), pady=(5, 5), sticky="nsew")
            en3.bind("<KeyPress>", self.movefocus)
            en3.bind("<Button-1>",self.adjustcxy)
            en4=ttk.Entry(self.window.con,width=self.width,font=self.efont)
            en4.grid(row=2,column=2,padx=(3, 4), pady=(5, 5), sticky="nsew")
            en4.bind("<KeyPress>", self.movefocus)
            en4.bind("<Button-1>",self.adjustcxy)
            self.nwlabel[2]=[en3,en4,[2,0,0,0],[3,0,0,0]]
            self.nwlabel[1][0].focus_set()

    def delete(self,x):
        if x[0]!=0:
            x[0].grid_remove()
        if x[1]!=0:
            x[1].grid_remove()
        self.nwlabel.remove(x)

    def deletex(self,x):
        print(x.grid_info()['row'])
        x.grid_remove()
        self.deletelist.remove(x)

    def left(self,event=None):
        if self.state==1:
            if self.newpageindex!=0:
                self.newpageindex-=1
                self.configlabels(self.newpagelist[self.newpageindex])
                #self.displaylabels(self.conpageline)
                self.window.lp.config(text=f"Page{self.newpageindex}")
        else:
            
            if self.CNBpage!=0:
                self.canvas.destroy()
                self.CNBpage-=1
                self.decodeintostr(self.CNB.pagedatalist,self.CNBpage,self.CNBline)
                self.configcanvas(self.pagelinestr,self.window.lp)
                self.window.lp.config(text=f"Page{self.CNBpage}")

    def right(self,event=None):
        if self.state==1:
            if self.newpageindex!=len(self.newpagelist)-1:
                self.newpageindex+=1
                self.configlabels(self.newpagelist[self.newpageindex])
                #self.displaylabels(self.conpageline)
                self.window.lp.config(text=f"Page{self.newpageindex}")
        else:
            if self.CNBpage!=len(self.CNB.pagedatalist)-1:
                self.canvas.destroy()
                self.CNBpage+=1
                self.decodeintostr(self.CNB.pagedatalist,self.CNBpage,self.CNBline)
                self.configcanvas(self.pagelinestr,self.window.lp)
                self.window.lp.config(text=f"Page{self.CNBpage}")

    def manageconfigpage(self):
        self.newpagelist[-1]=[x for x in self.newpagelist[-1]  if x!=[0,0,0] ]
        while len(self.newpagelist[-1])>self.conpageline:
            self.newpagelist.append([self.newpagelist[-1][self.conpageline:]])
            self.newpagelist[-2]=self.newpagelist[-2][:self.conpageline]
            self.newpageindex+=1
        while len(self.newpagelist[-1])<self.conpageline:
            self.newpagelist[-1].append([0,0,0])
        print(self.newpagelist[self.newpageindex],"from manageconfigpage turning to newword")
        #self.decodeintostr(self.CNB.pagedatalist,self.CNBpage,self.CNBline)
        self.configlabels(self.newpagelist[self.newpageindex])
        self.displaylabels(self.conpageline)

    def escape(self):
        print("into escape")
        self.state=0
        self.newpagelist=[[]]
        self.window.con.grid_remove()
        self.window.lp.grid_remove()
        self.window.menubox=ttk.Frame(self.window)
        self.window.menubox.grid(row=0,column=0)
        triggerconfig=Giflabel(self.window.menubox,0,self.triggerconfig)
        triggerconfig.grid(row=0,column=0,padx=20)
        leftbutton=Giflabel(self.window.menubox,1,self.left)
        leftbutton.grid(row=0,column=1,padx=20)
        rightbutton=Giflabel(self.window.menubox,2,self.right)
        rightbutton.grid(row=0,column=2,padx=20)
        self.CNB.PAdjust(self.CNBpage)
        self.setuppage()
        with open(f'voc{self.CNBindex}.json', 'w') as file:  
            json.dump(self.CNBdata, file, indent=4)
        self.menudata[self.CNBindex+1]['pagedatalist']=self.CNB.pagedatalist
        self.menudata[self.CNBindex+1]['currentpage']=self.CNBpage
        self.menudata[self.CNBindex+1]['lastwordindex']=self.CNB.lastwordindex
        with open(f'menu.json', 'w') as file:  
            json.dump(self.menudata, file, indent=4) 

    def update(self):
        #self.DetectChangeScene()
        self.window.update()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("NBook!")
    
    # Simply set the theme
    root.tk.call("source", "azure.tcl")
    root.tk.call("set_theme", "dark")
    root.tk.call('tk', 'scaling', ScaleFactor/80)

    app = Manager(root)
    #app.pack(fill="both", expand=True)
    app.update()
    # Set a minsize for the window, and place it in the middle
    root.minsize(root.winfo_width(), root.winfo_height())
    x_cordinate = int((root.winfo_screenwidth() *23/40))# - (root.winfo_width() / 2)
    y_cordinate = int((root.winfo_screenheight() *1/40)) #- (root.winfo_height() / 2))
    root.geometry("+{}+{}".format(x_cordinate, y_cordinate-20))

    root.mainloop()

#old movefocus

"""
        if self.cxy[0] ==0:#current entry is NRow
            if m=='d':
                self.newword.name=d
                self.cxy[0]+=1
                #print(self.newword.name,self.cxy)

        elif self.cxy[0] in self.colinelist[1]:#current entry is CRow
            if m=='d':
                self.cxy[0]+=1
                if self.cxy[0]>self.endline:
                    self.endline=self.cxy[0]
                    self.colinelist[2].append(self.endline)
                    a=ttk.Entry(self.window.con,width=15)
                    a.grid(row=self.endline,column=1,padx=(1, 10), pady=(20, 10), sticky="nsew")
                    a.bind("<KeyPress>", self.movefocus)
                    b=ttk.Entry(self.window.con,width=50)
                    b.grid(row=self.endline,column=2,padx=(1, 10), pady=(20, 10), sticky="nsew")
                    b.bind("<KeyPress>", self.movefocus)
                    self.colist.append([a,b])
                    self.newword.compile(1,[len(self.colinelist[1]),d],0,0)
                else:
                    self.newword.compile(1,[self.colinelist[1].index(self.cxy[0]-1),d],0,0)
            elif m=='u':
                if self.cxy[0]==self.colinelist[1][0]:
                    self.cxy[0]=0
                else:
                    self.cxy[0]-=1
                self.newword.compile(1,[self.colinelist[1].index(self.cxy[0]+1),d],0,0)
            elif m=='l':
                if self.cxy[0]==1:
                    self.cxy[0]=0
                    self.newword.compile(1,[self.colinelist[1].index(self.cxy[0]+1),d],0,0)
                else:
                    self.newword.compile(1,[self.colinelist[1].index(self.cxy[0]),d],0,0)
                    self.cxy[0]=self.colinelist[1][self.colinelist[1].index(self.cxy[0])-1]
            elif m=='r':
                self.newword.compile(1,[self.colinelist[1].index(self.cxy[0]),d],0,0)
                if self.cxy[0]!=self.colinelist[1][-1]:
                    self.cxy[0]=self.colinelist[1][self.colinelist[1].index(self.cxy[0])+1]
                
        elif self.cxy[0] in self.colinelist[2]:#current entry is MRow
            
            if self.cxy[1]==0:# meaning entry
                #Meaning --> collo transfromation via line index
                if self.cxy[0]>self.colinelist[1][-1]:
                    self.newword.compile(2,len(self.colinelist[1])-1,[self.cxy[0]-self.colinelist[1][-1],d],0)
                else:
                    for i in range(len(self.colinelist[1])):
                        if self.colinelist[1][i]>self.cxy[0]:
                            self.newword.compile(2,i-1,[self.cxy[0]-self.colinelist[1][i-1],d],0)
                            break

                if m=='u':
                    for i in range(1,10):
                        if self.cxy[0]-i in self.colinelist[1]:
                            self.cxy[0]=self.cxy[0]-i
                            break
                        elif self.cxy[0]-i in self.colinelist[2]:
                            self.cxy[0]=self.cxy[0]-i
                            break
                elif m=='d':
                    if self.cxy[0]>=self.colinelist[1][-1] and self.cxy[0]>=self.colinelist[2][-1]:
                        pass
                    else:
                        for i in range(1,10):
                            if self.cxy[0]+i in self.colinelist[1]:
                                self.cxy[0]=self.cxy[0]+i
                                break
                            elif self.cxy[0]+i in self.colinelist[2]:
                                self.cxy[0]=self.cxy[0]+i
                                break 
                elif m=='r':
                    self.cxy[1]=1
                elif m=='l':
                    if self.cxy[0]>self.colinelist[1][-1] and self.cxy[0]>=self.colinelist[2][-1]:#end of c,m not sure whether bigger than s
                        self.endline+=1
                        b=ttk.Entry(self.window.con,width=50)
                        b.grid(row=self.endline,column=2,padx=(1, 10), pady=(20, 10), sticky="nsew")
                        b.bind("<KeyPress>", self.movefocus)
                        a=ttk.Entry(self.window.con,width=15)
                        a.grid(row=self.endline,column=1,padx=(1, 10), pady=(20, 10), sticky="nsew")#append new collocation
                        a.bind("<KeyPress>", self.movefocus)
                        self.colist.append([a,b])
                        self.colinelist[1].append(self.endline)
                        self.cxy[0]=self.endline
                    elif self.cxy[0]<self.colinelist[1][-1]:
                        for ncindex in self.colinelist[1]:
                            if ncindex>self.cxy[0]:
                                end=1
                                for y in self.colinelist[2]:
                                    if y>self.cxy[0] and y<self.colinelist[2]:
                                        end=0
                                        break
                                if end==1:
                                    #listmove
                                    for x in self.colinelist[1]:
                                        if x>self.cxy[0]:
                                            x+=1
                                    for x in self.colinelist[2]:
                                        if x>self.cxy[0]:
                                            x+=1
                                    for x in self.colinelist[3]:
                                        if x>ncindex:
                                            x+=1
                                    for i in range(ncindex,self.endline+1):
                                        self.colist[i][0].grid(row=i+1,column=1,padx=(1, 10), pady=(20, 10), sticky="nsew")
                                        if self.colist[i][1]!=0:
                                            self.colist[i][1].grid(row=i+1,column=2,padx=(1, 10), pady=(20, 10), sticky="nsew")
                                    self.endline+=1
                                    #end listmove
                                    #add new meaning
                                    a=ttk.Entry(self.window.con,width=15)
                                    a.grid(row=ncindex,column=1,padx=(1, 10), pady=(20, 10), sticky="nsew")#append new collocation
                                    a.bind("<KeyPress>", self.movefocus)
                                    b=ttk.Entry(self.window.con,width=50)
                                    b.grid(row=ncindex,column=2,padx=(1, 10), pady=(20, 10), sticky="nsew")
                                    b.bind("<KeyPress>", self.movefocus)
                                    self.colist.insert(ncindex,[a,b])
                                    self.colinelist[2].insert(self.colinelist[2].index(self.cxy[0])+1,ncindex)
                                    self.cxy[0]=ncindex

                            break
            if self.cxy[1]==1:#egsentence entry
                self.newword.compile(3,0,0,[0,d])
                if m=='l':
                    self.cxy[1]=0
        print(self.cxy)
        self.colist[self.cxy[0]][self.cxy[1]].focus_set()
"""
#old display strings
"""
        i=-1
        for x in pagelinestr:
            i+=1
            if x[2]==1:
                self.pagelabellist[i][0].config(text="◉"+x[0])
                self.pagelabellist[i][1].config(text=x[1])
                #print("configured in")
            else:
                if x[0]!=0:
                    self.pagelabellist[i][0].config(text=x[0])
                    self.pagelabellist[i][1].config(text=x[1])
                else:
                    if x[1]!=0:
                        self.pagelabellist[i][1].config(text=x[1]) 
        #print("configured in")"""

#displaystr tryout
"""
        self.treeview = ttk.Treeview(
            self.window.lp,
            #selectmode="browse",
            columns=("Meanings","Egsentence"),
            height=20,
        )
        self.treeview.grid(row=0,column=0)
        self.treeview.column("#0",width=0)
        self.treeview.column("Meanings", anchor="w", width=200)
        self.treeview.column("Egsentence", anchor="w", width=770)
        #self.treeview.heading("#0",text="")
        self.treeview.heading("Meanings", text="Meanings")
        self.treeview.heading("Egsentence", text="Egsentence")
        # Define treeview data
        

        # Insert treeview data
        for item in self.pagelinestr:
            if item[0]==0:
                self.treeview.insert("", index="end", values=("",item[1]))
            else:
                self.treeview.insert("", index="end", values=(item[0],item[1]))
        items = self.treeview.get_children() 
        for item in items:
            for i in range(1):
                self.treeview.item(item[i],tags='oddrow')  # 对每一个单元格命名
                self.treeview.tag_configure('oddrow',font=self.cfont)"""

#ancinet configlabels

"""
    def configlabels(self,pagelinestr):#config label.text
        i=-1
        for x in pagelinestr:
            i+=1
            print(x,i,len(pagelinestr))
            if x[2]==1:
                self.pagelabellist[i][0].config(text="◉"+x[0])
                self.pagelabellist[i][1].config(text=x[1])
                #print("configured in")
            else:
                if x[0]!=0:
                    self.pagelabellist[i][0].config(text="◦"+x[0])
                    self.pagelabellist[i][1].config(text=x[1])
                else:
                    if x[1]!=0:
                        self.pagelabellist[i][1].config(text=x[1])
                    else:
                        self.pagelabellist[i][1].config(text="")
                        self.pagelabellist[i][0].config(text="")

    def displaylabels(self,pagelength):#grid labels
        for i in range(pagelength):
            self.pagelabellist[i][0].grid(row=i*2,column=0,padx=1,pady=1,columnspan=1)
            self.pagelabellist[i][1].grid(row=i*2,column=1,padx=1,pady=1,columnspan=1)
            self.pagelabellist[i][2].grid(row=i*2+1,column=0,padx=1,pady=0,sticky="nsew")
            self.pagelabellist[i][3].grid(row=i*2+1,column=1,padx=1,pady=0,sticky="nsew")
            
            
        def initlabels(self,pagelength,master):#list of ttklabel
        self.pagelabellist=[]
        for i in range(pagelength):
            a=ttk.Label(master,text="",width=self.width2,font=self.cfont,justify='center')
            b=ttk.Label(master,text="",font=self.efont,width=self.width) 
            c=ttk.Separator(master)
            d=ttk.Separator(master)
            self.pagelabellist.append([a,b,c,d]) 

    def initcanvatexts(self,pagelength,master):#list of ttklabel
        self.pagelabellist=[]
        for i in range(pagelength):
            ta = master.create_text(20,40+self.csize*4*i ,text='◉'+self.pagelinestr[i][0], anchor="w",fill="white",width=200,font=self.cfont)
            tb = master.create_text(280,40+self.csize*4*i ,text=self.pagelinestr[i][1], anchor="w",fill="white",width=600,font=self.efont)
            la = master.create_line(10,40+self.csize*4*i+2*self.csize,260, 40+self.csize*4*i+2*self.csize , fill="#585858")
            lb = master.create_line(270,40+self.csize*4*i+2*self.csize,890, 40+self.csize*4*i+2*self.csize , fill="#585858")
     
            self.pagelabellist.append([ta,tb]) 

"""

#ancient treeview approach
"""
import tkinter as tk  
from tkinter import ttk  
from tkinter import font as tkFont
import ctypes

#ctypes.windll.shcore.SetProcessDpiAwareness(1)
#ScaleFactor=ctypes.windll.shcore.GetScaleFactorForDevice(0)


from tkintertable import TableCanvas  

 
  
import tkinter as tk  
from tkinter import ttk  
import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(1)
ScaleFactor=ctypes.windll.shcore.GetScaleFactorForDevice(0)
# 创建主窗口  
root = tk.Tk()  
root.title("Ttk Listbox 示例")  
root.tk.call("source", "azure.tcl")
root.tk.call("set_theme", "dark")
root.tk.call('tk', 'scaling', ScaleFactor/80)  
# 创建一个Frame来放置Listbox  
frame = ttk.Frame(root, padding=1)  
frame.pack(fill=tk.BOTH, expand=True)  
a=ttk.Label(frame,width=10,text="-------------------")
a.grid(row=0,column=1)
for i in range(1,100):
    a=ttk.Separator(frame)
    a.grid(row=i,column=1,pady=5,padx=0)

  
# 运行Tkinter主循环  
root.mainloop()




# 创建 Tkinter 窗口  
root = tk.Tk()  
root.title("TkinterTable 示例")  
  
# 创建表格对象  
table = TableCanvas(root)  
  
# 定义表格数据和列标题  
data = [  
    ['姓名', '年龄', '城市'],  
    ['Alice', 25, 'New York'],  
    ['Bob', 32, 'Paris'],  
    ['Charlie', 18, 'London'],  
]  
  
# 将数据添加到表格中  
table.createTable(data, showtoolbar=False, showstatusbar=False)  
  
# 配置表格的样式（可选）  
table.configure(stretch='all', selectmode='browse')  
  
# 将表格添加到窗口中  
table.pack(fill='both', expand=True)  
  
#root.tk.call('tk', 'scaling', ScaleFactor/70)# 运行 Tkinter 主循环  
root.mainloop()

       self.treeview = ttk.Treeview(
            self.window.lp,
            #selectmode="browse",
            show="headings",
            columns=("meaning","egsentence"),
            height=10,
        )
        #self.treeview.grid(row=1,column=1)
        #self.treeview.pack(expand=True, fill="both") 
        # Treeview columns
        self.treeview.column("meaning", anchor="w", width=120)
        self.treeview.column("egsentence", anchor="w", width=200)
        self.treeview.heading("meaning", text="meaning")  
        self.treeview.heading("egsentence", text="egsentence") 
        # Define treeview data
        treeview_data = [
            ("", 1, "Parent", ("Item 1", "Value 1")),
            (1, 2, "Child", ("Subitem 1.1", "Value 1.1")),
            (1, 3, "Child", ("Subitem 1.2", "Value 1.2")),
            (1, 4, "Child", ("Subitem 1.3", "Value 1.3")),
            (1, 5, "Child", ("Subitem 1.4", "Value 1.4")),
            ("", 6, "Parent", ("Item 2", "Value 2")),
            (6, 7, "Child", ("Subitem 2.1", "Value 2.1")),
            (6, 8, "Sub-parent", ("Subitem 2.2", "Value 2.2")),
            (8, 9, "Child", ("Subitem 2.2.1", "Value 2.2.1")),
            (8, 10, "Child", ("Subitem 2.2.2", "Value 2.2.2")),
            (8, 11, "Child", ("Subitem 2.2.3", "Value 2.2.3")),
            (6, 12, "Child", ("Subitem 2.3", "Value 2.3")),
            (6, 13, "Child", ("Subitem 2.4", "Value 2.4")),
            ("", 14, "Parent", ("Item 3", "Value 3")),
            (14, 15, "Child", ("Subitem 3.1", "Value 3.1")),
            (14, 16, "Child", ("Subitem 3.2", "Value 3.2")),
            (14, 17, "Child", ("Subitem 3.3", "Value 3.3")),
            (14, 18, "Child", ("Subitem 3.4", "Value 3.4")),
            ("", 19, "Parent", ("Item 4", "Value 4")),
            (19, 20, "Child", ("Subitem 4.1", "Value 4.1")),
            (19, 21, "Sub-parent", ("Subitem 4.2", "Value 4.2")),
            (21, 22, "Child", ("Subitem 4.2.1", "Value 4.2.1")),
            (21, 23, "Child", ("Subitem 4.2.2", "Value 4.2.2")),
            (21, 24, "Child", ("Subitem 4.2.3", "Value 4.2.3")),
            (19, 25, "Child", ("Subitem 4.3", "Value 4.3")),
        ]

        # Insert treeview data
        #for item in treeview_data:
         #   self.treeview.insert("", "end", value=(item[1],item[2]))
        self.treeview.insert("", "end", values=("Value 1", "Value 2"))  
        self.treeview.insert("", "end", values=("Value 4", "Value 5")) 
        self.treeview.pack(expand=True, fill="both") 

"""        # Select and scroll
