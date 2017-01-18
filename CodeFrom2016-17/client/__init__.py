
from botnet.logging import *

from subprocess import Popen, DEVNULL

import atexit

VIDEO_PORT = 6000
CMDLINE = "netcat -l -p {port} | mplayer -fps 60 -cache 1024 -cache-min 1 -"

VIDOPTS = [
    {"width": 1920, "height": 1080},
    {"width": 1280, "height": 720}
]

class Client:
    def fatal(self, message):
        log(message)
        log("Quitting...")
        exit()

    def connected(self, protocol):
        self.protocol = protocol
        self.vidopts = 0
        self.video()

    def video(self, toggle=False):
        if hasattr(self, "proc"):
            self.proc.kill()
            self.proc.wait(1)
        if toggle:
            self.vidopts += 1
            if self.vidopts >= len(VIDOPTS):
                self.vidopts = 0
        self.proc = Popen(CMDLINE.format(port=VIDEO_PORT), shell=True, stderr=DEVNULL, stdout=DEVNULL)
        atexit.register(self.proc.kill)
        self.protocol.send_message("VSTR", VIDEO_PORT, 0, VIDOPTS[self.vidopts])
        
