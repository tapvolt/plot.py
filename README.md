
# plot.py
A small python script to read a HPGL plotter file and plot directly to the device via serial, while managing not to overflow the plotters command buffer. 

## The why
I wrote this because I hit a problem with Chiplotle (http://sites.music.columbia.edu/cmc/chiplotle/) where large plots would hit a tipping point and error my plotter. After some debugging I narrowed it down to how Chiplotle managed its commands throttling with the plotter and not the actually HPGL files themselves. This work is based off the good work of Dhananjay Balan (# https://blog.dbalan.in/blog/2019/02/23/resurracting-an-hp-7440a-plotter/index.html) who made use of a way to query the plotters buffer status so not to overflow it with commands.

This is pretty specific to my scenario; HP7475A plotter with 1024 bytes of buffer, over serial RS232, using Python 3.9 (what came on my MacBook). Your millage may vary. 
## The how

```
$ plot.py --help

usage: plot.py [-h] [--file image.hpgl] [--port /dev/tty.usbserial-1220]

Plot a file via a serial port.

optional arguments:
  -h, --help            show this help message and exit
  --file image.hpgl     A path to or the HPGL file you would like to plot.
  --port /dev/tty.usbserial-1220
                        The serial port to use.

```
An example:
```
$ plot.py --file image.hpgl --port /dev/tty.usbserial-1220
...
plotting occurs
...
```