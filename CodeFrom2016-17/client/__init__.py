
from botnet.logging import *

from subprocess import Popen, DEVNULL, PIPE, STDOUT

import atexit

VIDEO_PORT = 6868
CMD1 = ["netcat", "{address}", "{port}".format(port=VIDEO_PORT)]
CMD2 = ["mplayer", "-fps", "60", "-cache", "1024", "-cache-min", "1", "-"]

VIDOPTS = [
    {"width": 1920, "height": 1080},
    {"width": 1280, "height": 720}
]

class Client:
    def __init__(self, addr):
        self.server = addr
    
    def fatal(self, message):
        log(message)
        log("Quitting...")
        exit()

    def connected(self, protocol):
        self.protocol = protocol
        self.vidopts = 0
        self.video()

    def video(self, toggle=False):
        if hasattr(self, "proc2"):
            self.proc2.kill()
            debug(self.proc2.wait(1))
        if hasattr(self, "proc1"):
            self.proc1.kill()
            self.proc1.wait(1)
        if toggle:
            self.vidopts += 1
            if self.vidopts >= len(VIDOPTS):
                self.vidopts = 0
        CMD1[1] = CMD1[1].format(address=self.server)
        self.proc1 = Popen(CMD1, stdout=PIPE)
        self.proc2 = Popen(CMD2, stdin=self.proc1.stdout, stderr=STDOUT, stdout=get_log_fd("mplayer"))
        self.proc1.stdout.close()
        atexit.register(self.proc1.kill)
        atexit.register(self.proc2.kill)
        self.protocol.send_message("VSTR", VIDEO_PORT, 0, VIDOPTS[self.vidopts])
        
