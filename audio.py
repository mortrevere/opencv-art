import pyaudio
import numpy as np

class AudioCapture():
    def __init__(self):
        print("init audio")


        self.CHUNK = 1024 # number of data points to read at a time
        self.RATE = 44100 # time resolution of the recording device (Hz)

        self.p=pyaudio.PyAudio() # start the PyAudio class
        i_device = 9
        info = self.p.get_host_api_info_by_index(0)
        numdevices = info.get('deviceCount')
        for i in range(0, numdevices):
            if (self.p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                name = self.p.get_device_info_by_host_api_device_index(0, i).get('name')
                print("Input Device id ", i, " - ", name)
                if "pulse" in name:
                    i_device = i
        print("chose", i_device)
        self.stream=self.p.open(format=pyaudio.paInt16,channels=1,rate=self.RATE,input=True, frames_per_buffer=self.CHUNK, input_device_index=i_device) #uses default input device
        self.intensity = 0
    def peaking(self):
        #print(self.maxi * 1.1 , self.maxi_intensity)
        return self.maxi * 1.01 > self.maxi_intensity
    def capture(self):
        
        n = 10
        avgs = [0]*n
        maxis = [0]*n
        i = 0

        print("capture audio on @ ", n*self.CHUNK/self.RATE)

        # create a numpy array holding a single read of audio data
        while True: #to it a few times just to see
            data = np.fromstring(self.stream.read(self.CHUNK),dtype=np.int16)
            avg = np.mean(data) 
            maxi = np.max(data)
            avgs[i%n] = avg
            maxis[i%n] = maxi
            #print(maxis, avgs)
            m = sum(maxis)/n
            a = sum(avgs)/n
            a = max(a, 0)
            self.maxi = maxi
            self.maxi_intensity = max(maxis)
            intensity = maxi/(m+2*a)
            #if intensity > 1:
            #    print(intensity)
            #else:
            #    print()
            if intensity:
                self.intensity = intensity
            #if maxi > ((sum(maxis) + sum(avgs))/(n/1.2)):
            #    print(data)
            i += 1

