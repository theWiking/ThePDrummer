# #########################################
# Mateusz Koch
# This is program on master work on study
# This could help guitar player to make midi part on dums
# #########################################


#IMPORTS

import tkinter as tk
from tkinter import messagebox as msg, filedialog

import recordWave
import recognizeFreq
import SliceAudio

from threading import Thread
from time import sleep

#PROPERTYS
__version__="alfa"
__email__='@.gmail.com'
__author__='Matesz Koch'

#FUNCTIONS
def FrameMaker(parent,title="",column=0,row=0):

    MainFrame = tk.LabelFrame(parent, text=title)
    MainFrame.grid(column=column, row=row)
    MainFrame.columnconfigure(0, weight=1)
    MainFrame.rowconfigure(0, weight=1)
    MainFrame.pack(fill="both", expand="yes")

    return MainFrame

def _msgBox(title,infoText):
    dialogeBox=tk.Toplevel(window)
    dialogeBox.title(title)
    dialogeBox.geometry("200x100+100+100")
    dialogeBox.attributes("-toolwindow", 1)
    dialogeBox.grab_set()
    dialogeBox.focus_force()
    #dialogeBox.after(10,lambda: )
    frame=FrameMaker(dialogeBox)
    tk.Label(frame,text=infoText).grid(column=0,row=0)

def StartLoop():
    window.mainloop()
def _quit(): # 7
    window.quit()
    window.destroy()
    exit()

def ShowVersion():
    _msgBox("Version",__version__)
def ShowContact():
    _msgBox("Contact","Contact to "+__author__+"\n"+__email__)
def ShowAbout():
    _msgBox("About","")
def ShowHelp():
    pass

def CleanFrame(frame):
    for widget in frame.winfo_children():
        widget.destroy()
def ChangeState(frame,state=True):
    stateString = 'disabled'
    if(state):
        stateString = 'normal'

    for child in frame.winfo_children():
        child.configure(state=stateString)
def testValDigit(inStr,i,acttyp):
    ind=int(i)
    if acttyp == '1': #insert
        if not inStr[ind].isdigit():
            return False
    return True


def _LoadSechamt(title,parent,clear=True,column=4,row=4):
    if(clear):
        CleanFrame(mainFrame)
    frame = FrameMaker(parent,title=title)
    for i in range(0,column):
        frame.columnconfigure(i, weight=1)
    for i in range(0,row):
        frame.rowconfigure(i, weight=0)
    return frame

# Change background in frame
def recordBackground(frame):

    while(True):

        if(recordWave.ainfo==""):
            frame.configure(background="white")
        elif(recordWave.ainfo=="Ready"):
            frame.configure(background="yellow")
        elif(recordWave.ainfo=="end"):
            frame.configure(background="grey")
            break
        else:
            frame.configure(background="red")
        sleep(0.1)
    pass
def retunValueFreq(frame):
    while(True):
        if(recognizeFreq.ainfo!=0):
            #_msgBox("test ",recognizeFreq.ainfo)
            dictFrame=frame.__dict__
            dictFrame=dictFrame['children']
            dictFrame['!label']["text"]="Freq: "+" "+str(recognizeFreq.ainfo)


            break
        sleep(0.1)

#FUNCTION BUTTONS

def runRecord(frame,name="",seconds=0):

    print("startRecord")
    th=Thread(target=recordWave.recordSample,kwargs={'FILE_NAME':name,"RECORD_SECONDS":seconds})
    th.daemon = True
    th.start()

    thObs = Thread(target=recordBackground, args={frame})
    thObs.daemon=True
    thObs.start()

    print("endRecord")
    pass
    #return resp.status_code
#TODO Copy file to folder and make all on local folder
def sliceAudio(frame,name=""):
    dictFrame=frame.__dict__
    dictFrame=dictFrame['children']
    print(dictFrame)
    space=int(dictFrame['!entry'].get())
    pick=int(dictFrame['!entry2'].get())
    th1=Thread(target=SliceAudio.SliceFileOnFragments,kwargs={'frame':frame,'tk':tk,'NAME':name,'spaceModificer':space,'pickExpadner':pick})
    th1.deamon=True
    th1.start()
    #space, pick,
    pass

