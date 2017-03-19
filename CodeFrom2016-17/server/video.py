
from botnet.logging import *

from subprocess import Popen, PIPE

from threading import Thread

import shlex, atexit

CMD1 = "raspivid --flush -hf -vf --profile baseline -w {width} -h {height} -t 0 --bitrate {bitrate} -n -o -"
CMD2 = ("nc.traditional", "-l", "-p")

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
        self.proc = Popen(cmdline, stdout=PIPE)
        self.proc2 = Popen(CMD2 + (str(self["port"]),), stdin=self.proc.stdout)
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
        
