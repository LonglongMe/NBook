import tkinter as tk
from tkinter import ttk
from PIL import Image,ImageTk
import json
from tkinter import font as tkFont

class Gifbutton(ttk.Button):
    def __init__(self,master,index):
        super().__init__(master)
        self.name="Vocbook"
        self.index=index
        self.frameindex=0
        self.gifstate=0
        self.openorclose=-1#notbookgif/
        self.images=[ImageTk.PhotoImage(Image.open(f'assets/openbook ({i}).png').resize((75,75), Image.BICUBIC)) for i in range(19)]
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
        if type==1:
            if targetlist[1]>len(self.collocation)-1:
                self.collocation.append(update)
                self.meaning.append([])
                self.egsentence.append([[]])
            else:
                self.collocation[targetlist[1]]=update
        elif type==2:
            if targetlist[2]>len(self.meaning[targetlist[1]])-1:
                self.meaning[targetlist[1]].append(update)
                self.egsentence[targetlist[1]].append([])
            else:
                self.meaning[targetlist[1]][targetlist[2]]=update
        else:
            if targetlist[3]>len(self.egsentence[targetlist[1]][targetlist[2]])-1:
                self.egsentence[targetlist[1]][targetlist[2]].append(update)
            else:
                self.egsentence[targetlist[1]][targetlist[2]][targetlist[3]]=update

        self.hadchanged=1
        print(self.collocation,self.meaning,self.egsentence)

class Vocbook:
    def __init__(self,name,index,pagedatalist,currentpage,lastwordindex):
        self.name=name
        self.index=index
        self.currentpage=currentpage
        self.pagedatalist=pagedatalist
        self.stagedpageinex=[]
        self.stagedword=[]
        self.lastwordindex=lastwordindex
        self.pageline=20

    def PAdjust(self,ind=0):
        pageline=20
        sum=0
        pageindex=0
        newlist=[[]]
        for pages in self.pagedatalist[ind:]:
            for words in pages:
                tepstart=1
                if sum+words[3]>=self.pageline:
                    if sum+words[3]==self.pageline:
                        newlist[pageindex].append([words[0],tepstart,words[3],words[3]])
                        newlist.append([])
                        pageindex+=1
                        sum=0
                    else:
                        newlist[pageindex].append([words[0],1,pageline-sum,words[3]])
                        newlist.append([])
                        pageindex+=1
                        tepstart=pageline-sum+1
                        while words[3]-tepstart>=pageline:
                            newlist[pageindex].append([words[0],tepstart,tepstart+pageline,words[3]])
                            tepstart+=20
                            newlist.append([])
                            pageindex+=1
                        sum=words[3]-tepstart
                        if sum!=0:
                            newlist[pageindex].append([words[0],tepstart,words[3],words[3]])
                else:
                    sum+=words[3]
                    newlist[pageindex].append([words[0],0,words[3]-1,words[3]])
        self.pagedatalist=self.pagedatalist[:ind]+newlist


    def output(self):
        pass

