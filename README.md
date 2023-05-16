# nl2lsl
LSL plugin for Digital Lynx SX

## Requirements
- python=3.9
- numpy
- pylsl

## Usage
```
python nl2lsl.py <IP> <port> <nBoard> <srate> <decimationFactor>
```
- IP: IP address to which data are received
- port: port number to which data are received
- nBoards: number of boards activited on the Digital Lynx SX system
- srate: sampling rate of received data in Hz
- decimationFactor: decimation factor of date fed to LSL

```
python NL_mockAmplifier.py <IP> <port> <nChannels> <srate> <duration>
```
- IP: IP address to which data are sent
- port: port number to which data are sent
- nChannels: number of channels
- srate: sampling rate of data in Hz
- duration: duration of the stream in seconds
