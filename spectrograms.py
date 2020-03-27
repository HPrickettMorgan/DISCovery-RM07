import numpy as np
np.set_printoptions(suppress=True)
from scipy.io import wavfile
from math import pi
from math import sqrt
from math import log10
from scipy.signal import spectrogram
from scipy.ndimage import gaussian_filter1d
from matplotlib.colors import LogNorm
from scipy.signal import find_peaks
import datetime
from pathlib import Path

def rms(signal):
    return sqrt(np.average(np.power(signal, 2)))

res_list = []
for path in Path('.').glob("media/*.wav"):
    #Read in file
    sample_rate, signal = wavfile.read(path)
    signal = signal.sum(axis=1)/2
    
    #Calculate spec
    freq_ax, time_ax, spec = spectrogram(signal, sample_rate, window="hann", nperseg=8192, noverlap=8192*0.25, scaling="spectrum")
    dt = time_ax[1]-time_ax[0]

    #Calculate relative loudness
    low_range_spec = spec[freq_ax <= 100, :]
    high_range_spec = spec[freq_ax > 100, :]
    low_range_total = np.sum(low_range_spec, axis=0)
    high_range_total = np.sum(high_range_spec, axis=0)
    relative_loudness = gaussian_filter1d(low_range_total/(high_range_total * (low_range_total+high_range_total)), 
                                          mode='reflect', 
                                          sigma=5).clip(0,0.01)
    relative_loudness[0] = 0
    relative_loudness[-1] = 0
    relative_loudness = ((relative_loudness)/relative_loudness[int(20/dt):-int(20/dt)].max()).clip(0, 1)
    
    #Find peaks
    peaks, peaks_data = find_peaks(relative_loudness, distance=60/dt, width=0.5/dt, height=0.01, rel_height=0.5)    

    track_seps = [(datetime.datetime(1970,1,1) + datetime.timedelta(seconds=peak)).strftime("%M:%S") for peak in peaks*dt]

    silence = np.concatenate(
        [
            signal[int(left*dt*sample_rate):int(right*dt*sample_rate)] 
            for left, right in 
            zip(peaks_data["left_ips"], peaks_data["right_ips"])
        ]
    ).astype('int16')
    wavfile.write(f"silence/{path.stem}_silence.wav", sample_rate, silence)

    ref_time = np.linspace(0,10, 44100*10)
    ref = np.sin(997*2*pi*ref_time) * 32767
    rms_ref = rms(ref)

    db_ref = 20 * log10(rms_ref/rms_ref)
    db_song = 20 * log10(rms(signal)/rms_ref)
    db_silence = 20 * log10(rms(silence)/rms_ref)
    snr = db_song - db_silence

    res_list.append(
        {"Name": path.stem, 
        "Results": {"Signal To Noise": snr, 
                    "Record Volume": db_song, 
                    "Number of Tracks": len(track_seps), 
                    "Tracking Markers": track_seps
                    }
        }
    )

with open("results.json", "w") as f:
    f.write(str(res_list))