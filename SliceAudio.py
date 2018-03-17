import librosa
import numpy as np
import os
#pip install progressbar2
from progressbar import ProgressBar
import shutil
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2TkAgg
import matplotlib.backends.tkagg as tkagg
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure



def remove_folder(path):
    # check if folder exists
    if os.path.exists(path):
         # remove if exists
         shutil.rmtree(path)

def prepare(audio, RATE):
    audio=librosa.to_mono(audio)
    audio=librosa.util.fix_length(audio,RATE)
    audio=librosa.util.normalize(audio)
    return audio


def getFingerPrint(audio, RATE):
    audio=prepare(audio,RATE)
    cqt=librosa.cqt(audio,sr=RATE,hop_length=2048)
    return cqt.flatten('F')

def basename(file):
    file = os.path.basename(file)
    return os.path.splitext(file)[0]

def removeToClose(times,tempo,spaceModificer=20):
    arrayIndex=[]
    for i in range(0,len(times)-1):
        #tempo/20 precysion of slice ->20 bigger make more space
        if times[i+1]-times[i]<(tempo/spaceModificer):
            arrayIndex.append(i+1)

    return np.delete(times,arrayIndex)
def moveBack(date,moveOn=0):
    if(moveOn==0):
        moveOn=date[0]
    for i in range(0,len(date)):
        date[i]=date[i]-moveOn
    return date

def SliceFileOnFragments(frame,tk,NAME="",spaceModificer=20,pickExpadner=5):
    remove_folder("beats")
    if(NAME[-4::]!=".wav"):
        NAME=NAME+".wav"
    fullAudio,RATE = librosa.load(NAME)

    print(len(fullAudio)/RATE)
    audioNormalizte=librosa.util.normalize(fullAudio**pickExpadner)
    percusive=librosa.effects.percussive(audioNormalizte)
    o_env = librosa.onset.onset_strength(percusive,sr=RATE,feature=librosa.cqt)
    print(len(o_env))
    onsetFrames = librosa.onset.onset_detect(onset_envelope=o_env,sr=RATE)
    tempo,timeBeats=librosa.beat.beat_track(percusive,RATE,start_bpm=60)

    print(tempo)
    print(onsetFrames)
    onsetFrames=removeToClose(onsetFrames,tempo,spaceModificer)

    print(onsetFrames)
    onsetFrames=moveBack(onsetFrames)
    # Ta tablica interesuje mnie do MIDI
    print(onsetFrames)
    onsetSamples = list(librosa.frames_to_samples(onsetFrames))

    print(onsetSamples)
    for i in onsetSamples:
        print(i/RATE)
    onsetSamples=np.concatenate(onsetSamples,len(fullAudio))

    starts = onsetSamples[0:-1]
    stops=onsetSamples[1:]
    print(starts)
    print(stops)
    print(len(onsetFrames))
    clicks = librosa.core.clicks(frames=onsetFrames, sr=RATE, length=len(fullAudio))
    librosa.output.write_wav("output.wav", fullAudio + clicks, RATE)




    fig = Figure(facecolor='white')
    axis = fig.add_subplot(111)
    time_vector = np.arange(0, len(fullAudio)/RATE, 1/RATE)
    axis.plot(time_vector,clicks)
    axis.plot(time_vector,fullAudio)
    axis.set_xlabel("Seconds")


    canvas = FigureCanvasTkAgg(fig, frame)


    canvas.show()
    #canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH,expand=True)
    canvas.get_tk_widget().grid(column=0, row=4, columnspan=4, rowspan=4, sticky='nsew')

    toolbar_frame=tk.LabelFrame(frame,text="")
    toolbar_frame.grid(column=0,row=3,columnspan=2)
    toolbar=NavigationToolbar2TkAgg(canvas,toolbar_frame)

    frame.update()


    print(timeBeats)


    #start slicing
    analysisFolder="beats"
    samplesFolder=os.path.join(analysisFolder,"samples")
    print(analysisFolder)
    try:
        os.makedirs(samplesFolder)
    except:
        pass

    vectors = []
    words = []
    filenames = []

    #TODO MakeProgressBar in new Window
    pbar=ProgressBar()
    for i,(start,stop) in enumerate(pbar(zip(starts,stops))):

        audio=fullAudio[start:stop]
        filename=os.path.join(samplesFolder,str(i)+".wav")
        librosa.output.write_wav(filename,audio,RATE)
        vector=getFingerPrint(audio,RATE)
        word = basename(filename)
        vectors.append(vector)
        words.append(word)
        filenames.append(filename)
    np.savetxt(os.path.join(analysisFolder,"vectors.txt"),vectors,fmt='%.5f',delimiter='\t')
    np.savetxt(os.path.join(analysisFolder,"words.txt"),words,fmt='%s')
    np.savetxt(os.path.join(analysisFolder,'filenames.txt'),filenames,fmt='%s')



    print("END_SLICE")

#SliceFileOnFragments(NAME="MonoRythm")
