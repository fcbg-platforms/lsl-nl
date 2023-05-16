import argparse
import socket
import time
import struct
import random
import numpy as np
import psychtoolbox as ptb

def startAmp(UDP_IP = "127.0.0.1",UDP_PORT = 5000 ,nChannels=64,sr=.001,duration=60):
    
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    
    sampleCount=0
    size = 68+nChannels*4 + 4
    
    
    range10 = range(10)
    f0 = 4
    cycle_duration = 1/f0
    
    t = np.arange(0,cycle_duration,sr)
    cycle_nSamples = len(t)
    
    t = t.reshape((1,len(t)))
    
    ones = np.ones((nChannels,1))
    mult = ones@t
    
    data = (np.sin(mult*2*np.pi*f0)*1e6).astype(np.int32)
    
    print(data.shape)
    
    
    print('Sending data...')
    t0 = ptb.GetSecs()
    while(True):
        t1 = ptb.GetSecs()
        stx = 0
        id = sampleCount
        ts = ptb.GetSecs() - t0
        status = 0
        ttl = 0
        packet = bytearray(size)
        
        # pack header
        struct.pack_into('<3Id2I10I',packet,0,stx,id,size,ts,status,ttl,*range10)
        
        # t = sampleCount*sr
        # data = (np.sin(np.ones(nChannels)*2*np.pi*sampleCount*sr*f0)*1e6).astype(np.int32)
        # struct.pack_into('<' + str(nChannels) + 'i', packet, 68,*data)
        
        struct.pack_into('<' + str(nChannels) + 'i', packet, 68,*(data[:,sampleCount%cycle_nSamples]))
        # struct.pack_into('<' + str(nChannels) + 'i', packet, 68,*(data[:,sampleCount]))
        # struct.pack_into('<' + str(nChannels) + 'i', packet, 68,*(np.ascontiguousarray(data[:,sampleCount%cycle_nSamples])))
        
        # pack footer
        struct.pack_into('<I', packet, 68 + nChannels*4, 0)
        
        sock.sendto(packet,(UDP_IP, UDP_PORT))
        sampleCount += 1
        
        ptb.WaitSecs('UntilTime',t1+sr)
        if (ptb.GetSecs() - t0) > duration:
            break
        
        
    print('Sent ' + str(sampleCount) + ' samples in ' + str(ptb.GetSecs() - t0) + ' seconds')

    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('ip', help='IP address to which data are sent')
    parser.add_argument('port', help='port number to which data are sent', type=int)
    parser.add_argument('nChannels', help='number of channels (multiple of 32)', type=int)
    parser.add_argument('sr', help='sampling rate in Hz', type=int)
    parser.add_argument('duration', help='duration of the stream',type=int)
    args = parser.parse_args()
    startAmp(args.ip, args.port, nChannels=args.nChannels, sr = 1/args.sr, duration = args.duration)