#TODO add funcion assync
def findTempoAnalize(frame,path=""):
    #print(path)
    pass
def findFreqAnalize(frame,path=""):
    th1=Thread(target=recognizeFreq.recognizeFreq,kwargs={'NAME':path})
    th1.daemon=True
    _msgBox("Start","Now the audio will be analize")
    th1.start()
    thFreq =Thread(target=retunValueFreq,kwargs={'frame':frame})
    thFreq.daemon=True
    thFreq.start()


    pass
# Load file (parent frame what button unlock/lock and where pass frame
def loadFile(frame,button,function):
    fileName=filedialog.askopenfilename(initialdir = "ThePDrummer/",title = "Select file",filetypes=(("wave files","*.wav"),("all files","*.*")))
    test=fileName[len(fileName)-4::]
    if(test!=".wav"):
        _msgBox("ERROR","NOT WAVE")
        button['state']="disabled"
    else:
        button['state'] = "normal"
        button['command']=lambda: function(frame, fileName)


    pass

#COMBO Load write patter view
def LoadWP():
    frame = _LoadSechamt("Write Pattern",mainFrame)
    pass
#COMBO Load Play and get pattern view
def LoadPnGP():
    frame = _LoadSechamt("Play and get pattern",mainFrame)
    pass
#COMBO Load Generate Patter view
def LoadGP():
    frame = _LoadSechamt("Generate Pattern",mainFrame)
    pass
# Load Midi player view
def LoadMV():
    frame = _LoadSechamt("Midi player (drum)", mainFrame)
    pass
# Load slice audio view
def LoadSA():
    frame = _LoadSechamt("Slice Audio", mainFrame)
    label1=tk.Label(frame, text="Space Parametr").grid(column=0, row=0)

    label2=tk.Label(frame, text="Pick Parametr").grid(column=1, row=0)


    space = tk.IntVar(value=20)
    textSpaceParametr = tk.Entry(frame, textvariable=space, validate="all")
    textSpaceParametr['validatecommand'] = (textSpaceParametr.register(testValDigit), '%P', '%i', '%d')
    textSpaceParametr.grid(column=0, row=1, sticky='nsew')


    pick = tk.IntVar(frame,value=5)
    textPickParametr = tk.Entry(frame, textvariable=pick)
    textPickParametr['validatecommand'] = (textPickParametr.register(testValDigit), '%P', '%i', '%d')
    textPickParametr.grid(column=1, row=1, sticky="nsew")


    buttonSliceIt=tk.Button(frame,text="Slice Audio",state="disabled")
    buttonSliceIt.grid(column=3,row=0,rowspan=2,sticky="nsew")

    tk.Button(frame, text="Load File", command=lambda: loadFile(frame, buttonSliceIt, sliceAudio)).grid(column=2, row=0,rowspan=2,sticky="nsew")

    pass
# Load Make midi view
def LoadMMV():
    frame = _LoadSechamt("Make midi pattern", mainFrame)
    pass
# Load Find Tempo view
#TODO fucntion to tempo
def LoadFTV():
    frame = _LoadSechamt("Find Tempo", mainFrame)

    infoLabel=tk.Label(frame,text="Tempo: ").grid(column=0,row=0)
    buttonFindTempo = tk.Button(frame, text="Find Tempo", state="disabled")
    buttonFindTempo.grid(column=2, row=0,sticky="nsew")

    tk.Button(frame,text="Load File",command=lambda :loadFile(frame,buttonFindTempo,findTempoAnalize)).grid(column=1,row=0)

    pass
# Load Find Freq view
def LoadFFV():
    frame = _LoadSechamt("Find Freq in sample", mainFrame)
    frame.columnconfigure(0, weight=0)
    tk.Label(frame, text="Freq: ",width=50).grid(column=0, row=0,stick='w')
    buttonFindFreq = tk.Button(frame, text="Find Freq", state="disabled")
    buttonFindFreq.grid(column=2, row=0,sticky="nsew")
    frame.pack()
    tk.Button(frame, text="Load File", command=lambda: loadFile(frame, buttonFindFreq,findFreqAnalize)).grid(column=1, row=0,sticky="nsew")
    frame.pack()
    pass
