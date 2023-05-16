import socket
import time
import struct
import random
import numpy as np
import psychtoolbox as ptb

def startAmp(nChannels=64,sr=.001,duration=60):
	UDP_IP = "127.0.0.1"
	UDP_PORT = 5000 
	
	sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	
	sampleCount=0
	size = 68+nChannels*4 + 4
	
	f0 = 4
	
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
		struct.pack_into('<3Id2I10I',packet,0,stx,id,size,ts,status,ttl,*range(10))
		
		# pack data
		# data = np.arange(nChannels) + sampleCount*nChannels	
		# ,dtype= np.int32
		t = sampleCount*sr
		data = (np.sin(np.ones(nChannels)*2*np.pi*sampleCount*sr*f0)*1e6).astype(np.int32)
		
		struct.pack_into('<' + str(nChannels) + 'i', packet, 68,*data)
		
		# pack footer
		struct.pack_into('<I', packet, 68 + nChannels*4, 0)
		
		sock.sendto(packet,(UDP_IP, UDP_PORT))
		sampleCount+=1
		
		ptb.WaitSecs('UntilTime',t1+sr)
		if (ptb.GetSecs() - t0) > duration:
			break
	
	print('Sent ' + str(sampleCount) + ' samples in ' + str(ts) + ' seconds')

	

if __name__ == '__main__': 
 	startAmp(nChannels=64, sr = .0001, duration = 120)