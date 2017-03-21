
from botnet.logging import *

from subprocess import Popen, PIPE

from threading import Thread

import shlex, atexit


CMD1 = "raspivid -g 5 --profile baseline -t 0 -h {height} -w {width} -fps 60 -vf -hf -b {bitrate} -o -"
CMD2 = ("gst-launch-1.0", "fdsrc", "!", "h264parse", "!", "rtph264pay", "pt=96", "!", "udpsink")
HOST = "host={}"
PORT = "port={}"

class Video(dict):
    def __init__(self, **kwargs):
        self["width"] = 1280
        self["height"] = 720
        self["port"] = 6868
        self["bitrate"] = 10000000
        self.update(kwargs)
        atexit.register(self.kill)
        
    def run(self):
        self.kill()
        cmdline = shlex.split(CMD1.format(**self))
        gst = (CMD2 + (HOST.format(self.host),) +
               (PORT.format(self["port"]),))
        log(cmdline, gst)
        self.proc = Popen(cmdline, stdout=PIPE)
        self.proc2 = Popen(gst, stdin=self.proc.stdout)
        self.proc.stdout.close()

    def kill(self):
        if hasattr(self, "proc"):
            if self.proc.poll() is None:
                self.proc.kill()
            if self.proc2.poll() is None:
                self.proc2.kill()
            self.proc2.wait(1)
            return self.proc.wait(1)
        return False
        
