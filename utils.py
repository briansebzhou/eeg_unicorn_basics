'''
Created by Victor Delvigne
ISIA Lab, Faculty of Engineering University of Mons, Mons (Belgium)
IMT Nord Europe, Villeneuve d'Ascq (France)
victor.delvigne@umons.ac.be
Source: TBD
Copyright (C) 2021 - UMons/IMT Nord Europe
This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.
This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.
You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
'''

import os
import cv2
import glob
import tkinter 
import datetime

import numpy as np

from tqdm import tqdm
from scipy import signal
from playsound import playsound
from pylsl import StreamInlet, resolve_stream

def intro_page(duration=15000):
    m = tkinter.Tk()
    m.title("random page")
    m.geometry('720x420')
    tkinter.Label(m, text="Experiment Begin", fg="red", font=('Helvetica 28')).pack(pady=150)
    m.after(duration, lambda:m.destroy())
    m.mainloop()

def play_vid(vid_path, vid_id=0, duration=5000):
    m = tkinter.Tk()
    m.title("random page")
    m.geometry('720x420')
    tkinter.Label(m, text="Video "+str(vid_id), fg="blue", font=('Helvetica 28')).pack(pady=150)
    m.after(duration, lambda:m.destroy())
    m.mainloop()
    playsound(vid_path, block=True)

def len_vid(path):
    data = cv2.VideoCapture(path)
    frames = data.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = int(data.get(cv2.CAP_PROP_FPS))
    return frames/fps

def gen_coeff(cuttoff, fs=50, filtype='lowpass', order=4):
    if filtype == 'lowpass':
        b,a = signal.butter(order, cuttoff[0]/(fs/2), filtype)
    elif filtype == 'bandpass':
        b,a = signal.butter(order, [cuttoff[0]/(fs/2), cuttoff[1]/(fs/2)], filtype)
    elif filtype == 'highpass':
        b,a = signal.butter(order, cuttoff[0]/(fs/2), filtype)
    return b, a 

def apply_filter(sig, b, a):
    sig = min_max_scale(sig)
    sig -= sig.mean()
    return signal.filtfilt(b, a, sig)

def min_max_scale(x):
    x -= x.min()
    x = x/x.max()
    return x

def signal_segmentation(sig, wind_len=4, overlapping=0.2, fs=50):
    win = wind_len*fs
    x = []
    end = False
    i = 0
    while not end:
        if i+win < len(sig):
            x.append(sig[i:i+win])
            i += int(win*(1-overlapping))
        else: 
            end = True
    return np.asarray(x)

def compute_entropy(sig):
    return 0.5*np.log10(2*np.pi*np.exp(1)*np.var(sig))

def sig_vid(path):
    X = []
    Y = []
    n_session = len(os.listdir(os.path.join(path)))//2
    for i in range(1, n_session+1):
        sig_path = glob.glob(os.path.join(path, 'session_'+str(i)+'_sig*'))[0]
        log_path = glob.glob(os.path.join(path, 'session_'+str(i)+'_log*'))[0]

        log = np.loadtxt(log_path)
        sig = np.loadtxt(sig_path)

        for vid in np.unique(log[:, -1]):
            if vid != 0 : #if intro
                
                x = sig[log[:, -1]==vid]
                y = log[log[:, -1]==vid]

                X.append(np.asarray(x))
                Y.append(np.asarray(y))
    return X, Y

def gen_feat(signals, label, filters):
    Features = np.zeros((1153, 8, 4))
    Label = np.zeros((1153))
    i = 0
    for vid in range(len(signals)):
        s = signals[vid][:, 1:9] #we keep only the EEG channels 
        l = label[vid][:, -1].astype(int)
        for e in range(s.shape[-1]): #for each electrodes
            for f in range(len(filters)): 
                b, a = filters[f] 
                x = apply_filter(s[:, e], b, a)
                x = signal_segmentation(x)
                for t in range(x.shape[0]):
                    Features[i+t, e, f] = compute_entropy(x[t])
                    Label[i+t] = l[0]
        i += t
    return Features, Label

def gen_val_arousal(vid_info, film_id):
    y = []
    for f in film_id:
        y.append([ float(vid_info[f-1][2]), float(vid_info[f-1][4])])
    y = np.asarray(y)
    tmp = np.vstack(
        ((y[:, 0] > np.median(y[:, 0])).astype(int), 
        ((y[:, 1] > np.median(y[:, 1])).astype(int))))
    y = np.transpose(tmp)
    return y