class Manager:
    def __init__(self,master):
        self.master=master
        self.menudata=None
        self.booknumber=None
        self.booknamelist=[]
        self.window=ttk.Frame(self.master)
        self.window.pack(fill="both", expand=True)
        self.CNB=None
        self.CNBindex=None
        self.CNBdata=None
        self.CNBword=[]
        self.CNBline=0
        self.CNBpage=0
        self.SetupMenu()
        self.cfont = tkFont.Font(family="华文细黑", size=12)
        self.efont=tkFont.Font(family="Ink Free", size=13)
        self.cstyle = ttk.Style()
        self.cstyle.configure("TButton", font=self.cfont)
        self.endline=2
        self.newpagelist=[[]]
        self.newpageindex=0
        self.newword=None
        self.conpageline=15
        self.cxy=[0,0]
        self.state=0
        self.pagelinestr=[]
        self.pagelabellist=[]
        self.nwlabel=[[],[],[]]
        self.nwlefthintlist=[]

    def SetupMenu(self):
        self.readmenu()
        self.window.col1 = ttk.Frame(self.window, padding=50)
        self.window.col1.grid(row=0, column=0)
        self.window.btnlist=[]
        for i in range(self.booknumber):
            a=Gifbutton(self.window.col1,i)
            a.bind('<Button-1>',self.enternotbook)
            self.window.btnlist.append(a)
            a.grid(row=i, column=1, padx=10, pady=10, sticky="nsew")
        self.window.lab= ttk.Label(
            master=self.window.col1,
            text="Welcome to NBook\nExert your time",
            justify="center",
            font=tkFont.Font(family="Ink Free", size=13)
        )
        self.window.lab.grid(row=4, column=1, pady=10, columnspan=2)
        # Separator
        self.window.separator = ttk.Separator(self.window.col1)
        self.window.separator.grid(row=3, column=1, padx=10, pady=20, sticky="ew")

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

    def enternotbook(self,event):
        self.CNBindex=self.window.btnlist.index(event.widget)
        self.readnotebook()
        self.CNBpage=self.CNB.currentpage
        self.CNBline=self.CNB.pageline
        self.window.destroy()
        self.window=ttk.Frame(self.master)
        self.window.grid(row=0,column=0)
        self.window.pack(fill="both", expand=True)
        self.window.menubox=ttk.Frame(self.window)
        self.window.menubox.grid(row=0,column=0)
        triggerconfig=ttk.Button(self.window.menubox,text='Config',command=self.triggerconfig)
        triggerconfig.grid(row=0,column=0,padx=(5,15))
        leftbutton=ttk.Button(self.window.menubox,text='←',command=self.left)
        leftbutton.grid(row=0,column=1,padx=(15,5))
        rightbutton=ttk.Button(self.window.menubox,text='→',command=self.right)
        rightbutton.grid(row=0,column=2,padx=(5,15))
        self.setuppage()

    def setuppage(self,event=None):#start setuppage 
        if self.state==0:
            self.window.lp = ttk.LabelFrame(self.window, text=f"Page:{self.CNBpage}", padding=(5,25))
            self.window.lp.grid(row=1, column=0,padx=(10, 10), pady=(10, 10))
            self.decodeintostr(self.CNB.pagedatalist,self.CNBpage,self.CNBline)
            self.initlabels(self.CNBline,self.window.lp)
            self.displaystrs(self.pagelinestr)
        if self.state==1:
            self.window.lp = ttk.LabelFrame(self.window, text="New Words", padding=(5,25))
            self.window.lp.grid(row=1, column=0,padx=(10, 10), pady=(10, 10))
            self.initlabels(self.conpageline,self.window.lp)
            self.configblock()

    def initlabels(self,pagelength,master):
        self.pagelabellist=[]
        for i in range(pagelength):
            a=ttk.Label(master,text="",width=15,font=self.cfont,justify='center')
            a.grid(row=i*2,column=0,padx=1,pady=1,columnspan=1)
                #a.bind('<Button-1>',self.triggerconfig)
            b=ttk.Label(master,text="",font=self.efont,width=42)
            b.grid(row=i*2,column=1,padx=1,pady=1,columnspan=1,sticky="nsew")  
            c=ttk.Separator(master)
            c.grid(row=i*2+1,column=1,padx=1,pady=0,sticky="nsew")
            d=ttk.Separator(master)
            d.grid(row=i*2+1, column=0, padx=1, pady=0, sticky="ew")  
            self.pagelabellist.append([a,b]) 

    def decodeintostr(self,pagedatalist,currentpage,pagelength):
        current=pagedatalist[currentpage]
        pagelinestr=[]
        for word4list in current:
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
        self.pagelinestr=pagelinestr

    def displaystrs(self,pagelinestr):#done setuppage
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
        #print("configured in")

    def triggerconfig(self,event=None):#start configpage
        self.state=1
        self.window.lp.grid_remove()
        self.setuppage(event)

    def configblock(self):
        self.newword=Word(self.CNB.lastwordindex)
        self.window.con = ttk.LabelFrame(self.window, text="AddWord", padding=0)
        self.window.con.grid(row=0, column=0 )
        lab1=ttk.Label(self.window.con,text='N:')
        lab1.grid(row=0, column=0, padx=(3, 3), pady=(5, 5), sticky="nsew")
        self.nwlefthintlist.append(lab1)
        en1=ttk.Entry(self.window.con,width=10)
        en1.grid(row=0,column=1,padx=(0, 4), pady=(5, 5), sticky="nsew")
        en1.bind("<KeyPress>", self.movefocus)
        en1.bind("<Button-1>",self.adjustcxy)
        self.nwlabel[0]=[en1,0,0,0]

        lab2=ttk.Label(self.window.con,text='C:')
        lab2.grid(row=1, column=0,padx=(3, 3), pady=(5, 5), sticky="nsew")
        self.nwlefthintlist.append(lab2)
        en2=ttk.Entry(self.window.con,width=15)
        en2.grid(row=1,column=1,padx=(0, 4), pady=(5, 5), sticky="nsew")
        en2.bind("<KeyPress>", self.movefocus)
        en2.bind("<Button-1>",self.adjustcxy)
        b=ttk.Label(self.window.con,width=40,text="-------------------------------------------------------------------------------------------")
        b.grid(row=1,column=2,padx=(0, 4), pady=(5, 5), sticky="nsew")
        self.nwlefthintlist.append(b)
        self.nwlabel[1]=[en2,b,[1,0,0,0],0]
        lab3=ttk.Label(self.window.con,text='M:')
        lab3.grid(row=2, column=0, padx=(3, 3), pady=(5, 5), sticky="nsew")
        self.nwlefthintlist.append(lab3)
        en3=ttk.Entry(self.window.con,width=10,font=self.cfont)
        en3.grid(row=2,column=1,padx=(0, 4), pady=(5, 5), sticky="nsew")
        en3.bind("<KeyPress>", self.movefocus)
        en3.bind("<Button-1>",self.adjustcxy)

        en4=ttk.Entry(self.window.con,width=40,font=self.efont)
        en4.grid(row=2,column=2,padx=(3, 4), pady=(5, 5), sticky="nsew")
        en4.bind("<KeyPress>", self.movefocus)
        en4.bind("<Button-1>",self.adjustcxy)
        self.nwlabel[2]=[en3,en4,[2,0,0,0],[3,0,0,0]]

        alterpagebutton=ttk.Frame(self.window.con)
        alterpagebutton.grid(row=0,column=2)
        leftbutton=ttk.Button(alterpagebutton,text="←",width=2,command=self.left)
        leftbutton.grid(row=0,column=0,padx=10)
        rightbutton=ttk.Button(alterpagebutton,text="→",width=2,command=self.right)
        rightbutton.grid(row=0,column=1,padx=10)

    def adjustcxy(self,event):
        for i in range(len(self.nwlabel)):
            for j in range(len(self.nwlabel[i])):
                if event.widget==self.nwlabel[i][j]:
                    self.cxy[0]=i
                    self.cxy[1]=j
        print(self.cxy)

    def movefocus(self,event):
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

            if self.nwlabel[self.cxy[0]][2]==0 and self.nwlabel[self.cxy[0]][3]==0:#type:name
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
                        a=ttk.Entry(self.window.con,width=10)
                        a.grid(row=self.cxy[0]+1,column=1,padx=(0, 4), pady=(5, 5), sticky="nsew")
                        a.bind("<KeyPress>", self.movefocus)
                        a.bind("<Button-1>",self.adjustcxy)
                        b=ttk.Entry(self.window.con,width=40,font=self.efont)
                        b.grid(row=self.cxy[0]+1,column=2,padx=(3, 4), pady=(5, 5), sticky="nsew")
                        b.bind("<KeyPress>", self.movefocus)
                        b.bind("<Button-1>",self.adjustcxy)
                        self.nwlabel.append([a,b,[2,self.nwlabel[self.cxy[0]][2][1],0,0],[3,self.nwlabel[self.cxy[0]][2][1],0,0]])
                    self.cxy[0]+=1

            elif self.nwlabel[self.cxy[0]][0]==0:#pureegsentense line
                print("detect egsentence line")
                self.newword.compile(self.nwlabel[self.cxy[0]][3],d)
                if m=='u':
                    if self.nwlabel[self.cxy[0]-1][3]!=0:
                        self.cxy[0]-=1

                elif m=='r':
                    print("intoiiiiii-000000000000000000000")
                    if self.cxy[0]==len(self.nwlabel)-1 or self.nwlabel[self.cxy[0]+1][0]==0:
                        b=ttk.Entry(self.window.con,width=40,font=self.efont)
                        b.grid(row=self.cxy[0]+1,column=2,padx=(3, 4), pady=(5, 5), sticky="nsew")
                        b.bind("<KeyPress>", self.movefocus)
                        b.bind("<Button-1>",self.adjustcxy)
                        self.nwlabel.insert(self.cxy[0]+1,[0,b,0,[3,self.nwlabel[self.cxy[0]][3][1],self.nwlabel[self.cxy[0]][3][2],self.nwlabel[self.cxy[0]][3][3]+1]])
                        self.cxy[0]+=1

                elif m=='d':
                    if self.cxy[0]==len(self.nwlabel)-1:
                        a=ttk.Entry(self.window.con,width=15)
                        a.grid(row=self.cxy[0]+1,column=1,padx=(0, 4), pady=(5, 5), sticky="nsew")
                        a.bind("<KeyPress>", self.movefocus)
                        a.bind("<Button-1>",self.adjustcxy)
                        b=ttk.Label(self.window.con,width=40,text="-------------------------------------------------------------------------------------------")
                        b.grid(row=self.cxy[0]+1,column=2,padx=(0, 4), pady=(5, 5), sticky="nsew")
                        self.nwlabel.append([a,b,[1,self.nwlabel[self.cxy[0]][3][1],0,0],0])
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
                        while self.nwlabel[a][3]!=0:#////////////////////////////////////////////////////////
                            if a==len(self.nwlabel):
                                break
                            a+=1
                        if self.nwlabel[a-1][3][2]==self.nwlabel[self.cxy[0]][2][2]:#wheter meaning is end of the collocation
                            a1=ttk.Entry(self.window.con,width=10)
                            a1.grid(row=self.cxy[0]+1,column=1,padx=(0, 4), pady=(5, 5), sticky="nsew")
                            a1.bind("<KeyPress>", self.movefocus)
                            a1.bind("<Button-1>",self.adjustcxy)
                            b=ttk.Entry(self.window.con,width=40,font=self.efont)
                            b.grid(row=self.cxy[0]+1,column=2,padx=(3, 4), pady=(5, 5), sticky="nsew")
                            b.bind("<KeyPress>", self.movefocus)
                            b.bind("<Button-1>",self.adjustcxy)
                            self.nwlabel.insert(a,[a1,b,[2,self.nwlabel[self.cxy[0]][3][1],self.nwlabel[self.cxy[0]][3][2]+1,0],[3,self.nwlabel[self.cxy[0]][3][2]+1,0,0]])
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
                        b=ttk.Entry(self.window.con,width=40,font=self.efont)
                        b.grid(row=self.cxy[0]+1,column=2,padx=(3, 4), pady=(5, 5), sticky="nsew")
                        b.bind("<KeyPress>", self.movefocus)
                        self.nwlabel.insert(self.cxy[0]+1,[0,b,0,[3,self.nwlabel[self.cxy[0]][3][1],self.nwlabel[self.cxy[0]][3][2],1]])
                        self.cxy[0]+=1
                    elif m=='d':
                        if self.cxy[0]==len(self.nwlabel)-1:
                            a=ttk.Entry(self.window.con,width=15)
                            a.grid(row=self.cxy[0]+1,column=1,padx=(0, 4), pady=(5, 5), sticky="nsew")
                            b=ttk.Label(self.window.con,width=40,text="-------------------------------------------------------------------------------------------")
                            b.grid(row=self.cxy[0]+1,column=2,padx=(0, 4), pady=(5, 5), sticky="nsew")
                            a.bind("<KeyPress>", self.movefocus)
                            self.nwlabel.append([a,b,[1,self.nwlabel[self.cxy[0]][3][1],0,0],0])
                            self.cxy[0]+=1
                            self.cxy[1]=0
                        else:
                            if self.nwlabel[self.cxy[0]+1][3]!=0:
                                self.cxy[0]+=1

            if m=='esc' or m=='nw':
                if self.newword.name!="" and self.nwlabel[2]!=[]:
                    length=0
                    newwordstrline=[]
                    self.cxy=[0,0]
                    for lines in self.nwlabel:
                        if lines[3]!=0:
                            if self.nwlabel.index(lines)==2:
                                newwordstrline.append([lines[0].get(),lines[1].get(),1])
                            else:
                                newwordstrline.append([lines[0].get(),lines[1].get(),0])
                            length+=1
                    self.CNB.pagedatalist[-1].append([self.newword.index,0,length-1,length])
                    self.CNB.lastwordindex+=1
                    self.CNBdata.append({"name":self.newword.name,"index":self.newword.index,"collocation":self.newword.collocation,"meaning":self.newword.meaning,"egsentence":self.newword.egsentence,"proficiency":0})
                self.newword=None
                if m=='esc':
                    self.escape()
                else:
                    self.newpagelist[-1]+=newwordstrline
                    self.manageconfigpage()

            print(self.cxy)
            print(self.nwlabel)
            self.nwlabel[self.cxy[0]][self.cxy[1]].focus_set()

    def remove(self,event):
        pass

    def left(self):
        if self.state==1:
            if self.newpageindex!=0:
                self.newpageindex-=1
                self.displaystrs(self.newpagelist[self.newpageindex])
        else:
            if self.CNBpage!=0:
                self.CNBpage-=1
                self.decodeintostr(self.CNB.pagedatalist,self.CNBpage,self.CNBline)
                self.displaystrs(self.pagelinestr[self.CNBpage])

    def right(self):
        if self.state==1:
            if self.newpageindex!=len(self.newpagelist)-1:
                self.newpageindex+=1
                self.displaystrs(self.newpagelist[self.newpageindex])
        else:
            if self.CNBpage!=len(self.CNB.pagedatalist)-1:
                self.CNBpage+=1
                self.decodeintostr(self.CNB.pagedatalist,self.CNBpage,self.CNBline)
                self.displaystrs(self.pagelinestr[self.CNBpage])

    def manageconfigpage(self):
        self.newpagelist[-1]=[x for x in self.newpagelist[-1]  if x!=[0,0,0] ]
        while len(self.newpagelist[-1])>self.conpageline:
            self.newpagelist.append([self.newpagelist[-1][self.conpageline:]])
            self.newpagelist[-2]=self.newpagelist[-2][:self.conpageline]
        while len(self.newpagelist[-1])<self.conpageline:
            self.newpagelist[-1].append([0,0,0])
        self.window.con.grid_remove()
        self.configblock()
        print(self.newpagelist[self.newpageindex])
        self.displaystrs(self.newpagelist[self.newpageindex])

    def escape(self):
        print("into escape")
        self.state=0
        self.newpagelist=[[]]
        self.window.con.grid_remove()
        self.window.lp.grid_remove()
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
    root.title("NBook")

    # Simply set the theme
    root.tk.call("source", "azure.tcl")
    root.tk.call("set_theme", "dark")

    app = Manager(root)
    #app.pack(fill="both", expand=True)
    app.update()
    # Set a minsize for the window, and place it in the middle
    root.minsize(root.winfo_width(), root.winfo_height())
    x_cordinate = int((root.winfo_screenwidth() / 2) - (root.winfo_width() / 2))
    y_cordinate = int((root.winfo_screenheight() / 2) - (root.winfo_height() / 2))
    root.geometry("+{}+{}".format(x_cordinate, y_cordinate-20))

    root.mainloop()
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