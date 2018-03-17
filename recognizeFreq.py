# Read in a WAV and find the freq's
import pyaudio
import wave
import numpy as np
import copy
global ainfo

def oberverInfo(info):
    global ainfo
    if (info!=ainfo):
        ainfo=copy.deepcopy(info)
    return ainfo

def recognizeFreq(NAME="MonoD"):
    global ainfo
    ainfo= 0
    print(NAME)
    if(NAME[-4::]!=".wav"):
        NAME=NAME+".wav"

    wf=wave.open(NAME,'rb')
    swidth=wf.getsampwidth()
    RATE=wf.getframerate()
    thefreq=0
    RECORDED_SECONDS=wf.getnframes()/RATE
    #print("Length of audio: ", round(RECORDED_SECONDS))
    #Window of all sample
    chunk = round(RATE * RECORDED_SECONDS)
    # use a Blackman window
    window = np.blackman(chunk)
    # open stream
    p = pyaudio.PyAudio()
    # read some data
    data = wf.readframes(chunk)
    # find the frequency of each chunk
    while len(data) == chunk * swidth:

        # unpack the data and times by the hamming window
        indata = np.array(wave.struct.unpack("%dh" % (len(data) / swidth), data)) * window
        # Take the fft and square each value
        fftData = abs(np.fft.rfft(indata)) ** 2
        # find the maximum
        which = fftData[1:].argmax() + 1
        # use quadratic interpolation around the max
        if which != len(fftData) - 1:
            y0, y1, y2 = np.log(fftData[which - 1:which + 2:])
            x1 = (y2 - y0) * .5 / (2 * y1 - y2 - y0)
            # find the frequency and output it
            thefreq = (which + x1) * RATE / chunk
            # TODO why it double freq
            thefreq = thefreq / 2

            #print("The freq1 is %f Hz." % (thefreq))
        else:
            thefreq = which * RATE / chunk
            #print("The freq is %f Hz." % (thefreq))
        # read some more data
        data = wf.readframes(chunk)
    p.terminate()
    #print("end")
    ainfo=copy.deepcopy(thefreq)
    return thefreq

#print(recognizeFreq("MonoD"))