
# plot.py
A small python script to read an HPGL plotter file and plot directly to the device via serial, while managing not to 
overflow the plotters command buffer. 

## The Why
I wrote this because I hit a problem with Chiplotle (http://sites.music.columbia.edu/cmc/chiplotle/) where large plots 
would hit a tipping point and error my plotter. ~~After some debugging I narrowed it down to how Chiplotle managed its 
commands throttling with the plotter and not the actually HPGL files themselves~~. I have a running theory it is due 
to my 9 pin to 25 pin cable and / or my USB to 9 pin serial adapter. This work is based off the good work of Dhananjay 
Balan (https://blog.dbalan.in/blog/2019/02/23/resurracting-an-hp-7440a-plotter/index.html) who made use of a way to 
query the plotters buffer status so not to overflow it with commands.

This is pretty specific to my scenario; HP7475A plotter with 1024 bytes of buffer, over serial RS232, using Python 3.9 
(what came on my MacBook). Your millage may vary. 

## The How
The script breaks up the HPGL commands into 1000 byte chunks and appends an "OA;" to the end. The OA command is asking 
for the "output actual position and pen status". When we receive a response we know the buffer is empty because OA was 
the last command on the stack, therefore we are okay to send the next chunk of commands over.

Care is taken for very long / chained pen down commands in case a single command is greater than 1024 bytes. These are 
transformed into atomic pen down commands. For example:
```
PD0,100,200,349,104,178,... 
```
Is transformed into:
```
PD0,100;
PD200,349;
PD104,178;
...
```
How to use:
```
$ python3 plot.py --help

usage: plot.py [-h] [--file image.hpgl] [--port /dev/tty.usbserial-1220]

Plot a file via a serial port.

optional arguments:
  -h, --help            show this help message and exit
  --file image.hpgl     A path to or the HPGL file you would like to plot.
  --port /dev/tty.usbserial-1220
                        The serial port to use.

```
A working example:
```
$ python3 plot.py --file image.hpgl --port /dev/tty.usbserial-1220

Received a response to my OA; command, buffer must be empty so it is time to send more commands.
Received a response to my OA; command, buffer must be empty so it is time to send more commands.
...
```