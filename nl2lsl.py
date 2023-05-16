import argparse
import socket
import struct
import numpy as np
from pylsl import StreamInfo, StreamOutlet, local_clock

def nl2lsl(UDP_IP="192.168.3.100", UDP_PORT=26090, nBoards=2, srate=1024, decimationFactor=1):
    # UDP_IP = "127.0.0.1"
    # UDP_PORT = 5005 
    # nBoards = 2 # number neuralynx board
    # srate = 1000 # sampling rate

    # size in bytes
    header_size = 68
    data_size = 128 # data size per board
    footer_size = 4
    sampleCount = 0

    packet_size = header_size + 4*32*nBoards + footer_size # packet size in bytes
    nChannels = nBoards*32 # number of channels streamed

    # open a socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    sock.settimeout(None)
    sock.bind((UDP_IP, UDP_PORT))

    # create LSL stream
    info = StreamInfo('NeuraLynx', 'EEG', nChannels, srate/decimationFactor, 'float32', 'myuid34234')
    info.desc().append_child_value("manufacturer", "NeuraLynx")
    channels = info.desc().append_child("channels")

    for n in range(nChannels):
        channels.append_child("channel") \
            .append_child_value("label", str(n+1)) \
            .append_child_value("unit", "microvolts") \
            .append_child_value("type", "EEG") \
            .append_child_value("ref", str(0))

    outlet = StreamOutlet(info)

    print('Waiting for data...')
    firstPacketReceived = False
    while True:
        # get data from neuralynx
        try:
            packet, addr = sock.recvfrom(packet_size)
        except socket.timeout:
            print('Timeout error: no data received during the last 2 seconds')
            break       

        if not firstPacketReceived:
            print('Receiving data from ' +addr[0]+':'+str(addr[1])+'... [press Ctrl+c to stop]')
            sock.settimeout(2)
        
        firstPacketReceived = True
        
        if (sampleCount%decimationFactor) == 0:
            header = struct.unpack_from('<3IQ2I10I',packet,offset = 0)
            data = struct.unpack_from('<' + str(nChannels) +'i',packet,offset = header_size)
            footer = struct.unpack_from('<I',packet,offset = header_size+nChannels*4)
            # push data in LSL stream
            outlet.push_sample(np.array(data)/1e5)
            
        sampleCount += 1
        
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('ip', help='IP address to which data are received')
    parser.add_argument('port', help='port number to which data are received', type=int)
    parser.add_argument('nBoards', help='number of boards of the Neuralynx system',type=int)
    parser.add_argument('srate', help='sampling rate',type=int)
    parser.add_argument('decimationFactor', help='decimation factor',type=int)
    args = parser.parse_args()
    
    nl2lsl(args.ip, args.port, args.nBoards, args.srate, args.decimationFactor)
    
    