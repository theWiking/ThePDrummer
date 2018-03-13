import pyaudio
import wave
from array import array
import copy
global ainfo
ainfo=""
def oberverInfo(info):
    global ainfo
    if (info!=ainfo):
        ainfo=copy.deepcopy(info)
    return ainfo

def recordSample(FILE_NAME="Record",RECORD_SECONDS=15,RATE=44100,CHUNK=1024,CHANNELS=1):
    oberverInfo("")
    FORMAT = pyaudio.paInt16
    FILE_NAME=FILE_NAME+".wav"
    # instantiate the pyaudio
    audio = pyaudio.PyAudio()
    stream=audio.open(format=FORMAT,channels=CHANNELS,rate=RATE,input=True,frames_per_buffer=CHUNK)
    # Start recording
    frames=[]
    seconds=0
    print("REDY")
    oberverInfo("Ready")
    while (True):
        data = stream.read(CHUNK)
        data_chunk = array('h', data)
        vol = max(data_chunk)
        if (vol >= 250):
            frames.append(data)
            for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                data = stream.read(CHUNK)
                data_chunk = array('h', data)
                vol = max(data_chunk)
                frames.append(data)

                if (seconds != round(i * CHUNK / RATE)):
                    seconds = round(i * CHUNK / RATE)
                    print("Recording: ", seconds,"s on ",RECORD_SECONDS)
                    oberverInfo(str(seconds))
            break
    # end of recording
    stream.stop_stream()
    stream.close()
    audio.terminate()
    # writing to file
    wavfile = wave.open(FILE_NAME, 'wb')
    wavfile.setnchannels(CHANNELS)
    wavfile.setsampwidth(audio.get_sample_size(FORMAT))
    wavfile.setframerate(RATE)
    wavfile.writeframes(b''.join(frames))  # append frames recorded to file
    wavfile.close()
    oberverInfo("end")
    pass

#test:
#recordSample(FILE_NAME="test",RECORD_SECONDS=5)