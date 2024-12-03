from transformers import VitsModel, AutoTokenizer
import torch
import scipy
import os
import time
import datetime
from pygame import mixer
from IPython.display import Audio
from pygame import mixer, _sdl2 as devicer

# look at your devices and edit both DEVICENAME_
def show_devices():
    mixer.init()
    devices={"Inputs": devicer.audio.get_audio_device_names(True),"Outputs": devicer.audio.get_audio_device_names(False)}
    mixer.quit()
    return devices

DEVICENAME_VIRTUAL_MIC = 'CABLE Input (VB-Audio Virtual Cable)'
DEVICENAME_LOUDSPEAKER = 'Динамики (2- Realtek High Definition Audio)'

# The first start will load model. It gets about 2 min
# Next playing gets about 3 sec

def Plaaay(mic=True,loudspeaker=True,text='',):
    model = VitsModel.from_pretrained("facebook/mms-tts-rus")
    tokenizer = AutoTokenizer.from_pretrained("facebook/mms-tts-rus")
    inputs = tokenizer(text, return_tensors="pt")
    with torch.no_grad():
        output = model(**inputs).waveform
    #scipy.io.wavfile.write("techno.wav", rate=model.config.sampling_rate, data=output)
    ii=Audio(output, rate=model.config.sampling_rate)
    file=datetime.datetime.now().strftime("%d%m%Y-%H%M%S")
    os.makedirs(os.path.dirname('audios/'), exist_ok=True)
    with open('audios/'+file+'.wav', 'wb') as f:
        f.write(ii.data)
    print('file done')
    if mic==True:
        print('Mic playing')
        mixer.init(devicename = DEVICENAME_VIRTUAL_MIC) # Initialize it with the correct device
        mixer.music.load('audios/'+file+'.wav') # Load the mp3
        mixer.music.play() # Play it
        mixer.music.set_volume(1.0)
        while mixer.music.get_busy():  # wait for music to finish playing
            time.sleep(1)
        mixer.quit()
    if loudspeaker==True:
        print('Loudspeaker playing')
        mixer.init(devicename = DEVICENAME_LOUDSPEAKER) # Initialize it with the correct device
        mixer.music.load('audios/'+file+'.wav') # Load the mp3
        mixer.music.play() # Play it
        mixer.music.set_volume(0.7)
        while mixer.music.get_busy():  # wait for music to finish playing
            time.sleep(1)
        mixer.quit()
    print('stop')

TEXT='''
Нет, на работу не надо в воскресенье
'''
Plaaay(text=TEXT)