# Load Scales on fingerboard view
def LoadSCALES():
    frame = _LoadSechamt("Scales", mainFrame)
    pass
# Load Tuner view
def LoadTuner():
    frame = _LoadSechamt("Tuner", mainFrame)

    pass
# Load Record audio view
def LoadRA():
    frame=_LoadSechamt("Record Wave",mainFrame)

    tk.Label(frame,text="Seconds of record").grid(column=0,row=0)
    tk.Label(frame,text="Name of record").grid(column=1,row=0)

    seconds = tk.IntVar()
    textBoxSeconds = tk.Entry(frame, textvariable=seconds,validate="all")
    textBoxSeconds['validatecommand']=(textBoxSeconds.register(testValDigit),'%P','%i','%d')
    textBoxSeconds.grid(column=0, row=1,sticky='nsew')

    namefile=tk.StringVar()
    textBoxName= tk.Entry(frame,textvariable=namefile)
    textBoxName.grid(column=1,row=1,sticky="nsew")


    buttonRecord=tk.Button(frame,text="Record",command=lambda:runRecord(frame,name=namefile.get(),seconds=seconds.get()))
    buttonRecord.grid(column=2,row=0,rowspan=2,sticky="nsew")


    frame.pack()
#TODO just for testes, i futre get set image here
def LoadSimple():
    tk.Label(mainFrame,text="Hello").grid(column=0,row=0)
#def FrameMaker(MainFrame):
 #   tk.Label(MainFrame,text="test").grid(column=0,row=0)

#MENUS
def HelpBar(menuBar):
    help = tk.Menu(menuBar, tearoff=0)
    help.add_command(label="Help",command=ShowHelp())
    help.add_command(label="Contact", command=ShowContact)
    help.add_command(label="Version", command=ShowVersion)
    help.add_command(label="About", command=ShowAbout)
    return help
def FileMenu(menuBar):
    file = tk.Menu(menuBar,tearoff=0)
    drumm = tk.Menu(file,tearoff=0)
    drumm.add_command(label="Write Pattern",command=LoadWP,state="disabled")
    drumm.add_command(label="Play and get pattern",command=LoadPnGP,state="disabled")
    drumm.add_command(label="Genarte Pattern",command=LoadGP,state="disabled")
    file.add_cascade(label='Drumm programs', menu=drumm, underline=0)
    file.add_separator()
    simpleFunction=tk.Menu(file,tearoff=0)
    simpleFunction.add_command(label="Play Midi",command=LoadMV,state="disabled")
    simpleFunction.add_command(label="Slice audio by picks",command=LoadSA)
    simpleFunction.add_command(label="Record Wave",command=LoadRA)
    simpleFunction.add_command(label="Make midi",command=LoadMMV,state="disabled")
    simpleFunction.add_command(label="Find Tempo",command=LoadFTV,state="disabled")
    simpleFunction.add_command(label="Find Freq",command=LoadFFV)
    file.add_cascade(label='Simple Functionality',menu=simpleFunction,underline=0)
    file.add_separator()
    addons=tk.Menu(file,tearoff=0)
    addons.add_command(label="Scales",command=LoadSCALES,state="disabled")
    addons.add_command(label="Tuner",command=LoadTuner,state="disabled")
    file.add_cascade(label="Addons",menu=addons,underline=0)
    file.add_separator()
    file.add_command(label="Exit",command=_quit)
    return file
def Menus():
    menuBar = tk.Menu(window)
    window.config(menu=menuBar)
    file=FileMenu(menuBar)
    help=HelpBar(menuBar)
    menuBar.add_cascade(label="File",menu=file)
    menuBar.add_cascade(label="Help", menu=help)



#INIT
window=tk.Tk()
window.title('The PDrummer')
window.geometry("800x600")
window.resizable(0,0)
Menus()
mainFrame=FrameMaker(title="",parent=window)
LoadSimple()
mainFrame.pack()


#START
StartLoop()

