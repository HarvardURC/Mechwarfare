
from botnet.logging import *

from subprocess import Popen

from threading import Thread

CMDLINE = "raspivid --flush --profile baseline -w {width} -h {height} -t 0 --bitrate {bitrate} -n -o - | nc.traditional {peer} {port}"

class Video(dict):
    def __init__(self, **kwargs):
        self["width"] = 1280
        self["height"] = 720
        self["port"] = 6000
        self["bitrate"] = 10000000
        self["peer"] = ""
        self.update(kwargs)
        
    def run(self):
        debug(self.kill())
        cmdline = CMDLINE.format(**self)
        self.proc = Popen(cmdline, shell=True)

    def kill(self):
        if hasattr(self, "proc"):
            debug(self.proc.pid)
            if self.proc.poll() is None:
                self.proc.kill()
            return self.proc.wait(1)
        return False
        
